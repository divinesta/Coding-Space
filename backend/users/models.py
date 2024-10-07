from django.db import models
from django.contrib.auth.models import AbstractUser
from django.apps import apps
from django.utils import timezone

from shortuuid.django_fields import ShortUUIDField
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
    
    def teachers(self):
        return User.objects.filter(institution=self, user_type="Instructor")
    
    def students(self):
        return User.objects.filter(institution=self, user_type="Student")


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, related_name='users', null=True, blank=True)
    user_type = models.CharField(max_length=100, choices=USER_TYPE, default="None")
    otp = models.CharField(max_length=100, null=True, blank=True)
    refresh_token = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True)
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
    
    def profile(self):
        return Profile.objects.get(user=self.user)

    def courses(self):
        return Course.objects.filter(teacher=self.teacher)
    
    def enrolled_students(self):
        return CourseEnrollment.objects.filter(course__teacher=self, is_enrolled=True)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher = models.ManyToManyField(Teacher, related_name='students', blank=True)
    identification_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    courses = models.ManyToManyField("users.Course", related_name='students', blank=True)
    assessments = models.ManyToManyField("users.Assessment", related_name='students', blank=True)
    quizzes = models.ManyToManyField("users.Quiz", related_name='students', blank=True)
    playgrounds = models.ManyToManyField("users.PlayGround", related_name='students', blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def courses(self):
        return Course.objects.filter(students=self)

    def assessments(self):
        return Assessment.objects.filter(students=self)

    def quizzes(self):
        return Quiz.objects.filter(students=self)

    def playgrounds(self):
        return PlayGround.objects.filter(students=self)


LANGUAGE_CHOICES = [
    ('python', 'Python'),
    ('javascript', 'JavaScript'),
    ('typescript', 'TypeScript'),
    ('c', 'C'),
    ('c++', 'C++'),
    ('c#', 'C#'),
]


class Course(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='courses')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    students = models.ManyToManyField(Student, related_name='courses', blank=True)
    title = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to='course_folder', default='default_course.jpg', null=True, blank=True)
    enrollment_code = models.CharField(max_length=10, null=True, blank=True)
    course_id = ShortUUIDField(
        length=8, max_length=10, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def students(self):
        return CourseEnrollment.objects.filter(course=self)
    
    def assessments(self):
        return Assessment.objects.filter(course=self)

    def quizzes(self):
        return Quiz.objects.filter(course=self)



class CourseEnrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True) 
    enrollment_id = ShortUUIDField(unique=True, length=10, max_length=10, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
    enrollment_date = models.DateTimeField(default=timezone.now)
    is_enrolled = models.BooleanField(default=False)

    class Meta:
        unique_together = [('course', 'student')]

    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.title}"

    def assessments(self):
        return Assessment.objects.filter(course=self.course)

    def quizzes(self):
        return Quiz.objects.filter(course=self.course)


class Assessment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assessments')
    title = models.CharField(max_length=200, help_text="at most 200 characters")
    description = models.TextField(null=True, blank=True)
    instructor_solution = models.TextField(null=True, blank=True)
    code_area = models.TextField(null=True, blank=True)
    question_area = models.TextField(null=True, blank=True)
    assessment_id = ShortUUIDField(unique=True, length=10, max_length=10, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
    use_ai_grading = models.BooleanField(default=False, null=True, blank=True)
    ai_grading_parameters = models.JSONField(null=True, blank=True)
    max_score = models.IntegerField(default=100, null=True, blank=True)
    due_date = models.DateTimeField(help_text="Deadline for assessment submission", null=True, blank=True)

    def __str__(self):
        return self.title

    def set_due_date(self, date, time):
        """
        Set the due date and time for the assessment.
        
        :param date: A date object (year, month, day)
        :param time: A time object (hour, minute)
        """
        self.due_date = timezone.make_aware(
            timezone.datetime.combine(date, time)
        )
        self.save()

    def is_overdue(self):
        """Check if the assessment is overdue."""
        if self.due_date is None:
            return False
        return timezone.now() > self.due_date
        

    def time_remaining(self):
        """Return the time remaining until the due date."""
        if self.due_date is None:
            return "No due date set"
        if self.is_overdue():
            return "Overdue"
        remaining = self.due_date - timezone.now()
        days, seconds = remaining.days, remaining.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{days} days, {hours} hours, {minutes} minutes"


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200, help_text="at most 200 characters")
    description = models.TextField(null=True, blank=True)
    code_area = models.TextField(null=True, blank=True)
    question_area = models.TextField(null=True, blank=True)
    quiz_id = ShortUUIDField(unique=True, length=10, max_length=10, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
    use_ai_grading = models.BooleanField(default=False)
    ai_grading_parameters = models.JSONField(null=True, blank=True)
    instructor_solution = models.TextField(null=True, blank=True)
    max_score = models.IntegerField(default=100)
    show_scores = models.BooleanField(default=False)
    time_limit = models.IntegerField(help_text="Time limit for the quiz in minutes", null=True, blank=True)

    def __str__(self):
        return self.title


class PlayGround(models.Model):
    title = models.CharField(max_length=200, help_text="at most 200 characters")
    playground_id = ShortUUIDField(unique=True, length=10, max_length=10, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
    code_area = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Submission(models.Model):
    SUBMISSION_TYPES = [
        ('ASSESSMENT', 'Assessment'),
        ('QUIZ', 'Quiz'),
    ]

    GRADING_STATUS = [
        ('PENDING', 'Pending'),
        ('GRADED', 'Graded'),
        ('REVALIDATION_REQUESTED', 'Revalidation Requested'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    submission_type = models.CharField(max_length=10, choices=SUBMISSION_TYPES)
    submitted_code = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True, blank=True)
    grading_status = models.CharField(
        max_length=25, choices=GRADING_STATUS, default='PENDING')
    ai_feedback = models.TextField(null=True, blank=True)
    instructor_feedback = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username}'s submission for {self.get_submission_type_display()}"
