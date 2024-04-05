from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView, UpdateView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib import messages
from users import mixins as user_mixins
from . import models, forms
from users.models import User

# Create your views here.


# 목록 가져오기
def post_list(request):
    post_list = models.Post.objects.all().order_by('-created_at')
    paginator = Paginator(post_list, 8)
    current_page = request.GET.get("page")
    if current_page is None:
        current_page = 1
    page = paginator.page(current_page)
    return render(request, "posts/post_list.html", {"page": page})

# 목록 가져오기 (조회수 기준)
def post_list_hits(request):
    post_list = models.Post.objects.all().order_by('-read_count')
    paginator = Paginator(post_list, 8)
    current_page = request.GET.get("page")
    if current_page is None:
        current_page = 1
    page = paginator.page(current_page)
    return render(request, "posts/post_list.html", {"page": page})

# 상세 페이지
def post_detail(request, post_id):
    post = get_object_or_404(models.Post, id=post_id)
    post.read_count=post.read_count+1
    post.save()
    return render(request, "posts/post_detail.html", {"post": post})

# 게시물 생성
@login_required
def post_create(request):
    if request.method == "POST":
        form = forms.PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(user=request.user)  # 현재 로그인한 사용자 전달
            return redirect("posts:detail", post_id=new_post.id)
    else:
        form = forms.PostForm()
    return render(request, "posts/post_form.html", {"form": form})


# 게시물 수정
@login_required
def post_update(request, post_id):
    post = get_object_or_404(models.Post, id=post_id)
    if request.method == "POST":
        form = forms.PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save(user=request.user)  # 현재 로그인한 사용자 전달
            return redirect("posts:detail", post_id=post.id)
    else:
        form = forms.PostForm(instance=post)
    return render(request, "posts/post_form.html", {"form": form})


# 게시물 삭제
@login_required
def page_delete(request, post_id):
    post = get_object_or_404(models.Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect("posts:list")
    else:
        return render(request, "posts/post_confirm_delete.html", {"post": post})


# 댓글 생성
def create_comment(request, post_id):
    post = get_object_or_404(models.Post, id=post_id)
    print(post)
    if request.method == 'POST':
        print(1)
        content=request.POST.get('content')
        models.Comment.objects.create(post=post, content=content)
        return redirect('posts:detail', post_id=post.id)
    else:
        print(2)
        return render(request, "posts/comment_form.html")
    

# 댓글 삭제
def delete_comment(request, comment_id):
    comment=get_object_or_404(models.Comment, id=comment_id)
    comment.delete()
    return redirect('posts:detail', post_id=comment.post.id)

def update_comment(request, comment_id):
    comment=get_object_or_404(models.Comment, id=comment_id)
    if request.method=='POST':
        comment.content=request.POST.get('content')
        comment.save()
        return redirect('posts:detail', post_id=comment.post.id)
    else:
        return render(request,'posts/comment_update_form.html', {'comment':comment})

# 댓글 수정
# @login_required
# def edit_comment(request, comment_id):
#     comment = get_object_or_404(models.Comment, id=comment_id)
#     if request.method == 'POST':
#         form = forms.CommentForm(request.POST, instance=comment)
#         if form.is_valid():
#             form.save()
#             return redirect('post_detail', post_id=comment.post.id)
#     else:
#         form = models.CommentForm(instance=comment)
#     return render(request, 'edit_comment.html', {'form': form})

# # 댓글 삭제
# @login_required
# def delete_comment(request, comment_id):
#     comment = get_object_or_404(models.Comment, id=comment_id)
#     if request.method == 'POST':
#         comment.delete()
#         return redirect('post_detail', post_id=comment.post.id)
#     return render(request, 'delete_comment.html', {'comment': comment})

# @login_required
# def comment_create(request, post_id):
#     post = models.Post.objects.get(id=post_id) # 댓글이 어떤 게시물의 댓글인지 확인
#     if request.method == "POST":
#         form = forms.CommentForm(request.POST)
#         print(form)
#         if not post:
#             return redirect("posts:list")
#         if form.is_valid():
#             comment = form.save()
#             print(comment.post_id, comment.user_pk)
#             comment.save()
#             messages.success(request, "Post reviewed")
#         return redirect("posts:detail", post_id=post.id)
#     else:
#         form=forms.CommentForm(user=request.user)
#     return render(request, "posts/comment_create.html", {"form": form})

# 댓글 수정    
# @login_required
# def comment_update(request, post_id, comment_id):
#     post = get_object_or_404(models.Post, id=post_id)
#     user = request.user
    
#     form=forms.CommentForm(request.POST)



# 이미지
class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Post
    template_name = "posts/post_photos.html"

    def get_object(self, queryset=None):
        post = super().get_object(queryset=queryset)
        if post.host.pk != self.request.user.pk:
            raise Http404()
        return post
    

# 이미지 삭제
@login_required
def delete_photo(request, post_id, photo_id):
    user = request.user
    try:
        post = models.Post.objects.get(pk=post_id)
        if post.host.pk != user.pk:
            messages.error(request, "Can't delete that photo")
        else:
            models.Photo.objects.filter(pk=photo_id).delete()
            messages.success(request, "Photo Deleted")
        return redirect(reverse("posts:photos", kwargs={"pk": post_id}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))
    

# 이미지 수정
class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "posts/photo_edit.html"
    pk_url_kwarg = "photo_id"
    success_message = "Photo Updated"
    fields = ("caption",)

    def get_success_url(self):
        post_id = self.kwargs.get("post_id")
        return reverse("posts:photos", kwargs={"pk": post_id})

# 이미지 추가
class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    template_name = "rooms/photo_create.html"
    form_class = forms.PhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("posts:photos", kwargs={"pk": pk}))