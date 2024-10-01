from users import views as user_views
from django.urls import path

urlpatterns = [
    path('user/token/', user_views.MyTokenObtainPairView.as_view()),
    path('user/register/', user_views.RegisterAPIView.as_view()),
    path('user/profile/<user_id>/', user_views.ProfileAPIView.as_view()),
    path('user/password-reset/<email>/', user_views.PasswordResetEmailVerifyAPIView.as_view()),
    path('user/password-reset/', user_views.PasswordResetAPIView.as_view()),
    path('user/password-change/', user_views.ChangePasswordAPIView.as_view()),
]
