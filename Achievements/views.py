from Achievements.Serializer import AchievementsSerializer
from rest_framework import generics


class Achievements(generics.ListCreateAPIView):
    serializer_class = AchievementsSerializer

