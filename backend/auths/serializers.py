from django.contrib.auth.password_validation import validate_password
from django.apps import apps

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Import User models dynamically
User = apps.get_model('users', 'User')
Manager = apps.get_model('users', 'Manager')
Institution = apps.get_model('users', 'Institution')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims to the token
        token['email'] = user.email
        token['username'] = user.username
        try:
            token['teacher_id'] = user.teacher.id
            token['student_id'] = user.student.id
            token['admin_id'] = user.admin.id
            token['manager_id'] = user.manager.id
        except:
            # If user is not a teacher, set teacher_id to 0
            token['teacher_id'] = 0
            token['student_id'] = 0
            token['admin_id'] = 0
            token['manager_id'] = 0

        return token

class RegisterSerializer(serializers.ModelSerializer):
    manager_email = serializers.EmailField()
    manager_password = serializers.CharField(write_only=True)

    class Meta:
        model = Institution
        fields = ['name', 'manager_email', 'manager_password']


    def create(self, validated_data):
        manager_email = validated_data.pop('manager_email')
        manager_password = validated_data.pop('manager_password')

        institution = Institution.objects.create(**validated_data)

        manager_user = User.objects.create_user(
            username=manager_email,
            email=manager_email,
            password=manager_password,
            user_role='manager',
            institution=institution
        )
        
        

        Manager.objects.create(user=manager_user, institution=institution)

        return institution


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class PasswordChangeSerializer(serializers.Serializer):
    # Fields for changing password
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

class PasswordResetSerializer(serializers.Serializer):
    # Fields for resetting password
    uuidb64 = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)