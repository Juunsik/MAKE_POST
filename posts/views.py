from django.shortcuts import render , redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Post
from  .forms import PostForm

# Create your views here.

#포스트 가져오기
def post_list(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list,8)
    current_page = request.GET.get("page")
    if current_page is not None:
        current_page = 1
    page = paginator.get_page(current_page)
    return render(request, "posts/post_list.html",{"page": page})

#상세페이지
def post_detail(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    return render(request, "posts/post_detail.html",{"post": post})
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save()
            return redirect("post-detail",post_id=new_post.id)
    else:
        form = PostForm()
    return render(request, "posts/post_form.html",{"form":form})

def post_update(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post-detail",post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, "posts/post_form.html",{"form":form})

def page_delete(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect("post-list")
    else:
        return render(request, "posts/post_confirm_delete.html",{"post":post})

