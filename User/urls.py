from django.urls import path
from User.views import UserList, UserRegister, UserLogin, LogoutView, ProfileView, UserImageView, UserIdImageView


urlpatterns = [
    path('profile/', ProfileView.as_view(), name='default_profile'),
    path('profile/<int:id>/', UserList.as_view(), name='User'),
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/image/', UserImageView.as_view(), name='user_image'),
    path('user/image/<int:id>/', UserIdImageView.as_view(), name='user_image_id')

]
