from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    # 게시물
    path("", views.post_list, name="list"),
    path("hits/", views.post_list_hits, name="hits"),
    path("write/", views.post_create, name="create"),
    path("<int:post_id>/", views.post_detail, name="detail"),
    path("<int:post_id>/edit/", views.post_update, name="update"),
    path("<int:post_id>/delete/", views.page_delete, name="delete"),
    # 댓글
    path("comments/write/<int:post_id>/", views.create_comment, name="comment-create"),
    path(
        "comments/delete/<int:comment_id>", views.delete_comment, name="comment-delete"
    ),
    path(
        "comments/update/<int:comment_id>", views.update_comment, name="comment-update"
    ),
    # 이미지
    path("<int:pk>/photos/", views.RoomPhotosView.as_view(), name="photos"),
    path("<int:pk>/photos/add/", views.AddPhotoView.as_view(), name="add-photo"),
    path(
        "<int:post_pk>/photos/<int:photo_pk>/delete/",
        views.delete_photo,
        name="delete-photo",
    ),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/edit/",
        views.EditPhotoView.as_view(),
        name="edit-photo",
    ),
]
