# backend/users/tasks.py

from celery import shared_task
from .models import Submission
from .service import perform_ai_grading


@shared_task
def grade_submission_task(submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
    except Submission.DoesNotExist:
        return "Submission does not exist."

    try:
        if submission.submission_type == 'ASSESSMENT' and submission.assessment:
            instructor_solution = submission.assessment.instructor_solution
            grading_parameters = submission.assessment.ai_grading_parameters
        elif submission.submission_type == 'QUIZ' and submission.quiz:
            instructor_solution = submission.quiz.instructor_solution
            grading_parameters = submission.quiz.ai_grading_parameters
        else:
            submission.grading_status = 'PENDING'
            submission.save()
            return "Invalid submission type."

        ai_score, ai_feedback = perform_ai_grading(
            submitted_code=submission.submitted_code,
            instructor_solution=instructor_solution,
            grading_parameters=grading_parameters
        )

        submission.score = ai_score
        submission.ai_feedback = ai_feedback
        submission.grading_status = 'GRADED'
        submission.save()
        return "Grading completed successfully."

    except Exception as e:
        submission.grading_status = 'PENDING'
        submission.save()
        return f"Grading failed: {str(e)}"
