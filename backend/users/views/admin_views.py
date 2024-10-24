from django.contrib.auth.password_validation import validate_password
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.conf import settings

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from ..models import User, Teacher, Student, Institution, Admin
from ..serializers import TeacherSerializer, StudentSerializer, UserSerializer

import random
import string
import pandas as pd
from io import BytesIO


class CreateUserView(generics.CreateAPIView):
    # This view is for adding a single user to the system
    serializer_class = UserSerializer
    # TODO: correct this permission class later "[IsAuthenticated, IsAdminUser]"
    permission_classes = [AllowAny]


    def create(self, request, *args, **kwargs):
        # Handle POST request to create a new user
        user_role = request.data['user_role']
        email = request.data['email']
        admin_id = request.data['admin_id']
        institution_id = request.data['institution_id']

        # Validate required fields
        if not user_role or not email or not institution_id:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure user_role is valid
        if user_role not in dict(User.USER_ROLES):
            return Response({'error': 'Invalid user role'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify if the institution exists
        institution = get_object_or_404(Institution, id=institution_id)

        # Check if the user already exists
        if User.objects.filter(email=email).exists():
            return Response({'error': 'A user with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a random password
        password = get_random_string(length=8)

        # Validate the generated password
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new user
        user = User.objects.create_user(
            username=email.split('@')[0],
            email=email,
            password=password,
            user_role=user_role,
            institution=institution
        )

        # Create a Teacher or Student object based on the user_role
        if user_role == 'teacher':
            profile = Teacher.objects.create(user=user, institution=institution)
            serializer = TeacherSerializer(profile)
        elif user_role == 'student':
            profile = Student.objects.create(user=user, institution=institution)
            serializer = StudentSerializer(profile)
        else:
            return Response({'error': 'Invalid user role'}, status=status.HTTP_400_BAD_REQUEST)

        # Get admin email
        admin = get_object_or_404(Admin, id=admin_id,  institution=institution)
        admin_email = admin.user.email

        # Send an email with the login credentials
        context = {
            "username": user.username,
            "email": email,
            "password": password,
            "user_role": user_role
        }

        subject = f"Your {user_role.capitalize(
        )} Account for Institution Management System"
        text_body = render_to_string('admin/create_new_user.txt', context)
        html_body = render_to_string('admin/create_new_user.html', context)
        message = EmailMultiAlternatives(
            subject=subject,
            from_email=admin_email,  # Use admin's email as the sender
            to=[user.email],  # Use the newly created user's email
            body=text_body,
        )

        message.attach_alternative(html_body, "text/html")
        message.send()

        # Return the serialized user data
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BulkAddUsersView(generics.CreateAPIView):
    # This view is for adding multiple users to the system from an Excel file
    # Only authenticated users can access this view
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    # This line specifies the parser classes that the view will use to handle incoming requests.
    # MultiPartParser is used for handling file uploads, while FormParser is for processing form data.
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        # Handle POST request to create multiple users
        file = request.FILES.get('file')
        user_role = request.data['user_role']
        institution_id = request.data['institution_id']

        # Check if all required fields are provided
        if not file:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify if the institution exists
        try:
            institution = Institution.objects.get(id=institution_id)
        except Institution.DoesNotExist:
            return Response({'error': 'Invalid institution'}, status=status.HTTP_400_BAD_REQUEST)

        # Read the Excel file
        try:
            df = pd.read_excel(BytesIO(file.read()))
        except Exception as e:
            return Response({'error': f'Error reading file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the Excel file has 'email'columns
        if 'email' not in df.columns:
            return Response({'error': 'Excel file must contain "email" column'}, status=status.HTTP_400_BAD_REQUEST)

        created_users = []
        errors = []

        # Get admin email
        admin = get_object_or_404(Admin, institution=institution)
        admin_email = admin.user.email

        # Iterate through each row in the Excel file
        for _, row in df.iterrows():
            email = row['email']
            # Generate a random password of 12 characters
            password = ''.join(random.choices(
                string.ascii_letters + string.digits, k=12))

            try:
                # Validate the generated password
                validate_password(password)
                # Create a new user
                user = User.objects.create_user(
                    username=email.split('@')[0],
                    email=email,
                    password=password,
                    user_role=user_role,
                    institution=institution
                )

                # Create a Teacher or Student object based on the user_role
                if user_role == 'teacher':
                    teacher = Teacher.objects.create(user=user, institution=institution)
                    serializer = TeacherSerializer(teacher)
                elif user_role == 'student':
                    student = Student.objects.create(user=user, institution=institution)
                    serializer = StudentSerializer(student)

                # Send an email with the login credentials
                context = {
                    "username": user.username,
                    "email": email,
                    "password": password,
                    "user_role": user_role
                }

                subject = f"Your {user_role.capitalize()} Account for Institution Management System"
                text_body = render_to_string('admin/create_new_user.txt', context)
                html_body = render_to_string('admin/create_new_user.html', context)
                message = EmailMultiAlternatives(
                    subject=subject,
                    from_email=admin_email,
                    to=[email],
                    body=text_body,
                )

                message.attach_alternative(html_body, "text/html")
                message.send()

                # This line appends the newly created user object to the created_users list.
                created_users.append(serializer.data)
            except Exception as e:
                errors.append(f"Error creating user {email}: {str(e)}")

        # Return the list of created users and any errors encountered
        return Response({
            'created_users': created_users,
            'errors': errors
        }, status=status.HTTP_201_CREATED if created_users else status.HTTP_400_BAD_REQUEST)


class TeacherStudentAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    # TODO: update permissions to IsOwnerOrAdmin
    permission_classes = [AllowAny]

    def get_queryset(self):
        institution_id = self.kwargs['institution_id']
        # user_type = self.kwargs['user_type']
        institution = Institution.objects.get(id=institution_id)
        
        # if user_type == 'teacher':
        #     return User.objects.filter(institution=institution, user_role='teacher')
        # elif user_type == 'student':
        #     return User.objects.filter(institution=institution, user_role='student')
        # else:
        return User.objects.filter(institution=institution)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })
class TeacherStudentDetail(generics.RetrieveUpdateDestroyAPIView):
    # TODO: update permissions to IsOwnerOrAdmin
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        user_type = self.kwargs['user_type']
        if user_type == 'teacher':
            return TeacherSerializer
        elif user_type == 'student':
            return StudentSerializer
        return UserSerializer

    def get_object(self):
        institution_id = self.kwargs['institution_id']
        user_id = self.kwargs['teacher_id'] or self.kwargs['student_id']
        user_type = self.kwargs['user_type']
        institution = Institution.objects.get(id=institution_id)
        
        if user_type == 'teacher':
            return get_object_or_404(Teacher, id=user_id, institution=institution)
        elif user_type == 'student':
            return get_object_or_404(Student, id=user_id, institution=institution)
        return get_object_or_404(User, id=user_id, institution=institution)







