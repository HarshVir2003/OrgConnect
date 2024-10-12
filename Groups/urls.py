from django.urls import path
from Groups.views import vv

urlpatterns = [
    path('', vv, name='jobUpdates')]
