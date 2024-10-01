from users import views as user_views
from django.urls import path

urlpatterns = [
    path('user/register/', user_views.RegisterAPIView.as_view()),
    path('user/profile/<user_id>/', user_views.ProfileAPIView.as_view()),
]
