from django.shortcuts import render
from django.apps import apps

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Course, CourseEnrollment
from .serializers import CourseSerializer, AssessmentSerializer, CodingAreaSerializer, QuizSerializer, PlayGroundSerializer


# Create your views here.
class CoursesAPIView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]


    def get_queryset(self):
        institution_id = self.kwargs['institution_id']
        institution = apps.get_model('users', 'Institution')

        institute = institution.objects.get(id=institution_id)

        queryset = Course.objects.filter(institution=institute)

        return queryset

# class EnrollmentAPIView(generics.CreateAPIView):
#     serializer_class = CourseEnrollmentSerializer
#     permission_classes = [AllowAny]


