from django.urls import path
from . import views


urlpatterns = [
    path("", views.post_list, name="post-list"),
    path("post/write/", views.post_create, name="post-create"),
    path("post/page/<int:post_id>/", views.post_detail, name="post-detail"),
    path("post/edit/<int:post_id>/edit", views.post_update, name="post-update" ),
    path("post/delete/<int:post_id>/delete/", views.page_delete, name="post-delete"),
    path("post/login/<int:post_id>/login/", views.page_delete, name="post-login"),
    path("post/CreateID/<int:post_id>/CreateID/", views.page_delete, name="CreateID"),
]