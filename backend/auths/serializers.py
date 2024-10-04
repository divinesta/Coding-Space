from django.contrib.auth.password_validation import validate_password
from django.apps import apps

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Import User models dynamically
User = apps.get_model('users', 'User')
Teacher = apps.get_model('users', 'Teacher')
Student = apps.get_model('users', 'Student')
Institution = apps.get_model('users', 'Institution')
Profile = apps.get_model('users', 'Profile')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims to the token
        token['email'] = user.email
        token['username'] = user.username
        try:
            token['teacher_id'] = user.teacher.id
        except:
            # If user is not a teacher, set teacher_id to 0
            token['teacher_id'] = 0

        return token

class RegisterSerializer(serializers.ModelSerializer):
    # Define password fields with write-only access and validation
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    institution = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'institution', 'user_type', 'password', 'password2']

    def validate(self, attr):
        # Check if passwords match
        if attr['password'] != attr['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match"})

        return attr

    def create(self, validated_data):
        # Extract institution name from validated data
        institution_name = validated_data.pop('institution', None)

        # Get or create institution if provided
        if institution_name:
            institution, _ = Institution.objects.get_or_create(name=institution_name)
        else:
            institution = None

        # Create user instance
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            institution=institution,
            user_type=validated_data['user_type']
        )

        # Set password and save user
        user.set_password(validated_data['password'])
        user.save()

        # Create user profile
        Profile.objects.create(user=user)

        # Create Teacher or Student instance based on user_type
        if user.user_type == 'Instructor':
            Teacher.objects.create(user=user)
        elif user.user_type == 'Student':
            Student.objects.create(user=user)

        return user

class PasswordChangeSerializer(serializers.Serializer):
    # Fields for changing password
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

class PasswordResetSerializer(serializers.Serializer):
    # Fields for resetting password
    uuidb64 = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)