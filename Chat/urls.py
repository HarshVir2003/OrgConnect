from django.urls import path
from .views import CreateUserAPIView, SendMessageAPIView, GetChatHistoryAPIView, SendReferAPIView

urlpatterns = [
    path('create-user/', CreateUserAPIView.as_view(), name='create_user_chat'),
    path('history/<str:id>', GetChatHistoryAPIView.as_view(), name='chat-history'),
    path('send-message/<str:id>', SendMessageAPIView.as_view(), name='send_message'),
    path('send-refer/<str:id>', SendReferAPIView.as_view(), name='refer-send')
]
