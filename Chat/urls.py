from django.urls import path
from .views import CreateUserAPIView, SendMessageAPIView, GetChatHistoryAPIView

urlpatterns = [
    path('create-user/', CreateUserAPIView.as_view(), name='create_user_chat'),
    path('history/', GetChatHistoryAPIView.as_view(), name='chat-history'),
    path('send-message/', SendMessageAPIView.as_view(), name='send_message'),
]
