from django.db import models
from common.models import CommonModel


# Create your models here.
class Photo(CommonModel):
    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="post_photos")
    post = models.ForeignKey("Post", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Post(CommonModel):

    title = models.CharField(max_length=100)
    content = models.TextField()
    read_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    host=models.ForeignKey('users.User', related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def first_photo(self):
        try:
            (photo,) =self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None


class Comment(CommonModel):
    content = models.TextField()
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.content}-{self.post}"
    
    # '-created_at'으로 했는데 동작안해서 list 두개 만듬
    class Meta:
        ordering=('created_at',)
