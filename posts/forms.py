from django import forms
<<<<<<< HEAD
from .models import Post
=======
from .models import Post, Comment
>>>>>>> comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
<<<<<<< HEAD
        fields = "__all__"
=======
        fields = "__all__"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)

    def save(self):
        comment = super().save(commit=False)
        return comment
>>>>>>> comment
