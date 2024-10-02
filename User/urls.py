from django.urls import path
from User.views import UserList, UserRegister, UserLogin, logout_user, profile_view

urlpatterns = [
    path('profile/', profile_view, name='default_profile'),
    path('profile/<int:id>/', UserList.as_view(), name='User'),
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', logout_user, name='logout')
]
