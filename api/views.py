from django.shortcuts import render
from rest_framework.views import APIView
from users.serializers import RegisterSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework import status,generics
from .permissions import permissions,isPostCreator,isCommentCreator,isFeedCreator
from django.contrib.auth.models import User
from posts.serializers import PostSerializer,CommentSerializer
from posts.models import Post,Comment
from rest_framework.viewsets import ModelViewSet
from follow.models import Follow
from follow.serializers import FollowSerializer,Userserializer
# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset=User
    serializer_class=RegisterSerializer

class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class PostView(ModelViewSet):
    queryset=Post
    serializer_class=PostSerializer
    permission_classes=[permissions.IsAuthenticated,isPostCreator]
    def get_queryset(self):
        return Post.objects.all()
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class CommentView(ModelViewSet):
    serializer_class=CommentSerializer
    permission_classes=[permissions.IsAuthenticated,isCommentCreator]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])
    def perform_create(self, serializer):
        post=Post.objects.get(pk=self.kwargs['post_pk'])
        serializer.save(user=self.request.user,post=post)
        
class FollowView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,user_id):
        try:
            to_folow=User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail":"User not found"},status=status.HTTP_404_NOT_FOUND)
        if request.user==to_folow:
            return Response({"detail":"you cannot follow yourself"},status=status.HTTP_400_BAD_REQUEST)
        
        follow,created=Follow.objects.get_or_create(follower=request.user,following=to_folow)
        if not created:
            return Response({"detail":"you already follow this user"},status=status.HTTP_400_BAD_REQUEST)
        
        return Response(FollowSerializer(follow).data,status=status.HTTP_201_CREATED)
    

    def delete(self,request,user_id):
        try:
            to_unfollow=User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail":"User not found"},status=status.HTTP_404_NOT_FOUND)
        try:
            follow=Follow.objects.get(follower=request.user,following=to_unfollow)
            follow.delete()    
            return Response({'detail': 'Unfollowed successfully.'}, status=204)
        except Follow.DoesNotExist:
            return Response({'detail': 'You do not follow this user.'}, status=400)    
        

class FollowingListView(generics.ListAPIView):
    serializer_class=Userserializer
    permission_classes=[permissions.IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.filter(followers_sets__follower=self.request.user)
    
class FollowersListView(generics.ListAPIView):
    serializer_class=Userserializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(following_sets__following=self.request.user)

class MyFeedView(ModelViewSet):
    serializer_class=PostSerializer
    permission_classes=[permissions.IsAuthenticated,isFeedCreator]

    def get_queryset(self):
        following_user_id=Follow.objects.filter(follower=self.request.user).values_list('following_id',flat=True)
        return Post.objects.filter(user__id__in=following_user_id).order_by('-created_at')
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)