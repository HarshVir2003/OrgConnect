from django.urls import path
from Groups.views import GroupsView

urlpatterns = [
    path('', GroupsView.as_view(), name='getGroups')
]
