from allauth.account.internal.decorators import login_stage_required
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
import json
from User.Serializer import UserSerializer, UserRegistrationSerializer, UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from django.urls import reverse
import requests
from drf_yasg.utils import swagger_auto_schema
from decouple import config
from Chat.roket_chat_helper import create_user
from rest_framework.parsers import MultiPartParser, FormParser

ROCKET_CHAT_URL = config('ROCKET_URL')


@swagger_auto_schema(
    operation_summary='Get profile of user.',
    operation_description='Get profile of a given user, given the ID of the user.',
)
class UserList(generics.RetrieveAPIView):
    http_method_names = ['get']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class UserRegister(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['post']
    parser_classes = [MultiPartParser, FormParser]

    # def get(self, request, *args, **kwargs):
    #     serializer = UserRegistrationSerializer()
    #     if request.user.is_authenticated:
    #         url = reverse('User', kwargs={'id': request.user.id})
    #         return redirect(url)
    #     return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary='POST User Register',
        operation_description='User Registration endpoint.',
        request_body=UserRegistrationSerializer
    )

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            User_object = User.objects.filter(username=request.data['username']).exists()
            email_exists = User.objects.filter(email=request.data['email']).exists()
            if request.data['username']:
                if not User_object and not email_exists:
                    serializer.save()
                    user = authenticate(username=request.data['username'], password=request.data['password'])
                    login(request, user)

                    # register user for chat app
                    # url = f'{ROCKET_CHAT_URL}/chat/create-user'
                    # requests.post(url, json={'username': request.data['username'], 'email': request.data['email'],
                    #                          'password': request.data['username'] + "@orgconnect.org"})
                    create_user(
                        name=request.data['username'],
                        username=request.data['username'],
                        email=request.data['email'],
                        password=request.data['username'] + "@orgconnect.org"
                    )
                    # redirect to user profile page
                    return Response({'message': 'Logged in.'}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Already Registered."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Provide a valid Username.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['post']

    # def get(self, request, *args, **kwargs):
    #     serializer = UserLoginSerializer()
    #     if request.user.is_authenticated:
    #         url = reverse('User', kwargs={'id': request.user.id})
    #         return redirect(url)
    #     return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary='POST Login.',
        request_body=UserLoginSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=request.data['username'], password=request.data['password'])
            if user is not None:
                login(request, user)
            else:
                return Response({'message': "Wrong username or password!"}, status=status.HTTP_401_UNAUTHORIZED)

            if request.user.is_authenticated:
                # temp redirect to profile
                return Response({'message': 'logged in.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='GET Logout',
        operation_description='Logout user by passing request object.',
        responses={200: 'logged out successfully'}
    )
    def get(self, request):
        logout(request)
        return Response({'message': 'logged out successfully'}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='GET current user\'s id.',
        responses={200: 'user is logged in.', 401: 'user not authenticated.'}
    )
    def get(self, request):
        if request.user.is_authenticated:
            return Response({'user-id': request.user.id}, status=status.HTTP_200_OK)




