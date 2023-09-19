from django.db import models
from django.contrib.auth.models import AbstractUser
import os

class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    topic = models.CharField(max_length=255, default='전체')
    img = models.ImageField(upload_to="images/")
    publish = models.CharField(max_length=1, default='Y')
    author_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.content = self.content.replace('..', '/blog')
        super().save(*args, **kwargs)
        
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/')  # 게시물 이미지 필드

    def delete(self, *args, **kwargs):
        # 게시물 삭제 시 연결된 이미지 파일도 삭제
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
