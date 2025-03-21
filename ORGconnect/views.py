from drf_yasg import openapi
from dj_rest_auth.registration.views import  SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decouple import config
from django.contrib.auth.models import User


ROCKET_CHAT_URL = config('ROCKET_URL')


class PasswordResetConfirmView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    @swagger_auto_schema(
        operation_summary='Password reset confirm page.',
        operation_description='send in the password',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'password': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['password']
        )

    )
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            token_generator = PasswordResetTokenGenerator()

            if token_generator.check_token(user, token):
                new_password = request.data.get('password')
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        except (User.DoesNotExist, ValueError):
            return Response({'error': 'Invalid user or token.'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    @swagger_auto_schema(
        operation_summary='Password reset request page.',
        operation_description='send in the email',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['email']
        )

    )
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # reset_url = request.build_absolute_uri(
            #     reverse('password-reset-confirm', kwargs={'uidb64': uid, 'token': token}))
            reset_url = f'localhost:3000/{uid}/{token}/'

            # Send the email
            send_mail(
                subject='Password Reset Request',
                message=f'click to change password \n {reset_url} \n tan q.',
                from_email='orgconnectdotorg@gmail.com',
                recipient_list=[email],
            )
            return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
