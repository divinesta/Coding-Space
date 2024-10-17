from django.contrib.auth.password_validation import validate_password
from django.apps import apps

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Import User models dynamically
User = apps.get_model('users', 'User')
Manager = apps.get_model('users', 'Manager')
Institution = apps.get_model('users', 'Institution')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(read_only=True)
    user_role = serializers.CharField(read_only=True)
    role_id = serializers.IntegerField(read_only=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add standard claims
        token['email'] = user.email
        token['username'] = user.username
        token['user_role'] = user.user_role

        # Add role-specific claim
        if user.user_role == 'teacher' and hasattr(user, 'teacher_profile'):
            token['teacher_id'] = user.teacher_profile.id
        elif user.user_role == 'student' and hasattr(user, 'student_profile'):
            token['student_id'] = user.student_profile.id
        elif user.user_role == 'admin' and hasattr(user, 'admin_profile'):
            token['admin_id'] = user.admin_profile.id
        elif user.user_role == 'manager' and hasattr(user, 'manager_profile'):
            token['manager_id'] = user.manager_profile.id
        else:
            token['role_id'] = None  # Or omit this field

        return token


class RegisterSerializer(serializers.ModelSerializer):
    manager_email = serializers.EmailField(write_only=True)
    manager_password = serializers.CharField(write_only=True)

    class Meta:
        model = Institution
        fields = ['name', 'manager_email', 'manager_password', 'logo']  # Include 'logo' if necessary

    def create(self, validated_data):
        manager_email = validated_data.pop('manager_email')
        manager_password = validated_data.pop('manager_password')

        # Create institution
        institution = Institution.objects.create(**validated_data)

        # Create manager user
        manager_user = User.objects.create_user(
            username=manager_email.split('@')[0],
            email=manager_email,
            password=manager_password,
            user_role='manager',
            institution=institution
        )

        # Create manager profile
        Manager.objects.create(user=manager_user, institution=institution)

        return institution


# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()


class PasswordChangeSerializer(serializers.Serializer):
    # Fields for changing password
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

class PasswordResetSerializer(serializers.Serializer):
    # Fields for resetting password
    uuidb64 = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)