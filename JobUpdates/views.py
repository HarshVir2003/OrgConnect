from django.urls import reverse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import redirect
from JobUpdates.models import JobUpdates
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .serializer import JobUpdatesSerializer


# Create your views here.

class JobUpdatesView(ListAPIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    queryset = JobUpdates.objects.all()
    serializer_class = JobUpdatesSerializer


class JobPosting(APIView):
    permission_classes = [IsAdminUser]

    # def get(self, request, *args, **kwargs):
    #     serializer = JobUpdatesSerializer()
    #     return Response(serializer.data)
    @swagger_auto_schema(operation_summary="Posting Job updates",
                         operation_description="only for developer side dont give user's access",
                         request_body=JobUpdatesSerializer)
    def post(self, request, *args, **kwargs):
        serializer = JobUpdatesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect(reverse('jobUpdates'))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
