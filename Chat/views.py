from drf_yasg.utils import swagger_auto_schema
from pyasn1_modules.rfc3279 import tpBasis
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import json
from .linkbuiilder import get_room_id
from drf_yasg import openapi
from .roket_chat_helper import create_user, send_message, get_chat_history
from django.contrib.auth.models import User


class CreateUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    @swagger_auto_schema(
        operation_summary="NOT FOR USER SIDE"
    )
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

    @swagger_auto_schema(
        operation_summary='Sending messages in a chat Socket',
        operation_description="In this operation we send messages in the socket, get the room id from the group or contact object and forward here.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['message']
        ),
        manual_parameters=[
            openapi.Parameter(
                'id',  # the name of the path parameter
                openapi.IN_PATH,  # location of the parameter (in the path)
                type=openapi.TYPE_STRING,  # define the parameter type as string
                description="A unique string value identifying this user",  # parameter description
                required=True,  # specify that it's required
            )
        ]
    )
    def post(self, request, id: str = None):
        room_id = get_room_id(id)
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

    @swagger_auto_schema(
        operation_summary='Sending referals in a chat Socket',
        operation_description="In this operation we send referals in the socket, get the room id from the group or contact object and forward here.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'link': openapi.Schema(type=openapi.TYPE_STRING),
                'job_at': openapi.Schema(type=openapi.TYPE_STRING),
                'job_des': openapi.Schema(type=openapi.TYPE_STRING),
                'additional_data': openapi.Schema(type=openapi.TYPE_OBJECT)
            },
            required=['message']
        ),
        manual_parameters=[
            openapi.Parameter(
                'id',  # the name of the path parameter
                openapi.IN_PATH,  # location of the parameter (in the path)
                type=openapi.TYPE_STRING,  # define the parameter type as string
                description="A unique string value identifying this user",  # parameter description
                required=True,  # specify that it's required
            )
        ]
    )
    def post(self, request, id=None):
        room_id = get_room_id(id)
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
