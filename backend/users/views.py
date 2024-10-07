from django.shortcuts import get_object_or_404

from . import models as user_models
from . import serializers as user_serializers

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response



# def get_serializer(app_label, serializer_name):
#     app_config = apps.get_app_config(app_label)
#     module = app_config.module
#     serializers_module = getattr(module, 'serializers', None)

#     if serializers_module is None:
#         raise ImportError(f"Could not find serializers module in {app_label}")

#     serializer = getattr(serializers_module, serializer_name, None)

#     if serializer is None:
#         raise AttributeError(f"Could not find serializer {serializer_name} in {app_label}.serializers")

#     return serializer

# CourseSerializer = get_serializer('assessments', 'CourseSerializer')


class InstitutionListAPIView(generics.ListAPIView):
    queryset = user_models.Institution.objects.all()
    serializer_class = user_serializers.InstitutionSerializer
    permission_classes = [AllowAny]


class StudentProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = user_serializers.StudentSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs['user_id']
        student = get_object_or_404(user_models.Student, user__id=user_id)
        return student
        # user = user_models.User.objects.get(id=user_id)

        # return user_models.Student.objects.get(user=user)

class TeacherProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = user_serializers.TeacherSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs['user_id']
        teacher = get_object_or_404(user_models.Teacher, user__id=user_id)
        return teacher

#FIXME: fix this view
class TeacherListAPIView(generics.ListAPIView):
    serializer_class = user_serializers.InstitutionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        institution_id = self.kwargs['institution_id']
        institution = user_models.Institution.objects.get(id=institution_id)

        return user_models.Teacher.objects.filter(user__institution=institution)

class TeacherCourseListAPIView(generics.ListCreateAPIView):
    serializer_class = user_serializers.CourseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = user_models.Teacher.objects.get(id=teacher_id)

        return user_models.Course.objects.filter(teacher=teacher)
    
class TeacherCourseDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = user_serializers.CourseSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        teacher_id = self.kwargs['teacher_id']
        course_id = self.kwargs['course_id']
        
        teacher = user_models.Teacher.objects.get(id=teacher_id)
        return get_object_or_404(user_models.Course, teacher=teacher, course_id=course_id)


class TeacherCourseCreateAPIView(generics.CreateAPIView):
    serializer_class = user_serializers.CourseSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        institution = request.data['institution']
        teacher = request.data['teacher']
        title = request.data['title']

        institution = user_models.Institution.objects.get(name=institution)
        teacher = user_models.Teacher.objects.get(user__username=teacher)

        user_models.Course.objects.create(institution=institution, teacher=teacher, title=title)

        return Response({"message": "Course created successfully"},status=status.HTTP_201_CREATED)
    

class TeacherStudentListAPIView(generics.ListAPIView):
    serializer_class = user_serializers.CourseEnrollmentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        course_id = self.kwargs['course_id']

        teacher = user_models.Teacher.objects.get(id=teacher_id)
        course = user_models.Course.objects.get(course_id=course_id)

        return user_models.CourseEnrollment.objects.filter(teacher=teacher, course=course)

    # def get_queryset(self):
    #     user_id = self.kwargs['user_id']
    #     user = user_models.User.objects.get(id=user_id)

    #     return user_models.Student.objects.filter(user=user)

class TeacherAssessmentCreateAPIView(generics.CreateAPIView):
    serializer_class = user_serializers.AssessmentSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        course_id = request.data['course_id']
        title = request.data['title']
        description = request.data['description']
        due_date = request.data['due_date']

        # Get the course object
        course = get_object_or_404(user_models.Course, course_id=course_id)

        user_models.Assessment.objects.create(
            course=course,
            title=title, 
            description=description, 
            due_date=due_date
        )

        return Response({"message": "Assessment created successfully"}, status=status.HTTP_201_CREATED)

class TeacherAssessmentListAPIView(generics.ListAPIView):
    serializer_class = user_serializers.AssessmentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        course_id = self.kwargs['course_id']

        course = user_models.Course.objects.get(course_id=course_id)

        return user_models.Assessment.objects.filter(course=course)


class TeacherQuizCreateAPIView(generics.CreateAPIView):
    serializer_class = user_serializers.QuizSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        course_id = request.data['course_id']
        title = request.data['title']
        description = request.data['description']
        time_limit = request.data['time_limit']  # This is optional

        # Get the course object
        course = get_object_or_404(user_models.Course, course_id=course_id)

        quiz = user_models.Quiz.objects.create(
            course=course,
            title=title,
            description=description,
            time_limit=time_limit
        )

        return Response({"message": "Quiz created successfully", "quiz_id": quiz.quiz_id}, status=status.HTTP_201_CREATED)


class TeacherQuizListAPIView(generics.ListAPIView):
    serializer_class = user_serializers.QuizSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = user_models.Course.objects.get(course_id=course_id)
        return user_models.Quiz.objects.filter(course=course)

class EnrollStudentsAPIView(generics.CreateAPIView):
    serializer_class = user_serializers.CourseEnrollmentSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        student_id = request.data['student_id']
        teacher_id = request.data['teacher_id']
        course_id = request.data['course_id']
        enrollment_code = request.data['enrollment_code']

        # Validate the enrollment code
        try:
            course = user_models.Course.objects.get(
                course_id=course_id, enrollment_code=enrollment_code)
        except user_models.Course.DoesNotExist:
            return Response({"message": "Invalid enrollment code"}, status=status.HTTP_400_BAD_REQUEST)

        if enrollment_code is None:
            return Response({"message": "Enrollment code is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the student is already enrolled
        student = get_object_or_404(user_models.Student, id=student_id)
        if user_models.CourseEnrollment.objects.filter(course=course, student=student).exists():
            return Response({"message": "You are already enrolled in this course."}, status=status.HTTP_400_BAD_REQUEST)
        
        teacher = get_object_or_404(user_models.Teacher, id=teacher_id)

        # Enroll the student
        user_models.CourseEnrollment.objects.create(
            course=course, student=student, teacher=teacher, is_enrolled=True)

        return Response({"message": "Course enrolled successfully."}, status=status.HTTP_201_CREATED)

class StudentCourseAPIView(generics.ListAPIView):
    serializer_class = user_serializers.CourseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        student = user_models.Student.objects.get(id=student_id)

        return user_models.Course.objects.filter(students=student)



# class StudentCourseDetailAPIView(generics.RetrieveAPIView):
#     serializer_class = user_serializers.CourseSerializer
#     permission_classes = [AllowAny]

#     def get_object(self):
#         student_id = self.kwargs['student_id']
#         student = user_models.Student.objects.get(id=student_id)

#         course_id = self.kwargs['course_id']
#         course = user_models.Course.objects.get(id=course_id)

#         return user_models.Enrollment.objects.filter(students=student, course=course)
