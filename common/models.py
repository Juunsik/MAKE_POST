from django.db import models

<<<<<<< HEAD
=======

>>>>>>> comment
# Create your models here.
class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
<<<<<<< HEAD
    
    class Meta:
        abstract = True
=======

    class Meta:
        abstract = True
>>>>>>> comment
