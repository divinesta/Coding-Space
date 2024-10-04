from django.contrib import admin
from users.models import User, Profile, Teacher, Student, Institution

# Register your models here.


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_at', 'updated_at']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'institution', 'user_type', 'otp']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'date']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'date']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'date']