from django.apps import apps
from importlib import import_module

from rest_framework import serializers

from .models import User, Profile, Teacher, Student, Institution


def get_serializer(app_label, serializer_name):
    try:
        module = import_module(f"{app_label}.serializers")
        serializer = getattr(module, serializer_name, None)

        if serializer is None:
            raise AttributeError(f"Could not find serializer {serializer_name} in {app_label}.serializers")

        return serializer
    except ImportError:
        raise ImportError(
            f"Could not import serializers module from {app_label}")


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        models = Institution
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(StudentSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class TeacherSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True)

    CourseSerializer = get_serializer('assessments', 'CourseSerializer')
    courses = CourseSerializer(many=True)

    CourseEnrollmentSerializer = get_serializer('assessments', 'CourseEnrollmentSerializer')
    EnrolledStudents = CourseEnrollmentSerializer(many=True)

    class Meta:
        model = Teacher
        fields = '__all__'
