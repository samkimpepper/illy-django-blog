from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)
    

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    # views : 수정필요, 
    views = models.IntegerField(default=0)
    topic = models.CharField(max_length=255, default='전체')
    img = models.ImageField(upload_to="images/")
    publish = models.CharField(max_length=1, default='Y')
    author_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # '..' 문자열이 포함된 content 필드를 변경
        self.content = self.content.replace('"..', '"')
        super().save(*args, **kwargs)
