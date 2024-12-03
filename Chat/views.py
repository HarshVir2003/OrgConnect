from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .roket_chat_helper import create_user, send_message
from django.contrib.auth.models import User


class CreateUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not email or not password:
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a user in Rocket.Chat
        response = create_user(username, email, password)
        if response.get("success"):
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": response.get("error")}, status=status.HTTP_400_BAD_REQUEST)


class SendMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    def post(self, request):
        room_id = request.data.get("room_id")
        message = request.data.get("message")

        if not room_id or not message:
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Send a message to a Rocket.Chat room
        response = send_message(room_id, message)
        if response.get("success"):
            return Response({"message": "Message sent successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": response.get("error")}, status=status.HTTP_400_BAD_REQUEST)
