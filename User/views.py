from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from User.Serializer import UserSerializer


# Create your views here.
class UserList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

# Can be Use to Destroy or update data
# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         return User.objects.filter(id=self.request.user.id)
