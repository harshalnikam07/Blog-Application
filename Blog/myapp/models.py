from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    # CAT=((1,'Technology'),(2,'Health'),(3,'Travel'),(4,'Education'))
    title=models.CharField(max_length=50)
    category=models.CharField(max_length=50, default='1')
    content=models.CharField(max_length=2000)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    author=models.ForeignKey('auth.user', on_delete=models.CASCADE, db_column='aid')
    image=models.ImageField(upload_to='image')

class SubPlan(models.Model):
    sub_plan=models.CharField(max_length=50)
    price=models.IntegerField()
    no_of_post=models.IntegerField(default=1)


class Author(models.Model):
    aid=models.ForeignKey('auth.user', on_delete=models.CASCADE, db_column='aid')
    sub_plan=models.ForeignKey('SubPlan', on_delete=models.CASCADE, db_column='sub_plan')

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    # rating = models.IntegerField(default=0)