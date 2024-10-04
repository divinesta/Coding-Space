from django.db import models
from django.utils import timezone
from django.apps import apps
from users.models import Teacher, Student

from shortuuid.django_fields import ShortUUIDField

# Create your models here.

LANGUAGE_CHOICES = [
    ('python', 'Python'),
    ('javascript', 'JavaScript'),
    ('typescript', 'TypeScript'),
    ('c', 'C'),
    ('c++', 'C++'),
    ('c#', 'C#'),
]

class Course(models.Model):
    institution = models.ForeignKey('users.Institution', on_delete=models.CASCADE, related_name='courses')
    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE, related_name='courses')
    students = models.ManyToManyField('users.Student', related_name='courses')
    title = models.CharField(max_length=300)
    description = models.TextField()
    image = models.FileField(upload_to='course_folder', default='default_course.jpg', null=True, blank=True)
    course_id = ShortUUIDField(length=10, max_length=10, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", prefix="CR")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def students(self):
        return CourseEnrollment.objects.filter(course=self)
    
    # def institution(self):
    #     institution = apps.get_model('users', 'Institution')
    #     return institution.objects.filter(students=self.students())


class CourseEnrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    enrollment_id = ShortUUIDField(unique=True, length=10, max_length=10, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
    enrollment_code = models.CharField(max_length=10, null=True, blank=True)
    enrollment_date = models.DateTimeField(default=timezone.now)
    is_enrolled = models.BooleanField(default=False)


    class Meta:
        unique_together = [('course', 'student')]        

    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.title}"

    def assessments(self):
        return Assessment.objects.filter(course=self)
    
    def quizzes(self):
        return Quiz.objects.filter(course=self)

class CodingArea(models.Model):
    title = models.CharField(max_length=200, help_text="at most 200 characters")
    code_area = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=200, choices=LANGUAGE_CHOICES, default='python')

    def __str__(self):
        return self.title
    
    def assessments(self):
        return Assessment.objects.filter(coding_area=self)
    
    def quiz(self):
        return Quiz.objects.filter(coding_area=self)
    
    def playgrounds(self):
        return PlayGround.objects.filter(coding_area=self)

class Assessment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assessments')
    title = models.CharField(max_length=200, help_text="at most 200 characters")
    description = models.TextField(null=True, blank=True)
    instructor_solution = models.TextField(null=True, blank=True)
    coding_area = models.ForeignKey(CodingArea, on_delete=models.SET_NULL, null=True, blank=True, related_name="assessment")
    question_area = models.TextField(null=True, blank=True)
    assessment_id = ShortUUIDField(unique=True, length=10, max_length=10, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
    use_ai_grading = models.BooleanField(default=False)
    ai_grading_parameters = models.JSONField(null=True, blank=True)
    max_score = models.IntegerField(default=100)
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
        return timezone.now() > self.due_date

    def time_remaining(self):
        """Return the time remaining until the due date."""
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
    coding_area = models.ForeignKey(CodingArea, on_delete=models.SET_NULL, null=True, blank=True, related_name="quiz")
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
    coding_area = models.ForeignKey(CodingArea, on_delete=models.SET_NULL, null=True, blank=True, related_name="playgrounds")

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

    student = models.ForeignKey(
        'users.Student', on_delete=models.CASCADE, related_name='submissions')
    assessment = models.ForeignKey(
        Assessment, on_delete=models.CASCADE, null=True, blank=True)
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, null=True, blank=True)
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

