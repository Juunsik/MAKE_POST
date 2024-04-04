from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        # widgets = {
        #     'title': forms.TextInput(attrs={'placeholder': 'Please enter a title'}),
        #     'content': forms.TextInput(attrs={'placeholder': 'Write your story...'}),
        #     'iamge' : 추가예정
        # }