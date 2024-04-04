from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    # 게시물
    path("", views.post_list, name="list"),
    path("post/write/", views.post_create, name="create"),
    path("post/page/<int:post_id>/", views.post_detail, name="detail"),
    path("post/page/<int:post_id>/edit/", views.post_update, name="update"),
    path("post/page/<int:post_id>/delete/", views.page_delete, name="delete"),
    # 댓글
    path("comments/write/<int:post_id>/", views.comment_create, name="comment-create"),
]