from django.urls import path
from User.views import UserList, UserRegister

urlpatterns = [
    path('profile/', UserList.as_view(), name='User'),
    path('register/', UserRegister.as_view(), name='register')
]
