from typing import Any
from django import forms
from .models import Post, Comment, Photo


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','content')
        widgets={    
            'title': forms.TextInput(attrs={'placeholder':'제목'}),
            'content': forms.Textarea(attrs={'placeholder':'내용'}),
        }
    
    def save(self, *args, **kwargs):
        post = super().save(commit=False)
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)

    def save(self, post_id, *args, **kwargs):
        comment = super().save(commit=False)
        post=Post.objects.get(id=post_id)
        comment.post=post
        comment.save()


class PhotoForm(forms.ModelForm):
    class Meta:
        model=Photo
        fields=('file','caption')
        
    def save(self, post_id, *args, **kwargs):
        photo=super().save(commit=False)
        post=Post.objects.get(id=post_id)
        photo.post=post
        photo.save()