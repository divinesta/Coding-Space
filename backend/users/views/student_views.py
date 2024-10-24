from django.shortcuts import get_object_or_404

from ..models import User, Student, CourseEnrollment, Course, Assessment, Quiz, PlayGround, Submission, Teacher, Institution
from ..serializers import StudentSerializer, CourseEnrollmentSerializer, CourseSerializer, AssessmentSerializer, QuizSerializer, PlayGroundSerializer, SubmissionSerializer
from ..tasks import grade_submission_task

from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework.permissions import AllowAny


class StudentProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs['user_id']
        institution_id = self.kwargs['institution_id']
        user = User.objects.get(id=user_id)
        institution = get_object_or_404(Institution, id=institution_id)
        student = get_object_or_404(Student, user=user, institution=institution)
        return student
        # user = user_models.User.objects.get(id=user_id)

        # return user_models.Student.objects.get(user=user)
        

class StudentCourseListAPIView(generics.ListAPIView):
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        student = get_object_or_404(Student, id=student_id)
        return CourseEnrollment.objects.filter(student=student)


class StudentCourseDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        student_id = self.kwargs['student_id']
        student = get_object_or_404(Student, id=student_id)

        course_id = self.kwargs['course_id']
        course = get_object_or_404(Course, course_id=course_id)

        # Use get() instead of filter() to retrieve a single CourseEnrollment instance
        return get_object_or_404(CourseEnrollment, student=student, course=course)


class EnrollStudentsAPIView(generics.CreateAPIView):
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        student_id = request.data['student_id']
        teacher_id = request.data['teacher_id']
        course_id = request.data['course_id']
        enrollment_code = request.data['enrollment_code']

        # Validate the enrollment code
        try:
            course = Course.objects.get(
                course_id=course_id, enrollment_code=enrollment_code)
        except Course.DoesNotExist:
            return Response({"message": "Invalid enrollment code"}, status=status.HTTP_400_BAD_REQUEST)

        if enrollment_code is None:
            return Response({"message": "Enrollment code is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the student is already enrolled
        student = get_object_or_404(Student, id=student_id)
        if CourseEnrollment.objects.filter(course=course, student=student).exists():
            return Response({"message": "You are already enrolled in this course."}, status=status.HTTP_400_BAD_REQUEST)

        teacher = get_object_or_404(Teacher, id=teacher_id)

        # Enroll the student
        CourseEnrollment.objects.create(
            course=course, student=student, teacher=teacher, is_enrolled=True)

        return Response({"message": "Course enrolled successfully."}, status=status.HTTP_201_CREATED)



class StudentPlaygroundAPIView(generics.ListCreateAPIView):
    serializer_class = PlayGroundSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        student = get_object_or_404(Student, id=student_id)
        return PlayGround.objects.filter(student=student)

    def perform_create(self, serializer):
        student_id = self.kwargs['student_id']
        student = get_object_or_404(Student, id=student_id)
        serializer.save()
        student.playgrounds.add(serializer.instance)


class StudentAssignmentAPIView(generics.ListCreateAPIView):
    serializer_class = AssessmentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        student_id = self.kwargs['student_id']
        course = get_object_or_404(Course, course_id=course_id)
        student = get_object_or_404(Student, id=student_id)
        return Assessment.objects.filter(course=course, students=student)

    def create(self, request, *args, **kwargs):
        assessment_id = request.data.get('assessment_id')
        submitted_code = request.data.get('submitted_code')

        assessment = get_object_or_404(Assessment, assessment_id=assessment_id)
        student = get_object_or_404(Student, user=self.request.user)

        submission = Submission.objects.create(
            student=student,
            assessment=assessment,
            submission_type='ASSESSMENT',
            submitted_code=submitted_code
        )

        # Trigger AI grading asynchronously
        grade_submission_task.delay(submission.id)

        return Response(
            {"message": "Assignment submitted successfully.",
                "submission_id": submission.id},
            status=status.HTTP_201_CREATED
        )


class StudentQuizAPIView(generics.ListCreateAPIView):
    serializer_class = QuizSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        student_id = self.kwargs['student_id']
        course = get_object_or_404(Course, course_id=course_id)
        student = get_object_or_404(Student, id=student_id)
        return Quiz.objects.filter(course=course, students=student)

    def create(self, request, *args, **kwargs):
        quiz_id = request.data.get('quiz_id')
        submitted_code = request.data.get('submitted_code')

        quiz = get_object_or_404(Quiz, quiz_id=quiz_id)
        student = get_object_or_404(Student, user=self.request.user)

        submission = Submission.objects.create(
            student=student,
            quiz=quiz,
            submission_type='QUIZ',
            submitted_code=submitted_code
        )

        # Trigger AI grading asynchronously
        grade_submission_task.delay(submission.id)

        return Response(
            {"message": "Quiz submitted successfully.",
                "submission_id": submission.id},
            status=status.HTTP_201_CREATED
        )


class StudentScoresAPIView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        student = get_object_or_404(Student, id=student_id)
        return Submission.objects.filter(student=student, grading_status='GRADED')
