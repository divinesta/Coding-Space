from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.apps import apps
from django.utils import timezone

from .validators import validate_image

from shortuuid.django_fields import ShortUUIDField
# Create your models here.



class Institution(models.Model):
    SUBSCRIPTION_STATUS = [
        ('trial', 'Trial'),
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed')
    ]
    
    name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    logo = models.ImageField(upload_to='institution_logos/', null=True, blank=True, validators=[validate_image])

    date_registered = models.DateTimeField(auto_now_add=True)  # Auto-timestamp when created
    
    subscription_status = models.CharField(max_length=20, choices=SUBSCRIPTION_STATUS, default='trial')
    subscription_end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
    


class User(AbstractUser):
    USER_ROLES = [
        ('manager', 'Manager'),
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('none', 'None')
    ]
    
    username = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    user_role = models.CharField(max_length=100, choices=USER_ROLES, null=True, blank=True)

    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    otp = models.CharField(max_length=100, null=True, blank=True)
    refresh_token = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        # This method runs before the model instance is saved
        # It ensures that the username is set if it's not already provided
        if not self.username:
            # If username is not set, use the part of the email before '@'
            self.username = self.email.split('@')[0]
        # Call the parent class's save method to actually save the instance
        super().save(*args, **kwargs)


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
    institution = models.OneToOneField(Institution, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Owner: {self.user.username}"


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='admins')
    image = models.ImageField(upload_to='admin_folder', default='default_admin_user.jpg', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Admin: {self.user.username}"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    image = models.ImageField(upload_to='teacher_folder', default='default_teacher_user.jpg', null=True, blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='teachers', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Teacher: {self.user.username}"
    

    def courses(self):
        return Course.objects.filter(teacher=self.teacher)
    
    def enrolled_students(self):
        return CourseEnrollment.objects.filter(course__teacher=self, is_enrolled=True)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='students', null=True, blank=True)
    image = models.ImageField(upload_to='student_folder', default='default_student_user.jpg', null=True, blank=True)
    teacher = models.ManyToManyField(Teacher, related_name='students', blank=True)
    identification_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    assessments = models.ManyToManyField("users.Assessment", related_name='students', blank=True)
    quizzes = models.ManyToManyField("users.Quiz", related_name='students', blank=True)
    playgrounds = models.ManyToManyField("users.PlayGround", related_name='students', blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Student: {self.user.username}"

    def courses(self):
        return Course.objects.filter(courseenrollment__student=self)

    def assessments(self):
        return Assessment.objects.filter(students=self)

    def quizzes(self):
        return Quiz.objects.filter(students=self)

    def playgrounds(self):
        return PlayGround.objects.filter(students=self)



class Course(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='courses')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    students = models.ManyToManyField(Student, related_name='courses', blank=True)
    title = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='course_folder', default='default_course.jpg', null=True, blank=True)
    enrollment_code = models.CharField(max_length=10, null=True, blank=True)
    course_id = ShortUUIDField(
        length=8, max_length=10, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
    created_at = models.DateTimeField(auto_now_add=True)

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
    enrollment_date = models.DateTimeField(auto_now_add=True)
    is_enrolled = models.BooleanField(default=False)

    class Meta:
        unique_together = [('course', 'student')]

    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.title}"

    def assessments(self):
        return Assessment.objects.filter(course=self.course)

    def quizzes(self):
        return Quiz.objects.filter(course=self.course)
    

class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, related_name='materials', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='course_materials/', validators=[FileExtensionValidator(['pdf'])], null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} for {self.course.title}"


class Assessment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, help_text="at most 200 characters")
    description = models.TextField(null=True, blank=True)
    instructor_solution = models.TextField(null=True, blank=True)
    code_area = models.TextField(null=True, blank=True)
    question_area = models.TextField(null=True, blank=True)
    assessment_id = ShortUUIDField(unique=True, length=20, max_length=20, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
    use_ai_grading = models.BooleanField(default=False, null=True, blank=True)
    ai_grading_parameters = models.JSONField(null=True, blank=True)
    ai_feedback = models.TextField(null=True, blank=True)
    instructor_feedback = models.TextField(null=True, blank=True)
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
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200, help_text="at most 200 characters")
    description = models.TextField(null=True, blank=True)
    code_area = models.TextField(null=True, blank=True)
    question_area = models.TextField(null=True, blank=True)
    quiz_id = ShortUUIDField(unique=True, length=20, max_length=20, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
    use_ai_grading = models.BooleanField(default=False)
    ai_grading_parameters = models.JSONField(null=True, blank=True)
    instructor_solution = models.TextField(null=True, blank=True)
    max_score = models.IntegerField(default=100)
    show_scores = models.BooleanField(default=False)
    ai_feedback = models.TextField(null=True, blank=True)
    instructor_feedback = models.TextField(null=True, blank=True)
    time_limit = models.IntegerField(help_text="Time limit for the quiz in minutes", null=True, blank=True)

    def __str__(self):
        return self.title


class PlayGround(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='playgrounds')
    title = models.CharField(max_length=200, help_text="at most 200 characters")
    playground_id = ShortUUIDField(unique=True, length=20, max_length=20, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
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

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='submissions', null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions', null=True, blank=True)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    submission_type = models.CharField(max_length=10, choices=SUBMISSION_TYPES)
    submitted_code = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True, blank=True)
    grading_status = models.CharField(
        max_length=25, choices=GRADING_STATUS, default='PENDING')
    ai_feedback = models.TextField(null=True, blank=True)
    is_viewed = models.BooleanField(default=False)
    instructor_feedback = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username}'s submission for {self.get_submission_type_display()}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    feedback = models.TextField()
    feedback_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s feedback"


class IssueReport(models.Model):
    REPORT_STATUS = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    reporter = models.ForeignKey(User, related_name='issue_reports', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=REPORT_STATUS, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Issue: {self.title} by {self.reporter.username}"


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"