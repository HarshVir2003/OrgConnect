from django.urls import path
from Feeds.views import (
    FeedView, PostsPostingView, CommentView, LikeView
)

urlpatterns = [
    path('', FeedView.as_view(), name='feeds'),
    path('post/', PostsPostingView.as_view(), name='post-create'),
    path('post/<int:id>/', PostsPostingView.as_view(), name='post-detail'),
    path('comment/', CommentView.as_view(), name='comment-create'),
    path('like/', LikeView.as_view(), name='like-create'),
    path('comment/<int:id>/', CommentView.as_view(), name='comment-detail'),
    path('like/<int:id>/', LikeView.as_view(), name='like-create'),
]
