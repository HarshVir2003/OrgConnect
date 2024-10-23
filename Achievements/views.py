import django.contrib.auth.models

from Achievements.Serializer import AchievementsSerializer
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from Achievements.processing import DataBuilder
from Achievements.models import Achievements


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

    def get(self, request, *args, **kwargs):
        try:
            data = self.get_queryset()
            serializer = self.get_serializer(data, many=True)
            return Response(serializer.data)
        except django.contrib.auth.models.User.DoesNotExist:
            return Response({'message': "User doesn't exists."}, status=status.HTTP_404_NOT_FOUND)


# todo: application of data updation
class AchievementsPost(APIView):
    serializer_class = AchievementsSerializer
    permission_classes = [IsAuthenticated]

    # todo: remove it later
    def get(self, request):
        return Response({'id': Achievements.objects.filter(user_id=request.user)[0].id})

    def post(self, request):
        serializer = AchievementsSerializer(data=request.data)
        if serializer.is_valid():
            if Achievements.objects.filter(title=request.data['title'], achieved_at=request.data['achieved_at'],
                                           Privacy_level=request.data['Privacy_level'], user_id=request.user).exists():
                return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
            serializer.save(user_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    # todo: requires a token id not in url but in request
    def put(self, request):
        try:
            achievement = Achievements.objects.get(user_id=request.user, id=request.data['id'])
        except Achievements.DoesNotExist:
            return Response({'message': 'Achievement does not exists'}, status=status.HTTP_404_NOT_FOUND)

        if len(request.data) > 2:
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

    def delete(self, request):
        try:
            achievement = Achievements.objects.get(user_id=request.user, id=request.data['id'])
        except Achievements.DoesNotExist:
            return Response({'message': 'Achievement doesnot exist'}, status=status.HTTP_404_NOT_FOUND)

        achievement.delete()
        return Response({'message': 'Achievement deleted successfully'}, status=status.HTTP_200_OK)
