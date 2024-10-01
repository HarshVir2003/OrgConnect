from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from User.Serializer import UserSerializer, UserRegistrationSerializer
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
            return Response({"message": "User Registered Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    pass

# Can be Use to Destroy or update data
# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         return User.objects.filter(id=self.request.user.id)
