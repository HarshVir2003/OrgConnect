from django.urls import path
from .views import CreateUserAPIView, SendMessageAPIView

urlpatterns = [
    path('create-user/', CreateUserAPIView.as_view(), name='create_user'),
    path('send-message/', SendMessageAPIView.as_view(), name='send_message'),
]
