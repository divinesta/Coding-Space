from django.apps import apps
from django.utils.crypto import get_random_string
from importlib import import_module

from rest_framework import serializers

from . import models as user_models


def get_serializer(app_label, serializer_name):
    try:
        module = import_module(f"{app_label}.serializers")
        serializer = getattr(module, serializer_name, None)

        if serializer is None:
            raise AttributeError(f"Could not find serializer {serializer_name} in {app_label}.serializers")

        return serializer
    except ImportError:
        raise ImportError(
            f"Could not import serializers module from {app_label}")



class UserSerializer(serializers.ModelSerializer):
    institution = serializers.StringRelatedField(many=False)
    class Meta:
        model = user_models.User
        fields = ['id', 'email', 'username', 'user_role','institution']
        read_only_fields = ['id', 'user_role']
        
class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    institution = serializers.StringRelatedField(many=False)
    
    class Meta:
        model = user_models.Admin
        fields = ['id', 'user', 'institution', 'image', 'date']



# class AdminCreationSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(write_only=True)
#     institution_id = serializers.IntegerField(write_only=True)
#     user_role = "admin"

#     class Meta:
#         model = user_models.User
#         fields = ['id', 'email', 'institution_id', 'user_role']

#     def create(self, validated_data):
#         email = validated_data.pop('email')
#         institution_id = validated_data.pop('institution_id')
#         user_role = validated_data.pop('user_role')

#         institution = user_models.Institution.objects.get(id=institution_id)
        
#         password = get_random_string(8)
        
#         user = user_models.User.objects.create_user(
#             username=email.split('@')[0],
#             email=email,
#             password=password,
#             user_role=user_role,
#             institution=institution
#         )
#         admin = user_models.Admin.objects.create(user=user, institution=institution)
#         return admin

class AssessmentSerializer(serializers.ModelSerializer):
    due_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    time_remaining = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    ai_feedback = serializers.CharField(read_only=True)
    instructor_feedback = serializers.CharField(read_only=True)

    class Meta:
        model = user_models.Assessment
        fields = ['course', 'title', 'description', 'question_area', 'due_date', 'time_remaining', 'is_overdue', 'ai_feedback', 'instructor_feedback']

    def get_time_remaining(self, obj):
        return obj.time_remaining()

    def get_is_overdue(self, obj):
        return obj.is_overdue()

    def __init__(self, *args, **kwargs):
        super(AssessmentSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class QuizSerializer(serializers.ModelSerializer):
    ai_feedback = serializers.CharField(read_only=True)
    instructor_feedback = serializers.CharField(read_only=True)

    class Meta:
        model = user_models.Quiz
        fields = ['course', 'title', 'description', 'question_area', 'time_limit', 'ai_feedback', 'instructor_feedback', 'max_score', 'show_scores']

    def __init__(self, *args, **kwargs):
        super(QuizSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class PlayGroundSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_models.PlayGround
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    students = serializers.StringRelatedField(many=True)
    assessments = AssessmentSerializer(many=True)
    quizzes = QuizSerializer(many=True)
    institution = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()
    
    class Meta:
        model = user_models.Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CourseSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    courses = CourseSerializer(many=True, read_only=True)
    assessments = AssessmentSerializer(many=True, read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)
    playgrounds = PlayGroundSerializer(many=True, read_only=True)
    scores = serializers.SerializerMethodField()

    class Meta:
        model = user_models.Student
        fields = '__all__'

    def get_scores(self, obj):
        submissions = user_models.Submission.objects.filter(student=obj)
        return SubmissionSerializer(submissions, many=True).data

    def __init__(self, *args, **kwargs):
        super(StudentSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
            
        




class CourseEnrollmentSerializer(serializers.ModelSerializer):
    assessments = AssessmentSerializer(many=True)
    quizzes = QuizSerializer(many=True)
    student = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()
        
    class Meta:
        model = user_models.CourseEnrollment
        fields = ['course', 'student', 'teacher', 'enrollment_id', 'enrollment_date', 'is_enrolled', 'assessments', 'quizzes']

    def __init__(self, *args, **kwargs):
        super(CourseEnrollmentSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
            
class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.CourseMaterial
        fields = '__all__'


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.Submission
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    courses = CourseSerializer(many=True)
    enrolled_students = CourseEnrollmentSerializer(many=True)

    class Meta:
        model = user_models.Teacher
        fields = '__all__'


class InstitutionSerializer(serializers.ModelSerializer):
    institution = serializers.StringRelatedField(many=False)

    class Meta:
        model = user_models.Institution
        fields = '__all__'

class ManagerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    institution = InstitutionSerializer()

    class Meta:
        model = user_models.Manager
        fields = '__all__'
        
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        # Update user fields
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update manager fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class InstitutionManagerSerializer(serializers.Serializer):
    # Institution fields
    name = serializers.CharField(max_length=255)
    logo = serializers.ImageField(required=False, allow_null=True)

    # Manager fields
    manager_name = serializers.CharField(max_length=100)
    contact_email = serializers.EmailField()
    contact_phone = serializers.CharField(max_length=20)

    def validate_contact_email(self, value):
        if user_models.User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists.")
        return value

    def validate(self, data):
        if user_models.Institution.objects.filter(name=data['name']).exists():
            raise serializers.ValidationError(
                "An institution with this name already exists.")
        return data

    def create(self, validated_data):
        institution = user_models.Institution.objects.create(
            name=validated_data['name'],
            logo=validated_data.get('logo')
        )

        user = user_models.User.objects.create_user(
            username=validated_data['contact_email'].split('@')[0],
            email=validated_data['contact_email'],
            password=get_random_string(12),
            user_role='manager'
        )

        user_models.Manager.objects.create(
            user=user,
            institution=institution,
            phone_number=validated_data['contact_phone']
        )

        return institution

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.Feedback
        fields = '__all__'

class IssueReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.IssueReport
        fields = '__all__'