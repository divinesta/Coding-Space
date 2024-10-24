from django.contrib.auth.password_validation import validate_password
from django.apps import apps

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Import User models dynamically
User = apps.get_model('users', 'User')
Manager = apps.get_model('users', 'Manager')
Institution = apps.get_model('users', 'Institution')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = User.objects.filter(email=email).first()

            if user and user.check_password(password):
                # Set username for parent class
                attrs['username'] = user.username
                data = super().validate(attrs)
                data.update({
                    'user': {
                        'username': user.username,
                        'email': user.email,
                        'role': user.user_role,
                    }
                })
                return data
            else:
                raise serializers.ValidationError(
                    'Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError(
                'Must include "email" and "password".')

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['user_role'] = user.user_role
        token['institution_id'] = user.institution.id

        if user.user_role == 'teacher' and hasattr(user, 'teacher_profile'):
            token['teacher_id'] = user.teacher_profile.id
        elif user.user_role == 'student' and hasattr(user, 'student_profile'):
            token['student_id'] = user.student_profile.id
        elif user.user_role == 'admin' and hasattr(user, 'admin_profile'):
            token['admin_id'] = user.admin_profile.id
        elif user.user_role == 'manager' and hasattr(user, 'manager_profile'):
            token['manager_id'] = user.manager_profile.id
        else:
            token['role_id'] = None

        return token


class RegisterSerializer(serializers.ModelSerializer):
    manager_email = serializers.EmailField(write_only=True)
    manager_contact = serializers.CharField(write_only=True)
    manager_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    manager_confirm_password = serializers.CharField(write_only=True)
    

    class Meta:
        model = Institution
        fields = ['name', 'manager_email', 'manager_contact', 'manager_password', 'manager_confirm_password']

    def validate(self, attrs):
        if attrs['manager_password'] != attrs['manager_confirm_password']:
            raise serializers.ValidationError({"manager_password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        manager_email = validated_data.pop('manager_email')
        manager_contact = validated_data.pop('manager_contact')
        manager_password = validated_data.pop('manager_password')
        manager_confirm_password = validated_data.pop('manager_confirm_password')

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

        manager_user.set_password(manager_password)
        manager_user.save()

        # Create manager profile
        Manager.objects.create(user=manager_user, institution=institution, phone_number=manager_contact)

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