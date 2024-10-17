from django.shortcuts import get_object_or_404

from ..models import Teacher, Submission
from ..service import perform_ai_grading

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response


class ManualGradeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request, submission_id):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        submission = get_object_or_404(Submission, id=submission_id)

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
        teacher_id = request.data['teacher_id']
        teacher = get_object_or_404(Teacher, id=teacher_id)
        submission = get_object_or_404(Submission, id=submission_id)

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
