from django.shortcuts import render, HttpResponse
from Groups.models import Community, Group, Contacts
from Groups.serializer import GroupSerializer, ContactsSerializer, CommunitySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from urllib.parse import quote


# Create your views here.
# todo: create a view for getting group members and write tests for it
class MembersView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]


class GroupsView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer

    def get_queryset(self):
        return Group.objects.filter(members=self.request.user)

    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            if Group.objects.filter(name=request.data['name'], community=request.data['community']).exists():
                return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


class CommunityView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommunitySerializer

    def get_queryset(self):
        return Community.objects.filter(admins=self.request.user)

    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CommunitySerializer(data=request.data)
        if serializer.is_valid():
            if Community.objects.filter(name=request.data['name'], admins=request.user,
                                        description=request.data['description'],
                                        profile_img=request.data['profile_img']).exists():
                return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('data not valid')
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


class ContactView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactsSerializer

    def get_queryset(self):
        return Contacts.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ContactsSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            friend = serializer.validated_data.get('friend')
            usernames = sorted([user.username, friend.username])
            user_encoded = quote(usernames[0])
            friend_enocded = quote(usernames[1])
            chat_url = f'test.com/{user_encoded}/{friend_enocded}'
            contact = Contacts.objects.create(user=user, friend=friend, chat_url=chat_url)
            return Response(ContactsSerializer(contact).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
