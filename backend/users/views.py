from django.shortcuts import render
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from users import models as user_models
from users import serializers as user_serializers

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

import random
from urllib.parse import urlencode

# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = user_serializers.MyTokenObtainPairSerializer

class RegisterAPIView(generics.CreateAPIView):
    queryset = user_models.User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = user_serializers.RegisterSerializer


def generate_random_otp(length=7):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = user_serializers.UserSerializer

    def get_object(self):
        email = self.kwargs['email']

        user = user_models.User.objects.filter(email=email).first()

        if user:

            uuidb64 = user.pk
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh.access_token)

            user.refresh_token = refresh_token
            user.otp = generate_random_otp()
            user.save()

            base_url = settings.FRONTEND_SITE_URL + "/create-new-password/"

            query_params = urlencode({
                "otp": user.otp,
                "uuidb64": uuidb64,
                "refresh_token": refresh_token,
            })

            link = f'{base_url}?{query_params}'

            context = {
                "link": link,
                "username": user.username,
            }

            subject = "Password Reset Email"
            text_body = render_to_string('email/password_reset.txt', context)
            html_body = render_to_string('email/password_reset.html', context)

            message = EmailMultiAlternatives(
                subject=subject,
                from_email=settings.FROM_EMAIL,
                to=[user.email],
                body=text_body,
            )

            message.attach_alternative(html_body, "text/html")
            message.send()

            # print("Link ===========", link)

        return user

User = get_user_model()

class PasswordResetAPIView(generics.UpdateAPIView):
    serializer_class = user_serializers.PasswordResetSerializer
    permission_classes = []

    def get_object(self):
        return User.objects.get(
            id=self.request.data.get('uuidb64'),
            otp=self.request.data.get('otp')
        )

    def update(self, request, *args, **kwargs):
        try:
            user = self.get_object()
        except User.DoesNotExist:
            return Response({"message": "Invalid reset token"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.otp = None  # Clear the OTP after use
            user.save()
            return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordAPIView(generics.UpdateAPIView):
    serializer_class = user_serializers.PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"message": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = user_serializers.ProfileSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs['user_id']
        user = user_models.User.objects.get(id=user_id)

        return user_models.Profile.objects.get(user=user)
