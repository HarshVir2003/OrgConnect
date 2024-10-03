from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from User.Serializer import UserSerializer, UserRegistrationSerializer, UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from django.urls import reverse


class UserList(generics.RetrieveAPIView):
    http_method_names = ['get']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class UserRegister(APIView):
    permission_classes = [AllowAny]

    # todo: remove in final version
    def get(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer()
        if request.user.is_authenticated:
            url = reverse('User', kwargs={'id': request.user.id})
            return redirect(url)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = authenticate(username=request.data['username'], password=request.data['password'])
            login(request, user)
            url = reverse('User', kwargs={'id': request.user.id})
            return redirect(url)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = [AllowAny]

    # todo: remove in final version
    def get(self, request, *args, **kwargs):
        serializer = UserLoginSerializer()
        if request.user.is_authenticated:
            url = reverse('User', kwargs={'id': request.user.id})
            return redirect(url)
        return Response(serializer.data)

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
                url = reverse('User', kwargs={'id': request.user.id})
                return redirect(url)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def logout_user(request):
    logout(request)
    # temp redirect to login
    return redirect(reverse('login'))


def profile_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('User', kwargs={'id': request.user.id}))
    return redirect(reverse('User', kwargs={'id': 1}))
