from django.urls import path
from Achievements.views import Achievements, AchievementsPost

urlpatterns = [
    path('<int:id>/', Achievements.as_view(), name='getAchievement'),
    path('post/', AchievementsPost.as_view(), name='postAchievement')
]