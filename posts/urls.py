from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="post-list"),
    path("post/write/", views.post_create, name="post-create"),
    path("post/page/<int:post_id>/", views.post_detail, name="post-detail"),
    path("post/page/<int:post_id>/edit/", views.post_update, name="post-update"),
    path("post/page/<int:post_id>/delete/", views.page_delete, name="post-delete"),
]