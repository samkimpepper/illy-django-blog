from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    # views : 수정필요, 
    views = models.IntegerField()
    topic = models.CharField(max_length=20)
    img = models.ImageField(upload_to="images/")
    
class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
