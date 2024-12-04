"""
URL configuration for ORGconnect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconfADMIN_USER_ID
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import PasswordResetConfirmView, PasswordResetRequestView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('User.urls')),
    path('JobUpdates/', include('JobUpdates.urls')),
    path('achievement/', include('Achievements.urls')),
    path('groups/', include('Groups.urls')),
    path('portfolio/', include('Portfolio.urls')),
    path('feeds/', include('Feeds.urls')),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('chat/', include('Chat.urls'))
]
