from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User

from Groups.models import Community, Group, Contacts
from Groups.serializer import GroupSerializer, ContactsSerializer, CommunitySerializer, MemberSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from urllib.parse import quote


# Create your views here.
# todo: create a view for getting group members and write tests for it
class MembersView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MemberSerializer

    def get(self, request, id: int | None = None) -> Response:
        if id is None:
            return Response({'message': 'No id provided!'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            group = Group.objects.get(id=id)
            community = Community.objects.get(id=group.community.id)
            if not community.admins.filter(id=request.user.id).exists():
                return Response({'message': 'not Authorised'}, status=status.HTTP_403_FORBIDDEN)

            members = group.members.all()
            serializer = self.serializer_class(members, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({'message': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id: int | None = None) -> Response:
        try:
            group = Group.objects.get(id=id)
            community = Community.objects.get(id=group.community.id)
            if not community.admins.filter(id=request.user.id).exists():
                return Response({'message': 'not Authorised'}, status=status.HTTP_403_FORBIDDEN)
            username = request.data.get('username')
            if username:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

            if user not in group.members.all():
                group.members.add(user)
                return Response({'message': f'{user.username} added to the group'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'User is already a member of this group'},
                                status=status.HTTP_400_BAD_REQUEST)

        except Group.DoesNotExist:
            return Response({'message': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id: int | None = None) -> Response:
        try:
            group = Group.objects.get(id=id)
            community = Community.objects.get(id=group.community.id)
            if not community.admins.filter(id=request.user.id).exists():
                return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

            username = request.data.get('username')
            if username:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

            if user in group.members.all():
                group.members.remove(user)
                return Response({'message': f'{user.username} removed from the group'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'User is not a member of this group'}, status=status.HTTP_400_BAD_REQUEST)

        except Group.DoesNotExist:
            return Response({'message': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)


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
