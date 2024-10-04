from auths import views as auth_views

from django.urls import path

urlpatterns = [
    path('user/token/', auth_views.MyTokenObtainPairView.as_view()),
    path('user/register/', auth_views.RegisterAPIView.as_view()),
    path('user/password-reset/<email>/', auth_views.PasswordResetEmailVerifyAPIView.as_view()),
    path('user/password-reset/', auth_views.PasswordResetAPIView.as_view()),
    path('user/password-change/', auth_views.ChangePasswordAPIView.as_view()),
]
