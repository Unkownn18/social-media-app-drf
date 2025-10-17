from django.urls import path,include
from .views import RegisterView,LoginView,PostView,CommentView,FollowView,FollowingListView,FollowersListView,MyFeedView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_nested import routers
router=routers.DefaultRouter()
router.register(r'posts',PostView,basename='post')
router.register(r'feed',MyFeedView,basename='feed')
post_router=routers.NestedDefaultRouter(router,'posts',lookup='post')
post_router.register(r'comments',CommentView,basename='commment')    
feed_router=routers.NestedDefaultRouter(router,'feed',lookup='post')
feed_router.register(r'comments',CommentView,basename='feed-comments')
urlpatterns=[
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('',include(router.urls)),
    path('',include(post_router.urls)),
    path('',include(feed_router.urls)),
    path('refresh/',TokenRefreshView.as_view()),
    path('follow/<int:user_id>/',FollowView.as_view()),
    path('following/',FollowingListView.as_view()),
    path('follower/',FollowersListView.as_view()),
]