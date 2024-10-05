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
    lookup_field = 'id'

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        target_user = User.objects.get(id=user_id)
        request_user = self.request.user
        data = DataBuilder(request_user, target_user)
        return data.get_data()

    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)


# todo : application of data updation
class AchievementsPost(APIView):
    serializer_class = AchievementsSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AchievementsSerializer(
            data=request.data)
        if serializer.is_valid():
            if Achievements.objects.filter(title=request.data['title'], achieved_at=request.data['achieved_at'],
                                        Privacy_level=request.data['Privacy_level'], user_id=request.user).exists():
                return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
            serializer.save(user_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
