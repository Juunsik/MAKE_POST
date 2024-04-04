from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse


# Create your models here.


class User(AbstractUser):
    LOGIN_EMAIL='email'
    LOGIN_KAKAO='kakao'
    
    LOGIN_CHOICES=(
        (LOGIN_EMAIL, 'Email'),
        (LOGIN_KAKAO, 'kakao'),
    )
    
    profile_img=models.ImageField(upload_to='profiles',blank=True)
    superhost=models.BooleanField(default=False)
    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )
    
    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})
    