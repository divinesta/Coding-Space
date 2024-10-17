from .views.institution_views import InstitutionManagerCreateView, CreateAdminView, AdminList, AdminDetail
from .views.admin_views import CreateUserView, TeacherList, TeacherDetail, StudentList, StudentDetail, BulkAddUsersView
from .views.teacher_views import TeacherProfileAPIView, TeacherCourseListAPIView, TeacherCourseDetailAPIView, TeacherStudentListAPIView, TeacherAssessmentListAPIView, TeacherQuizListAPIView, TeacherScoresAPIView, TeacherCourseCreateAPIView, TeacherAssessmentCreateAPIView, TeacherQuizCreateAPIView
from .views.student_views import StudentAssignmentAPIView, StudentQuizAPIView, StudentScoresAPIView, StudentCourseDetailAPIView, StudentCourseListAPIView, StudentPlaygroundAPIView, StudentProfileAPIView, EnrollStudentsAPIView
from .views.submission_views import ManualGradeAPIView, AIGradeAPIView
from django.urls import path

urlpatterns = [
    # Institution
    path('institutions/create/', InstitutionManagerCreateView.as_view()),
    
    #Institution Manager
    path('manager/create-admin/', CreateAdminView.as_view(), name='create-admin'),
    path('manager/admins-list/', AdminList.as_view(), name='admin-list'),
    path('manager/admin-detail/<admin_id>/', AdminDetail.as_view()),
    
    #Institution Admin
    path('admin/create-user/', CreateUserView.as_view()),
    path('admin/<institution_id>/teachers-list/', TeacherList.as_view()),
    path('admin/<institution_id>/teacher-detail/<teacher_id>/', TeacherDetail.as_view()),
    path('admin/<institution_id>/students-list/', StudentList.as_view()), #checked ✅
    path('admin/<institution_id>/student-detail/<student_id>/', StudentDetail.as_view()), #checked ✅
    path('admin/bulk-file-upload/', BulkAddUsersView.as_view()),
    
    #Student
    path('students/profile/<user_id>/', StudentProfileAPIView.as_view()),
    path('students/enroll-course/', EnrollStudentsAPIView.as_view()),
    path('students/<student_id>/course-list/', StudentCourseListAPIView.as_view()),
    path('students/<student_id>/course-detail/<course_id>/', StudentCourseDetailAPIView.as_view()),
    path('students/<student_id>/playgrounds/', StudentPlaygroundAPIView.as_view(), name='student-playgrounds'),
    path('students/<student_id>/courses/<course_id>/assignments/', StudentAssignmentAPIView.as_view(), name='student-assignments'),
    path('students/<student_id>/courses/<course_id>/quizzes/', StudentQuizAPIView.as_view(), name='student-quizzes'),
    path('students/<student_id>/scores/', StudentScoresAPIView.as_view(), name='student-scores'),

    # Teacher
    path('teacher/profile/<user_id>/', TeacherProfileAPIView.as_view()),
    path('teacher/create-course/', TeacherCourseCreateAPIView.as_view()),
    path('teacher/<teacher_id>/course/', TeacherCourseListAPIView.as_view()),
    path('teacher/<teacher_id>/course-detail/<course_id>/', TeacherCourseDetailAPIView.as_view()),
    path('teacher/<teacher_id>/enrolled-students/<course_id>/', TeacherStudentListAPIView.as_view()),
    path('teacher/create-assessment/', TeacherAssessmentCreateAPIView.as_view()),
    path('teacher/assessment-list/<course_id>/', TeacherAssessmentListAPIView.as_view()),
    path('teacher/create-quiz/', TeacherQuizCreateAPIView.as_view()),
    path('teacher/quiz-list/<course_id>/',TeacherQuizListAPIView.as_view()),
    path('teacher/courses/<course_id>/scores/', TeacherScoresAPIView.as_view(), name='teacher-course-scores'),
    
    
    # Submission
    path('submissions/<submission_id>/grade/', ManualGradeAPIView.as_view(), name='manual-grade'),
    path('submissions/<teacher_id>/<submission_id>/ai-grade/', AIGradeAPIView.as_view(), name='ai-grade'),
]
