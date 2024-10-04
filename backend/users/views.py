from django.apps import apps

from users import models as user_models
from users import serializers as user_serializers

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


def get_serializer(app_label, serializer_name):
    app_config = apps.get_app_config(app_label)
    module = app_config.module
    serializers_module = getattr(module, 'serializers', None)

    if serializers_module is None:
        raise ImportError(f"Could not find serializers module in {app_label}")

    serializer = getattr(serializers_module, serializer_name, None)

    if serializer is None:
        raise AttributeError(f"Could not find serializer {serializer_name} in {app_label}.serializers")

    return serializer

CourseSerializer = get_serializer('assessments', 'CourseSerializer')
Course = apps.get_model('assessments', 'Course')


class InstitutionListAPIView(generics.ListAPIView):
    queryset = user_models.Institution.objects.all()
    serializer_class = user_serializers.InstitutionSerializer
    permission_classes = [AllowAny]

class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = user_serializers.ProfileSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs['user_id']
        user = user_models.User.objects.get(id=user_id)

        return user_models.Profile.objects.get(user=user)
    

class StudentListAPIview(generics.ListAPIView):
    serializer_class = user_serializers.StudentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = user_models.User.objects.get(id=user_id)

        return user_models.Student.objects.get(user=user)

    
class TeacherCourseAPIView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = user_models.Teacher.objects.get(id=teacher_id)

        return Course.objects.filter(teacher=teacher)

    # def get_queryset(self):
    #     user_id = self.kwargs['user_id']
    #     user = user_models.User.objects.get(id=user_id)

    #     return user_models.Student.objects.filter(user=user)