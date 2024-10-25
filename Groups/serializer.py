from Groups.models import Contacts, Group, Community
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'profile_img', 'members', 'chat_url', 'community']


class ContactsSerializer(ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['user', 'friend', 'chat_url']


class CommunitySerializer(ModelSerializer):
    class Meta:
        model = Community
        fields = ['name', 'description', 'profile_img', 'admins']


class MemberSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'id']
