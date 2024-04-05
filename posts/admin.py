from django.contrib import admin
from .models import Post, Comment, Photo


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "content",
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "content",
    ]


@admin.register(Photo)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'file',
        'caption',
    ]