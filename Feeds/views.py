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
# Create your views here.

