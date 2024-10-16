from django.shortcuts import get_object_or_404

from ..models import Teacher, Course, CourseEnrollment, Assessment, Submission, Institution, Student, Quiz
from ..serializers import TeacherSerializer, CourseSerializer, CourseEnrollmentSerializer, AssessmentSerializer, SubmissionSerializer, QuizSerializer

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class TeacherProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = TeacherSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs['user_id']
        teacher = get_object_or_404(Teacher, user__id=user_id)
        return teacher


class TeacherCourseListAPIView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = Teacher.objects.get(id=teacher_id)

        return Course.objects.filter(teacher=teacher)


class TeacherCourseDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        teacher_id = self.kwargs['teacher_id']
        course_id = self.kwargs['course_id']

        teacher = Teacher.objects.get(id=teacher_id)
        return get_object_or_404(Course, teacher=teacher, course_id=course_id)


class TeacherCourseCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        institution = request.data['institution']
        teacher = request.data['teacher']
        title = request.data['title']

        institution = Institution.objects.get(name=institution)
        teacher = Teacher.objects.get(user__username=teacher)

        Course.objects.create(
            institution=institution, teacher=teacher, title=title)

        return Response({"message": "Course created successfully"}, status=status.HTTP_201_CREATED)


class TeacherStudentListAPIView(generics.ListAPIView):
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        course_id = self.kwargs['course_id']

        teacher = Teacher.objects.get(id=teacher_id)
        course = Course.objects.get(course_id=course_id)

        return CourseEnrollment.objects.filter(teacher=teacher, course=course)

    # def get_queryset(self):
    #     user_id = self.kwargs['user_id']
    #     user = user_models.User.objects.get(id=user_id)

    #     return user_models.Student.objects.filter(user=user)


class TeacherAssessmentCreateAPIView(generics.CreateAPIView):
    serializer_class = AssessmentSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        course_id = request.data['course_id']
        title = request.data['title']
        description = request.data['description']
        question_area = request.data['question_area']
        instructor_solution = request.data['instructor_solution']
        use_ai_grading = request.data['use_ai_grading']
        ai_grading_parameters = request.data['ai_grading_parameters']
        max_score = request.data['max_score']
        due_date = request.data['due_date']

        # Get the course object
        course = get_object_or_404(Course, course_id=course_id)

        Assessment.objects.create(
            course=course,
            title=title,
            description=description,
            question_area=question_area,
            instructor_solution=instructor_solution,
            use_ai_grading=use_ai_grading,
            ai_grading_parameters=ai_grading_parameters,
            max_score=max_score,
            due_date=due_date,
        )

        return Response({"message": "Assessment created successfully"}, status=status.HTTP_201_CREATED)


class TeacherAssessmentListAPIView(generics.ListAPIView):
    serializer_class = AssessmentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        course_id = self.kwargs['course_id']

        course = Course.objects.get(course_id=course_id)

        return Assessment.objects.filter(course=course)


class TeacherQuizCreateAPIView(generics.CreateAPIView):
    serializer_class = QuizSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        course_id = request.data['course_id']
        title = request.data['title']
        description = request.data['description']
        question_area = request.data['question_area']
        instructor_solution = request.data['instructor_solution']
        use_ai_grading = request.data['use_ai_grading']
        ai_grading_parameters = request.data['ai_grading_parameters']
        max_score = request.data['max_score']
        time_limit = request.data['time_limit']  # This is optional

        # Get the course object
        course = get_object_or_404(Course, course_id=course_id)

        quiz = Quiz.objects.create(
            course=course,
            title=title,
            description=description,
            question_area=question_area,
            instructor_solution=instructor_solution,
            use_ai_grading=use_ai_grading,
            ai_grading_parameters=ai_grading_parameters,
            max_score=max_score,
            time_limit=time_limit
        )

        return Response({"message": "Quiz created successfully", "quiz_id": quiz.quiz_id}, status=status.HTTP_201_CREATED)


class TeacherQuizListAPIView(generics.ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = Course.objects.get(course_id=course_id)
        return Quiz.objects.filter(course=course)


class TeacherScoresAPIView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = get_object_or_404(Teacher, id=teacher_id)
        course_id = self.kwargs['course_id']
        course = get_object_or_404(Course, course_id=course_id, teacher=teacher)
        return Submission.objects.filter(assessment__course=course, grading_status='PENDING')
