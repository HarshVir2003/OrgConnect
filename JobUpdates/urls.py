from django.urls import path
from JobUpdates.views import JobUpdatesView, JobPosting

urlpatterns = [
    path('', JobUpdatesView.as_view(), name='jobUpdates'),
    path('post/', JobPosting.as_view(), name='jobpost')
]
