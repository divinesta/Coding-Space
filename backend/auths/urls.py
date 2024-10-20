from auths import views as auth_views

from rest_framework_simplejwt.views import TokenRefreshView

from django.urls import path

urlpatterns = [
    path('user/login/', auth_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/register/', auth_views.RegisterAPIView.as_view()),
    path('user/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/forgot-password/<email>/', auth_views.PasswordResetEmailVerifyAPIView.as_view()),
    path('user/password-reset/', auth_views.PasswordResetAPIView.as_view()),
    path('user/password-change/', auth_views.ChangePasswordAPIView.as_view()),
]
