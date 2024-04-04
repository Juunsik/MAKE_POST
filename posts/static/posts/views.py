from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.


# 목록 가져오기
def post_list(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 8)
    current_page = request.GET.get("page")
    if current_page is None:
        current_page = 1
    page = paginator.page(current_page)
    return render(request, "posts/post_list.html", {"page": page})

# 상세 페이지
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # 가정: 'comments'는 Post 모델에 related_name으로 설정되어 있음
    form = CommentForm()
    return render(request, "posts/post_detail.html", {"post": post})

# 게시물 생성
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save()
            return redirect("posts:detail", post_id=new_post.id)
    else:
        form = PostForm()
    return render(request, "posts/post_form.html", {"form": form})


# 게시물 수정
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("posts:detail", post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, "posts/post_form.html", {"form": form})


# 게시물 삭제
def page_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect("posts:list")
    else:
        return render(request, "posts/post_confirm_delete.html", {"post": post})


# 댓글 생성
def comment_create(request, post_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        post = Post.objects.get(id=post_id) # 댓글이 어떤 게시물의 댓글인지 확인
        if not post:
            return redirect("posts:list")
        if form.is_valid():
            comment = form.save()
            comment.post = post
            comment.save()
            messages.success(request, "Post reviewed")
            return redirect("posts:detail", post_id=post.id)
    else:
        form=CommentForm()
    return render(request, "posts/post_detail.html", {"form": form})