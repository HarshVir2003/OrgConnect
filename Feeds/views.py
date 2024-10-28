from django.shortcuts import render
from django.contrib.auth.models import User
from Feeds.models import Posts, Likes, Comments
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from Feeds.Serializer import CommentsSerializers, LikesSerializers, PostsSerializer
from Feeds.processing import DataBuilder


class FeedView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostsSerializer
    http_method_names = ['get']

    def get_queryset(self):
        data = DataBuilder(self.request.user)
        return data.get_data()

    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)

