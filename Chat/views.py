from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import json
from .linkbuiilder import get_room_id

from .roket_chat_helper import create_user, send_message, get_chat_history
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

    def post(self, request, id=None):
        room_id = id
        message = request.data.get("message")

        if not room_id or not message:
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Send a message to a Rocket.Chat room
        response = send_message(room_id, message)
        if response.get("success"):
            return Response({"message": "Message sent successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": response.get("error")}, status=status.HTTP_400_BAD_REQUEST)


class SendReferAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        room_id = id
        link = request.data.get('link')
        job_at = request.data.get('job_at')
        job_des = request.data.get('job_des')
        additional_data = request.data.get('data')

        if not room_id or not (link and job_at and job_des):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare the message as a dictionary
        message_content = {
            "link": link,
            "job_at": job_at,
            "job_description": job_des,
            "additional_data": additional_data,
        }

        # Serialize the message to JSON
        serialized_message = json.dumps(message_content)

        # Send the message to the Rocket.Chat room
        response = send_message(room_id, serialized_message)  # Assume send_message is defined elsewhere
        if response.get("success"):
            return Response({"message": "Message sent successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": response.get("error")}, status=status.HTTP_400_BAD_REQUEST)


class GetChatHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get(self, request, id=None):
        """
        Retrieve chat history from Rocket.Chat.
        """
        room_id = get_room_id(id)  # enter name here
        count = request.query_params.get("count", 50)

        if not room_id:
            return Response({"error": "room_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate count parameter
        try:
            count = int(count)
        except ValueError:
            return Response({"error": "count must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch chat history
        history = get_chat_history(room_id, count)

        if "error" in history:
            return Response(history["error"], status=status.HTTP_400_BAD_REQUEST)

        return Response(history, status=status.HTTP_200_OK)
