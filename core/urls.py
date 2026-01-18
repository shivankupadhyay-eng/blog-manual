from django.urls import path
from .views import CustomUserAPIView, LoginAPIView, BlogAPIView,CommentAPIView,VoteAPIView,BlogVoteStatsAPIView,BlogVoteDetailAPIView

urlpatterns = [
    # User Endpoints
    path("users/", CustomUserAPIView.as_view(), name="user-create"),
    path("users/<int:id>/", CustomUserAPIView.as_view(), name="user-detail"),
    
    path("login/", LoginAPIView.as_view()),

    # Blog Endpoints
    path("blogs/", BlogAPIView.as_view(), name="blog-create"),
    path("blogs/<int:id>/", BlogAPIView.as_view(), name="blog-detail"),
    
    # Blog Vote Stats
    path("blogs/stats/", BlogVoteStatsAPIView.as_view(), name="blog-vote-stats"),
    path("blogs/<int:id>/stats/",BlogVoteDetailAPIView.as_view()),

    # Comment Endpoints
    path("comments/", CommentAPIView.as_view(), name="comment-create"),
    path("comments/<int:id>/", CommentAPIView.as_view(), name="comment-detail"),
    
    # Vote Endpoints
    path("blogs/<int:blog_id>/votes/", VoteAPIView.as_view(), name="vote-manage"),
]
