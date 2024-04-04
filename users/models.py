from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    profile_img=models.ImageField(blank=True)
    superhost=models.BooleanField(default=False)