from django.urls import path
from Feeds.views import FeedView

urlpatterns = [
    path('', FeedView.as_view(), name='LoadViews')
]
