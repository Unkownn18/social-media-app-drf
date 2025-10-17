from rest_framework import serializers
from .models import Post,Comment
from django.contrib.auth.models import User
class Userserializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username']

class PostSerializer(serializers.ModelSerializer):
    user=Userserializer(read_only=True)
    class Meta:
        model=Post
        fields=['id','title','user','body']
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['id','created_at','user','content']
        read_only_fields=['id','created_at','user']