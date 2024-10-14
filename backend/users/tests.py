# backend/users/tests.py

from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from . import models as user_models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class AIGradingAPITestCase(TestCase):
    def setUp(self):
        # Generate unique emails using uuid
        teacher_email = f"teacher1_{uuid.uuid4()}@example.com"
        student_email = f"student1_{uuid.uuid4()}@example.com"

        # Create a teacher user with a unique email
        self.teacher_user = User.objects.create_user(
            username='teacher1',
            email=teacher_email,  # Assign unique email
            password='pass123',
            user_type='Instructor'
        )
        self.teacher = user_models.Teacher.objects.create(
            user=self.teacher_user
        )

        # Create a student user with a unique email
        self.student_user = User.objects.create_user(
            username='student1',
            email=student_email,  # Assign unique email
            password='pass123',
            user_type='Student'
        )
        self.student = user_models.Student.objects.create(
            user=self.student_user
        )

        # Create an institution
        self.institution = user_models.Institution.objects.create(
            name='Test Institution',
            code='TESTINSTITUTION'
        )

        # Create a course
        self.course = user_models.Course.objects.create(
            course_id='COURSE123',
            title='Test Course',
            institution=self.institution,
            teacher=self.teacher
        )

        # Create an assessment
        self.assessment = user_models.Assessment.objects.create(
            assessment_id='ASSESS123',
            course=self.course,
            title='Test Assessment',
            description='An assessment for testing.',
            question_area='Write a function to add two numbers.',
            instructor_solution='def add(a, b):\n    sum = a + b\n    return sum',
            use_ai_grading=True,
            ai_grading_parameters={
                "correctness": "Ensure the function correctly adds two numbers.",
                "efficiency": "Use the most efficient approach without compromising readability.",
                "code_quality": "Follow PEP 8 guidelines and include necessary comments."
            },
            max_score=100,
            due_date='2025-12-31T23:59:59Z'
        )

        # Enroll the student in the course
        user_models.CourseEnrollment.objects.create(
            course=self.course,
            student=self.student,
            teacher=self.teacher,
            is_enrolled=True
        )

        # Initialize API client
        self.client = APIClient()
        self.client.login(username='student1', password='pass123')

    @patch('users.service.perform_ai_grading')
    def test_ai_grading_triggered_on_submission(self, mock_perform_ai_grading):
        # Define mock response
        mock_perform_ai_grading.return_value = (
            95.0, "Great job! Your solution is correct and efficient.")

        # Submit an assignment
        submit_url = reverse('student-assignments', kwargs={
            'student_id': self.student.id,
            'course_id': self.course.course_id
        })
        submission_data = {
            'assessment_id': self.assessment.assessment_id,
            'submitted_code': 'def add(a, b):\n    return a + b'
        }
        response = self.client.post(submit_url, submission_data, format='json')

        # Verify the submission was created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        submission_id = response.data.get('submission_id')
        submission = user_models.Submission.objects.get(id=submission_id)

        # Verify AI grading was called
        mock_perform_ai_grading.assert_called_once_with(
            submitted_code='def add(a, b):\n    return a + b',
            instructor_solution='def add(a, b):\n    sum = a + b\n    return sum',
            grading_parameters=self.assessment.ai_grading_parameters
        )

        # Verify the submission fields are updated
        self.assertEqual(submission.score, 95.0)
        self.assertEqual(submission.ai_feedback,
                         "Great job! Your solution is correct and efficient.")
        self.assertEqual(submission.grading_status, 'GRADED')

    @patch('users.service.perform_ai_grading')
    def test_ai_grading_handles_missing_solution(self, mock_perform_ai_grading):
        # Define mock to raise ValueError when instructor_solution is missing
        mock_perform_ai_grading.side_effect = ValueError(
            "Instructor solution is missing.")

        # Create a new assessment without an instructor solution
        assessment_no_solution = user_models.Assessment.objects.create(
            assessment_id='ASSESS124',
            course=self.course,
            title='Assessment Without Solution',
            description='An assessment without an instructor solution.',
            question_area='Write a function to subtract two numbers.',
            instructor_solution='',
            use_ai_grading=True,
            ai_grading_parameters={
                "correctness": "Ensure the function correctly subtracts two numbers.",
                "efficiency": "Use the most efficient approach without compromising readability.",
                "code_quality": "Follow PEP 8 guidelines and include necessary comments."
            },
            max_score=100,
            due_date='2025-12-31T23:59:59Z'
        )

        # Submit an assignment with missing instructor solution
        submit_url = reverse('student-assignments', kwargs={
            'student_id': self.student.id,
            'course_id': self.course.course_id
        })
        submission_data = {
            'assessment_id': assessment_no_solution.assessment_id,
            'submitted_code': 'def subtract(a, b):\n    return a - b'
        }
        response = self.client.post(submit_url, submission_data, format='json')

        # Verify the submission was created with pending grading
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        submission_id = response.data.get('submission_id')
        submission = user_models.Submission.objects.get(id=submission_id)

        # Verify AI grading was called
        mock_perform_ai_grading.assert_called_once_with(
            submitted_code='def subtract(a, b):\n    return a - b',
            instructor_solution='',
            grading_parameters=assessment_no_solution.ai_grading_parameters
        )

        # Verify the submission fields are updated accordingly
        self.assertIsNone(submission.score)
        self.assertEqual(submission.ai_feedback,
                         "AI grading failed due to an internal error.")
        self.assertEqual(submission.grading_status, 'PENDING')
