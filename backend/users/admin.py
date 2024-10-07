from django.contrib import admin
from . import models as user_models

# Register your models here.


@admin.register(user_models.Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_at', 'updated_at']

@admin.register(user_models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'institution', 'user_type', 'otp']


@admin.register(user_models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'date']

@admin.register(user_models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'date']

@admin.register(user_models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'date']

@admin.register(user_models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["institution", "teacher", "title", "course_id", "enrollment_code", "date"]

@admin.register(user_models.CourseEnrollment)
class CourseEnrollment(admin.ModelAdmin):
    list_display = ["course", "student", "teacher", "enrollment_id", "enrollment_date", "is_enrolled"]

@admin.register(user_models.Assessment)
class Assessment(admin.ModelAdmin):
    list_display = ["course", "title", "due_date", "time_remaining", "is_overdue"]

@admin.register(user_models.Quiz)
class Quiz(admin.ModelAdmin):
    list_display = [ "course", "title", "description", "time_limit"]

@admin.register(user_models.PlayGround)
class PlayGround(admin.ModelAdmin):
    list_display = ["title", "playground_id", "code_area"]

@admin.register(user_models.Submission)
class Submission(admin.ModelAdmin):
    list_display = ["student", "submission_type", "score"]

