from rest_framework.views import APIView
from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from Groups.models import Community, Group, Contacts
from Groups.serializer import ContactsSerializer, CommunitySerializer, MemberSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from Groups.serializer import GroupSerializer
from Groups.serializer import GroupDeleteSerializer, CommunityDeleteSerializer, ContactDeleteSerializer


# Create your views here.
class MembersView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MemberSerializer
    http_method_names = ['get', 'post', 'delete']

    @swagger_auto_schema(
        operation_summary='Getting all members of the groups.',
        operation_description='pass in the id of the group for which, we want the members list.',

    )
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

    @swagger_auto_schema(
        operation_summary='Add user to the group.',
        operation_description='pass in the username of the person to be added in the group, pass in the group id in the path.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
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

    @swagger_auto_schema(
        operation_summary='Delete the user form the group.',
        operation_description='pass in the id for the group in the path and pass in the username as json.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
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
    http_method_names = ['get', 'post', 'del']

    def get_queryset(self):
        return Group.objects.filter(members=self.request.user)

    @swagger_auto_schema(
        operation_summary='Get the groups list which use is part of.',
        operation_description="No parameter's required for this one",
    )
    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary='Create the group.',
        operation_description="pass in all the data for the group you want to make.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'profile_img': openapi.Schema(type=openapi.TYPE_FILE),
                'members': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER)
                ),
                'community': openapi.Schema(type=openapi.TYPE_INTEGER, description="community's id")

            }
        )

    )
    def post(self, request, *args, **kwargs):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            if Group.objects.filter(name=request.data['name'], community=request.data['community']).exists():
                return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        serializer = GroupDeleteSerializer(data=request.data)
        if serializer.is_valid():
            if Group.objects.filter(name=request.data.get('group_name'),
                                    community=request.data.get('community_name')).exists():
                Group.objects.filter(name=request.data.get('group_name'),
                                     community=request.data.get('community_name')).delete()
                return Response({"message": 'Group delete successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'Group not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Group not found.'}, status=status.HTTP_404_NOT_FOUND)


class CommunityView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommunitySerializer

    def get_queryset(self):
        return Community.objects.filter(admins=self.request.user)

    @swagger_auto_schema(
        operation_summary="Get all the community's user is admin of.",
        operation_description='only get the communities which user is admin of as for the one user is member of, get that object id from the group.'

    )
    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary='This is used to create communities.',
        operation_description='Here we can create a community.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'profile_img': openapi.Schema(type=openapi.TYPE_FILE),
                'admins': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER)
                ),
                'description': openapi.Schema(type=openapi.TYPE_STRING)

            }
        )
    )
    def post(self, request, *args, **kwargs):
        serializer = CommunitySerializer(data=request.data)
        if serializer.is_valid():
            if Community.objects.filter(name=request.data['name'], admins=request.user,
                                        description=request.data['description'],
                                        profile_img=request.data['profile_img']).exists():
                return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        serializer = CommunityDeleteSerializer(data=request.data)
        if serializer.is_valid():
            if Community.objects.filter(name=request.data.get('name')).exists():
                Community.objects.filter(name=request.data.get('name')).delete()
                return Response({'message': 'Successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


class ContactView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactsSerializer

    def get_queryset(self):
        return Contacts.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_summary='this is used to get all the friends of the user.',
        operation_description='this port return all the friends user had added to his account.',

    )
    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary='this is used add friend to user account.',
        operation_description='this port create a object in which user and friend id described in a relation',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(type=openapi.TYPE_INTEGER),
                'friend': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['user', 'friend']

        )

    )
    def post(self, request, *args, **kwargs):
        serializer = ContactsSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            friend = serializer.validated_data.get('friend')
            contact = Contacts.objects.create(user=user, friend=friend)
            return Response(ContactsSerializer(contact).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        serializer = ContactDeleteSerializer(data=request.data)
        if serializer.is_valid():
            if Contacts.objects.filter(user=request.user, friend=request.data.get('friend')).exists():
                Contacts.objects.filter(user=request.user, friend=request.data.get('friend')).delete()
                return Response({"message": "Successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


class CommunityIdView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommunitySerializer
    queryset = Community.objects.all()
    lookup_field = 'id'
