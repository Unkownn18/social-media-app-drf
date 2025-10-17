from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    user=models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    body=models.CharField()
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    created_at=models.DateField(auto_now_add=True)