from django.shortcuts import render
from django.urls import reverse
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.shortcuts import redirect
from JobUpdates.models import JobUpdates
from rest_framework import status
from JobUpdates.serializer import JobUpdatesSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView


# Create your views here.

class JobUpdatesView(ListAPIView):
    http_method_names = ['get']
    queryset = JobUpdates.objects.all()
    serializer_class = JobUpdatesSerializer


class JobPosting(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        serializer = JobUpdatesSerializer()
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = JobUpdatesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect(reverse('jobUpdates'))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
