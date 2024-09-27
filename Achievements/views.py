from Achievements.models import Achievements
from Achievements.Serializer import AchievementsSerializer
from rest_framework import generics


# Create your views here.
class Achievements(generics.ListCreateAPIView):
    serializer_class = AchievementsSerializer

