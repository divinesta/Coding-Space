from django.shortcuts import render

from users import models as user_models
from users import serializers as user_serializers

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

import random

# Create your views here.


class RegisterAPIView(generics.CreateAPIView):
    queryset = user_models.User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = user_serializers.RegisterSerializer


# def generate_random_otp(length=7):
#     otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
#     return otp


# class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = user_serializers.UserSerializer

#     def get_object(self):
#         email = self.kwargs['email']

#         user = user_models.User.objects.filter(email=email).first()

#         if user:

#             uuidb64 = user.pk
#             refresh = RefreshToken.for_user(user)
#             refresh_token = str(refresh.access_token)

#             user.refresh_token = refresh_token
#             user.otp = generate_random_otp()
#             user.save()

#             link = f'http://localhost:5173/create-new-password/?otp={
#                 user.otp}&uuidb64={uuidb64}&=refresh_token{refresh_token}'

#             context = {
#                 "link": link,
#                 "username": user.username,
#             }

#             subject = "Password Reset Email"
#             text_body = render_to_string('email/password_reset.txt', context)
#             html_body = render_to_string('email/password_reset.html', context)

#             message = EmailMultiAlternatives(
#                 subject=subject,
#                 from_email=settings.FROM_EMAIL,
#                 to=[user.email],
#                 body=text_body,
#             )

#             message.attach_alternative(html_body, "text/html")
#             message.send()

#             print("Link ===========", link)

#         return user


# class PasswordChangeAPIView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = api_serializers.UserSerializer
#     permission_classes = [AllowAny]

#     def create(self, request, *args, **kwargs):
#         payload = request.data

#         otp = payload['otp']
#         uuidb64 = payload['uuidb64']
#         password = payload['password']

#         user = User.objects.get(id=uuidb64, otp=otp)
#         if user:
#             user.set_password(password)
#             # user.otp = ""
#             user.save()

#             return Response({"message": "Password changed successfully"}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)


# class ChangePasswordAPIView(generics.CreateAPIView):
#     serializer_class = api_serializers.UserSerializer
#     permission_classes = [AllowAny]

#     def create(self, request, *args, **kwargs):
#         user_id = request.data['user_id']

#         old_password = request.data['old_password']
#         new_password = request.data['new_password']

#         user = User.objects.get(id=user_id)
#         if user is not None:
#             if check_password(old_password, user.password):
#                 user.set_password(new_password)
#                 user.save()
#                 return Response({"message": "Password Changed Successfully", "icon": "success"}, status=status.HTTP_200_OK)

#             else:
#                 return Response({"message": "Old Password is Incorrect", "icon": "warning"}, status=status.HTTP_200_OK)

#         else:
#             return Response({"message": "User Not Found", "icon": "error"}, status=status.HTTP_404_NOT_FOUND)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = user_serializers.ProfileSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs['user_id']
        user = user_models.User.objects.get(id=user_id)

        return user_models.Profile.objects.get(user=user)
