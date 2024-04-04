from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from posts import models as post_models
from .models import User


# Register your models here.

class PostInline(admin.TabularInline):
    
    model=post_models.Post


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    
    inlines=(PostInline,)
    
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "profile_img",
                    "superhost",
                )
            },
        ),
    )
