from django.shortcuts import get_object_or_404

from . import models as user_models
from . import serializers as user_serializers
from .service import perform_ai_grading
from .tasks import grade_submission_task

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser




#TODO: Implement payment logic: When payment has been successful, change the 
# institution status to 'paid', and set active to True

class InstitutionListCreateAPIView(generics.ListCreateAPIView):
    queryset = user_models.Institution.objects.all()
    serializer_class = user_serializers.InstitutionSerializer
    #TODO: update permissions
    permission_classes = [AllowAny]


class InstitutionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = user_serializers.InstitutionSerializer
    #TODO: update permissions
    permission_classes = [AllowAny]

    def get_object(self):
        institution_id = self.kwargs['institution_id']
        institution = get_object_or_404(user_models.Institution, id=institution_id)
        return institution



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
        question_area = request.data['question_area']
        instructor_solution = request.data['instructor_solution']
        use_ai_grading = request.data['use_ai_grading']
        ai_grading_parameters = request.data['ai_grading_parameters']
        max_score = request.data['max_score']
        due_date = request.data['due_date']

        # Get the course object
        course = get_object_or_404(user_models.Course, course_id=course_id)

        user_models.Assessment.objects.create(
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
        question_area = request.data['question_area']
        instructor_solution = request.data['instructor_solution']
        use_ai_grading = request.data['use_ai_grading']
        ai_grading_parameters = request.data['ai_grading_parameters']
        max_score = request.data['max_score']
        time_limit = request.data['time_limit']  # This is optional

        # Get the course object
        course = get_object_or_404(user_models.Course, course_id=course_id)

        quiz = user_models.Quiz.objects.create(
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


class TeacherScoresAPIView(generics.ListAPIView):
    serializer_class = user_serializers.SubmissionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = get_object_or_404(user_models.Teacher, id=teacher_id)
        course_id = self.kwargs['course_id']
        course = get_object_or_404(user_models.Course, course_id=course_id, teacher=teacher)
        return user_models.Submission.objects.filter(assessment__course=course, grading_status='PENDING')



class ManualGradeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request, submission_id):
        teacher = get_object_or_404(user_models.Teacher, user=self.request.user)
        submission = get_object_or_404(user_models.Submission, id=submission_id)

        # Ensure the submission belongs to the teacher's course
        if submission.assessment.course.teacher != teacher and submission.quiz.course.teacher != teacher:
            return Response({"message": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

        score = request.data.get('score')
        feedback = request.data.get('feedback')

        if score is not None:
            submission.score = score

        if feedback is not None:
            submission.instructor_feedback = feedback

        submission.grading_status = 'GRADED'
        submission.save()

        return Response({"message": "Submission graded successfully."}, status=status.HTTP_200_OK)


class AIGradeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request, submission_id):
        # teacher_id = request.data['teacher_id']
        teacher = get_object_or_404(user_models.Teacher, user=self.request.user)
        submission = get_object_or_404(user_models.Submission, id=submission_id)

        # Ensure the submission belongs to the teacher's course
        belongs_to_teacher = False
        if submission.assessment and submission.assessment.course.teacher == teacher:
            belongs_to_teacher = True
        if submission.quiz and submission.quiz.course.teacher == teacher:
            belongs_to_teacher = True

        if not belongs_to_teacher:
            return Response({"message": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

        # Integrate AI Grading Logic
        try:
            if submission.submission_type == 'ASSESSMENT' and submission.assessment:
                instructor_solution = submission.assessment.instructor_solution
                grading_parameters = submission.assessment.ai_grading_parameters
            elif submission.submission_type == 'QUIZ' and submission.quiz:
                instructor_solution = submission.quiz.instructor_solution
                grading_parameters = submission.quiz.ai_grading_parameters
            else:
                return Response({"message": "Invalid submission type."}, status=status.HTTP_400_BAD_REQUEST)

            ai_score, ai_feedback = perform_ai_grading(
                submitted_code=submission.submitted_code,
                instructor_solution=instructor_solution,
                grading_parameters=grading_parameters
            )

            submission.score = ai_score
            submission.ai_feedback = ai_feedback
            submission.grading_status = 'GRADED'
            submission.save()

            return Response(
                {
                    "message": "Submission graded using AI.",
                    "ai_score": ai_score,
                    "ai_feedback": ai_feedback
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message": "AI grading failed.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


#Student Views

class StudentCourseListAPIView(generics.ListAPIView):
    serializer_class = user_serializers.CourseEnrollmentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        student = get_object_or_404(user_models.Student, id=student_id) 
        return user_models.CourseEnrollment.objects.filter(student=student)



class StudentCourseDetailAPIView(generics.RetrieveAPIView):
    serializer_class = user_serializers.CourseEnrollmentSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        student_id = self.kwargs['student_id']
        student = get_object_or_404(user_models.Student, id=student_id)

        course_id = self.kwargs['course_id']
        course = get_object_or_404(user_models.Course, course_id=course_id)

        # Use get() instead of filter() to retrieve a single CourseEnrollment instance
        return get_object_or_404(user_models.CourseEnrollment, student=student, course=course)


class StudentPlaygroundAPIView(generics.ListCreateAPIView):
    serializer_class = user_serializers.PlayGroundSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        student = get_object_or_404(user_models.Student, id=student_id)
        return user_models.PlayGround.objects.filter(student=student)

    def perform_create(self, serializer):
        student_id = self.kwargs['student_id']
        student = get_object_or_404(user_models.Student, id=student_id)
        serializer.save()
        student.playgrounds.add(serializer.instance)

class StudentAssignmentAPIView(generics.ListCreateAPIView):
    serializer_class = user_serializers.AssessmentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        student_id = self.kwargs['student_id']
        course = get_object_or_404(user_models.Course, course_id=course_id)
        student = get_object_or_404(user_models.Student, id=student_id)
        return user_models.Assessment.objects.filter(course=course, students=student)

    def create(self, request, *args, **kwargs):
        assessment_id = request.data.get('assessment_id')
        submitted_code = request.data.get('submitted_code')

        assessment = get_object_or_404(user_models.Assessment, assessment_id=assessment_id)
        student = get_object_or_404(user_models.Student, user=self.request.user)

        submission = user_models.Submission.objects.create(
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
    serializer_class = user_serializers.QuizSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        student_id = self.kwargs['student_id']
        course = get_object_or_404(user_models.Course, course_id=course_id)
        student = get_object_or_404(user_models.Student, id=student_id)
        return user_models.Quiz.objects.filter(course=course, students=student)

    def create(self, request, *args, **kwargs):
        quiz_id = request.data.get('quiz_id')
        submitted_code = request.data.get('submitted_code')

        quiz = get_object_or_404(user_models.Quiz, quiz_id=quiz_id)
        student = get_object_or_404(user_models.Student, user=self.request.user)

        submission = user_models.Submission.objects.create(
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
    serializer_class = user_serializers.SubmissionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        student = get_object_or_404(user_models.Student, id=student_id)
        return user_models.Submission.objects.filter(student=student, grading_status='GRADED')


