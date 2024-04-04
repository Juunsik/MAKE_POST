from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    # 로그인, 회원 가입
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    # Kakao 로그인
    path("login/kakao/", views.KakaoLogin.as_view(), name="kakao-login"),
    path("login/kakao/callback/", views.KakaoCallBack.as_view(), name="kakao-callback"),
    path("update-profile/", views.UpdateProfileView.as_view(), name="update"),
    path("<int:pk>/", views.UserProfileView.as_view(), name="profile"),
]
