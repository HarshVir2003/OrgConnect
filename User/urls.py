from django.urls import path
from User.views import UserList

urlpatterns = [
    path('', UserList.as_view(), name='User'),
]
