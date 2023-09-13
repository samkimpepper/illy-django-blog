from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)

class Topic(models.Model):
    name = models.CharField(max_length=20)

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    # views : 수정필요, 
    views = models.IntegerField(default=0)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    img = models.ImageField(upload_to="images/")
    


