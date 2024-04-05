import requests
import os
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.http import Http404
from django.views import View
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixins
from config import settings

# Create your views here.


# FormView를 사용해서 구현하는 바업
class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("posts:list")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("posts:list")


# View를 사용해서 구현하는 방법
# class LoginView(View):
#     def get(self, request):
#         form=forms.LoginForm()
#         return render(request, 'users/login.html', {'form':form})

#     def post(self, request):
#         form=forms.LoginForm(request.POST)
#         if form.is_valid():
#             email=form.cleaned_data.get('email')
#             password=form.cleaned_data.get('password')
#             user=authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse('posts:list'))
#         return render(request, 'users/login.html', {'form':form})


def log_out(request):
    messages.info(request, f"See you later")
    logout(request)
    return redirect(reverse("posts:list"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("posts:list")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        print(user)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


# kakao 로그인
class KakaoLogin(View):
    def get(self, request):
        client_id=os.environ.get('KAKAO_ID')
        redirect_uri='http://127.0.0.1:8000/users/login/kakao/callback/'
        kakao_login_uri='https://kauth.kakao.com/oauth/authorize'
        
        return redirect(f'{kakao_login_uri}?client_id{client_id}&redirect_uri={redirect_uri}&response_type=code')


class kakaoException(Exception):
    pass

class KakaoCallBack(View):
    def get(self, request):
        try:
            data=request.query_params.copy()
            
            # access token 발급 요청
            code=data.get('code')
            if not code:
                raise Http404()
            
            request_data={
                'grant_type':'authorization_code',
                'client_id':os.environ.get('KAKAO_ID'),
                'redirect_uri':'http://127.0.0.1:8000/users/login/kakao/callback/',
                'client_secret':os.environ.get('CLIENT_KEY'),
                'code':code,
            }
            
            token_headers={
                'Content-type':'application/x-www-form-urlencoded;charset=utf-8'
            }
            token_res=requests.post('https://kauth.kakao.com/oauth/token', data=request_data, headers=token_headers)
            
            token_json=token_res.json()
            access_token=token_json.get('access_token')
            if not access_token:
                return Http404()
            access_token=f'Bearer {access_token}'
            
            # 사용자 정보 요청
            auth_headers={
                'authorization':access_token,
                'Content-type':'application/x-www-form-urlencoded;charset=utf-8',
            }
            user_info_res=requests.get('https://kakao.com/v2/user/me', headers=auth_headers)
            user_info_json=user_info_res.json()
            
            kakao_account=user_info_json.get('kakao_account')
            profile_img=user_info_json['properties']['profile_image']
            kakao_nickname=user_info_json['properties']['nickname']
            
            if not kakao_account:
                return Http404()
            user_email=kakao_account.get('email')
            
            if user_email is None:
                    raise kakaoException("Please also give me your email")

            try:
                user = models.User.objects.get(email=user_email)
                if user.login_method!=models.User.LOGIN_KAKAO:
                    raise kakaoException(f'please log in with: {user.login_method}')
            except models.User.DoesNotExist:
                user = models.User.objects.create(
                    email=user_email,
                    username=user_email,
                    first_name=kakao_nickname,
                    login_method=models.User.LOGIN_KAKAO,
                )
                user.set_unusable_password()
                user.save()
                if profile_img is not None:
                    photo_request = requests.get(profile_img)
                    user.profile_img.save(
                        f"{kakao_nickname}-profile_img", ContentFile(photo_request.content)
                    )
            login(request, user)
            messages.success(request, f"Welcome back{user.first_name}")
            return redirect(reverse("posts:list"))
        except kakaoException as e:
            messages.error(request, e)
            return redirect(reverse("users:login"))





# class KakaoLogin(View):
#     def get(self, request):
#         kakao_api='https://kauth.kakao.com/oauth/authorize?response_type=code'
#         redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
#         client_id = os.environ.get("KAKAO_ID")
#         return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")

# class kakaoException(Exception):
#     pass

# class KaKaoCallBack(View):
#     def get(self, request):
#         try:
#             data={
#                 'grant_type':'authorization_code',
#                 'client_id':os.environ.get('KAKAO_ID'),
#                 'redirection_uri':'http://127.0.0.1:8000/users/login/kakao/callback',
#                 'code':request.GET['code']
#             }

#             kakao_token_api='https://kauth.kakao.com/oauth/token'
#             access_token=requests.post(kakao_token_api, data=data).json()['access_token']
#             kakao_user_api='https://kapi.kakao.com/v2/user/me'
#             header={'Authorization':f'Bearer ${access_token}'}
#             user_information=requests.get(kakao_user_api, headers=header).json()
            
#             kakao_email=user_information['kakao_account']['email']
#             profile_img=user_information['properties']['profile_image']
#             kakao_nickname=user_information['properties']['nickname']

#             if kakao_email is None:
#                 raise kakaoException("Please also give me your email")

#             try:
#                 user = models.User.objects.get(email=kakao_email)
#                 if user.login_method!=models.User.LOGIN_KAKAO:
#                     raise kakaoException(f'please log in with: {user.login_method}')
#             except models.User.DoesNotExist:
#                 user = models.User.objects.create(
#                     email=kakao_email,
#                     username=kakao_email,
#                     first_name=kakao_nickname,
#                 )
#                 user.set_unusable_password()
#                 user.save()
#                 if profile_img is not None:
#                     photo_request = requests.get(profile_img)
#                     user.profile_img.save(
#                         f"{kakao_nickname}-profile_img", ContentFile(photo_request.content)
#                     )
#             login(request, user)
#             messages.success(request, f"Welcome back{user.first_name}")
#             return redirect(reverse("posts:list"))
#         except kakaoException as e:
#             messages.error(request, e)
#             return redirect(reverse("users:login"))



class UserProfileView(DetailView):
    model = models.User
    context_object_name = "user_obj"


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "first_name",
        "last_name",
    )
    success_message = "Profile Updated"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last name"}
        return form
