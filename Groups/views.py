from django.shortcuts import render, HttpResponse
from Groups.models import Community, Group, Contacts
from Groups.serializer import GroupSerializer, ContactsSerializer, CommunitySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

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
