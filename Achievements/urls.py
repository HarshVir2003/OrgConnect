from django.urls import path
from Achievements.views import AchievementsGet, AchievementsPost

urlpatterns = [
    path('<int:id>/', AchievementsGet.as_view(), name='getAchievement'),
    path('post/', AchievementsPost.as_view(), name='postAchievement')
]
