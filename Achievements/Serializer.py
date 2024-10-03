from rest_framework import serializers
from Achievements.models import Achievements


class AchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievements
        fields = ['title', 'achieved_at', 'Privacy_level']
