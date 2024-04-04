from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
<<<<<<< HEAD
from .models import Post
from .forms import PostForm



# Create your views here.
=======
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.


>>>>>>> comment
# 목록 가져오기
def post_list(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 8)
    current_page = request.GET.get("page")
    if current_page is None:
        current_page = 1
    page = paginator.page(current_page)
    return render(request, "posts/post_list.html", {"page": page})

<<<<<<< HEAD
=======

>>>>>>> comment
# 상세 페이지
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "posts/post_detail.html", {"post": post})

<<<<<<< HEAD
=======

>>>>>>> comment
# 게시물 생성
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save()
<<<<<<< HEAD
            return redirect("post-detail",post_id=new_post.id)
    else:
        form = PostForm()
    return render(request, "posts/post_form.html",{"form": form})
    # 보려면 get을 써야하는데 
=======
            return redirect("posts:detail", post_id=new_post.id)
    else:
        form = PostForm()
    return render(request, "posts/post_form.html", {"form": form})

>>>>>>> comment

# 게시물 수정
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
<<<<<<< HEAD
            return redirect("post-detail", post_id=post.id)
=======
            return redirect("posts:detail", post_id=post.id)
>>>>>>> comment
    else:
        form = PostForm(instance=post)
    return render(request, "posts/post_form.html", {"form": form})

<<<<<<< HEAD
#게시물 삭제
=======

# 게시물 삭제
>>>>>>> comment
def page_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
<<<<<<< HEAD
        return redirect("post-list")
    else:
        return render(request, "posts/post_confirm_delete.html", {"post": post})

=======
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
    return render(request, "posts/comment_form.html", {"form": form})
>>>>>>> comment
