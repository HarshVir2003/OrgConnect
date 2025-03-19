from django.urls import path
from User.views import UserList, UserRegister, UserLogin, LogoutView, ProfileView


urlpatterns = [
    path('profile/', ProfileView.as_view(), name='default_profile'),
    path('profile/<int:id>/', UserList.as_view(), name='User'),
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),


]
