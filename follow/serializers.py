from rest_framework import serializers
from posts.serializers import Userserializer
from .models import Follow

class FollowSerializer(serializers.ModelSerializer):
    follower=Userserializer(read_only=True)
    following=Userserializer(read_only=True)
    class Meta:
        model=Follow
        fields=['id','follower','following','created_at']       