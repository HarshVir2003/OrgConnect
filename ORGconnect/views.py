import json

import requests
from allauth.account.views import login
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from social_django.utils import psa
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User



class PasswordResetConfirmView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

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
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                reverse('password-reset-confirm', kwargs={'uidb64': uid, 'token': token}))

            # Send the email
            send_mail(
                subject='Password Reset Request',
                message=f'Front end-point to be provided. refer docs for details.',
                from_email='orgconnectdotorg@gmail.com',
                recipient_list=[email],
            )
            return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt  # Disable CSRF protection for testing purposes (not recommended in production)
def google_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            id_token = data.get('id_token')

            # Verify the token and get user info from Google
            url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=" + id_token
            response = requests.get(url)
            if response.status_code == 200:
                user_info = response.json()
                email = user_info.get('email')
                first_name = user_info.get('given_name')
                last_name = user_info.get('family_name')  # This may or may not be available
                picture = user_info.get('picture')

                # # Print user info for debugging
                # print(user_info)

                # Check if the user already exists
                user = User.objects.filter(email=email).first()

                if not user:
                    # Create a new user, use last_name if available
                    if last_name:
                        user = User.objects.create_user(
                            username=email,
                            email=email,
                            first_name=first_name,
                            last_name=last_name
                        )
                    else:
                        # If last_name is not provided, create user without it
                        user = User.objects.create_user(
                            username=email,
                            email=email,
                            first_name=first_name
                        )

                # Log the user in
                login(request, user)

                return JsonResponse({"message": "User logged in successfully"}, status=200)

            return JsonResponse({"error": "Invalid token"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid method"}, status=405)

