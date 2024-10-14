from users import views as user_views
from django.urls import path

urlpatterns = [
    # Institution
    path('institutions/', user_views.InstitutionListAPIView.as_view()),
    #TODO: correct this url and it's view
    path('institutions/teacher-list/<institution_id>/', user_views.TeacherListAPIView.as_view()),

    # Student
    path('students/profile/<user_id>/', user_views.StudentProfileAPIView.as_view()),
    path('students/enroll-course/', user_views.EnrollStudentsAPIView.as_view()),
    path('students/<student_id>/course-list/', user_views.StudentCourseListAPIView.as_view()),
    path('students/<student_id>/course-detail/<course_id>/', user_views.StudentCourseDetailAPIView.as_view()),
    path('students/<student_id>/playgrounds/', user_views.StudentPlaygroundAPIView.as_view(), name='student-playgrounds'),
    path('students/<student_id>/courses/<course_id>/assignments/', user_views.StudentAssignmentAPIView.as_view(), name='student-assignments'),
    path('students/<student_id>/courses/<course_id>/quizzes/', user_views.StudentQuizAPIView.as_view(), name='student-quizzes'),
    path('students/<student_id>/scores/', user_views.StudentScoresAPIView.as_view(), name='student-scores'),

    # Teacher
    path('teacher/profile/<user_id>/', user_views.TeacherProfileAPIView.as_view()),
    path('teacher/create-course/', user_views.TeacherCourseCreateAPIView.as_view()),
    path('teacher/<teacher_id>/course/', user_views.TeacherCourseListAPIView.as_view()),
    path('teacher/<teacher_id>/course-detail/<course_id>/', user_views.TeacherCourseDetailAPIView.as_view()),
    path('teacher/<teacher_id>/enrolled-students/<course_id>/', user_views.TeacherStudentListAPIView.as_view()),
    path('teacher/create-assessment/', user_views.TeacherAssessmentCreateAPIView.as_view()),
    path('teacher/assessment-list/<course_id>/', user_views.TeacherAssessmentListAPIView.as_view()),
    path('teacher/create-quiz/', user_views.TeacherQuizCreateAPIView.as_view()),
    path('teacher/quiz-list/<course_id>/',user_views.TeacherQuizListAPIView.as_view()),
    path('teacher/courses/<course_id>/scores/', user_views.TeacherScoresAPIView.as_view(), name='teacher-course-scores'),
    
    
    # Submission
    path('submissions/<submission_id>/grade/', user_views.ManualGradeAPIView.as_view(), name='manual-grade'),
    path('submissions/<submission_id>/ai-grade/', user_views.AIGradeAPIView.as_view(), name='ai-grade'),
]
