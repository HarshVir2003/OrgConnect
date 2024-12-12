import django.contrib.auth.models
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from Achievements.processing import DataBuilder
from Achievements.models import Achievements
from .Serializer import AchievementsSerializer

class AchievementsGet(generics.ListCreateAPIView):
    serializer_class = AchievementsSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']


    def get_queryset(self):
        user_id = self.kwargs.get('id')
        target_user = User.objects.get(id=user_id)
        request_user = self.request.user
        data = DataBuilder(request_user, target_user)
        return data.get_data()

    @swagger_auto_schema(
        operation_summary="get user's Achievements",
        operation_description="enter user id to get there achievements"
    )
    def get(self, request, *args, **kwargs):
        try:
            data = self.get_queryset()
            serializer = self.get_serializer(data, many=True)
            return Response(serializer.data)
        except django.contrib.auth.models.User.DoesNotExist:
            return Response({'message': "User doesn't exists."}, status=status.HTTP_404_NOT_FOUND)


class AchievementsPost(APIView):
    serializer_class = AchievementsSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="posting achievement via valid data",
        operation_summary="POST Achievement here",
        request_body=AchievementsSerializer
    )
    def post(self, request):
        serializer = AchievementsSerializer(data=request.data)
        if serializer.is_valid():
            if Achievements.objects.filter(title=request.data['title'], achieved_at=request.data['achieved_at'],
                                           Privacy_level=request.data['Privacy_level'], user_id=request.user).exists():
                return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
            serializer.save(user_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


    @swagger_auto_schema(
        operation_summary="Update an existing post",
        operation_description='only the privacy levels, enter the achievement object id and level change value',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'Privacy_level': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['Privacy_level']
        )
    )
    def put(self, request, id=None):
        try:
            achievement = Achievements.objects.get(user_id=request.user, id=id)
        except Achievements.DoesNotExist:
            return Response({'message': 'Achievement does not exists'}, status=status.HTTP_404_NOT_FOUND)

        if len(request.data) > 1:
            return Response({'message': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)
        if request.data['Privacy_level'] and int(request.data['Privacy_level']) in [0, 1, 2]:
            privacy_level = request.data['Privacy_level']
        else:
            privacy_level = None

        if privacy_level is not None:
            achievement.Privacy_level = privacy_level
            achievement.save()
            return Response({'message': 'Achievement updated'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': "privacy level is None"}, status=status.HTTP_400_BAD_REQUEST)



    @swagger_auto_schema(
        operation_summary="Delete an existing achievement",
        operation_description='delete the achievement using the id of the post',

    )
    def delete(self, request, id=None):
        try:
            achievement = Achievements.objects.get(user_id=request.user, id=id)
        except Achievements.DoesNotExist:
            return Response({'message': 'Achievement doesnot exist'}, status=status.HTTP_404_NOT_FOUND)

        achievement.delete()
        return Response({'message': 'Achievement deleted successfully'}, status=status.HTTP_200_OK)
