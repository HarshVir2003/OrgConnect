from rest_framework import serializers

from Groups.models import Contacts, Group, Community
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name', 'profile_img', 'members', 'chat_url', 'community']

    chat_url = serializers.CharField(allow_null=True, required=False)

class ContactsSerializer(ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['id','user', 'friend', 'chat_url']

    chat_url = serializers.CharField(allow_null=True, required=False)

class CommunitySerializer(ModelSerializer):
    class Meta:
        model = Community
        fields = ['id','name', 'description', 'profile_img', 'admins']


class MemberSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'id']
