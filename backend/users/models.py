from django.db import models
from django.contrib.auth.models import AbstractUser
from django.apps import apps


# Create your models here.

USER_TYPE = [
    ("Instructor", "Instructor"),
    ("Student", "Student")
]

class Institution(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    user_type = models.CharField(max_length=100, choices=USER_TYPE, default="None")
    otp = models.CharField(max_length=100, null=True, blank=True)
    refresh_token = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='user_folder', default='default_user.jpg', null=True, blank=True)
    full_name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = self.user.username
        super(Profile, self).save(*args, **kwargs)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    def courses(self):
        Course = apps.get_model('assessments', 'Course')
        return Course.objects.filter(teacher=self)
    
    def EnrolledStudents(self):
        CourseEnrollment = apps.get_model('assessments', 'CourseEnrollment')
        # The double underscore (__) in Django ORM queries is used for traversing relationships.
        # In this case, course__teacher=self means:
        # 1. Look at the 'course' field of CourseEnrollment
        # 2. Then look at the 'teacher' field of that course
        # 3. Filter where that teacher is the current instance (self)
        # 
        # So this line returns all CourseEnrollment objects where the course's teacher is the current teacher
        return CourseEnrollment.objects.filter(course__teacher=self, is_enrolled=True)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher = models.ManyToManyField(Teacher, related_name='students', blank=True)
    courses = models.ManyToManyField(
        "assessments.Course", related_name='students', blank=True)
    assessments = models.ManyToManyField(
        "assessments.Assessment", related_name='students', blank=True)
    quizzes = models.ManyToManyField(
        "assessments.Quiz", related_name='students', blank=True)
    playgrounds = models.ManyToManyField(
        "assessments.PlayGround", related_name='students', blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_courses(self):
        Course = apps.get_model('assessments', 'Course')
        return Course.objects.filter(students=self)

    def get_assessments(self):
        Assessment = apps.get_model('assessments', 'Assessment')
        return Assessment.objects.filter(students=self)

    def get_quizzes(self):
        Quiz = apps.get_model('assessments', 'Quiz')
        return Quiz.objects.filter(students=self)

    def get_playgrounds(self):
        PlayGround = apps.get_model('assessments', 'PlayGround')
        return PlayGround.objects.filter(students=self)
