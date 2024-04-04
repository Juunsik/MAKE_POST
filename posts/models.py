from django.db import models
from common.models import CommonModel


# Create your models here.
class Post(CommonModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    read_count = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.title

class Comment(CommonModel):
    content=models.TextField()
    post=models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.content}-{self.post}'
    
