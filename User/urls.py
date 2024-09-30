from django.urls import path
from User.views import UserList, UserRegister, UserLogin

urlpatterns = [
    path('profile/<int:id>/', UserList.as_view(), name='User'),
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
]
