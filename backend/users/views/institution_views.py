from django.shortcuts import get_object_or_404
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..serializers import InstitutionSerializer, InstitutionManagerSerializer, UserSerializer, AdminSerializer
from ..permissions import IsOwnerOrAdmin
from ..models import Institution, Manager, User, Admin


# TODO: Implement payment logic: When payment has been successful, change the
# institution status to 'paid', and set active to True

class InstitutionManagerCreateView(generics.CreateAPIView):
    serializer_class = InstitutionManagerSerializer
    permission_classes = [AllowAny]
    

    def perform_create(self, serializer):
        if serializer.is_valid():
            # Create Institution
            institution = Institution.objects.create(
                name=serializer.validated_data['name'],
                logo=serializer.validated_data.get('logo'),
                subscription_status='trial'
            )

            # Create User for Manager
            user = User.objects.create_user(
                username=serializer.validated_data['contact_email'].split('@')[0],
                email=serializer.validated_data['contact_email'],
                user_role='manager',
                institution=institution
            )

            # Create Manager
            Manager.objects.create(
                user=user,
                institution=institution,
                email=serializer.validated_data['contact_email'],
                phone_number=serializer.validated_data['contact_phone']
            )

            # TODO: Implement payment processing logic here
            # For example:
            # process_payment(serializer.validated_data['payment_info'])
            # if payment_successful:
            #     institution.subscription_status = 'paid'
            #     institution.save()

            return Response({"message": "Institution and Manager created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstitutionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InstitutionManagerSerializer
    # TODO: update permissions
    permission_classes = [AllowAny]

    def get_object(self):
        institution_id = self.kwargs['institution_id']
        institution = get_object_or_404(Institution, id=institution_id)
        return institution
    


#TODO: Add link to this view 👇 for the login page in the email

class CreateAdminView(generics.CreateAPIView):
    serializer_class = UserSerializer
    # TODO: update permissions to IsOwnerOrAdmin
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Handle POST request to create a new user
        email = request.data['email']
        institution_id = request.data['institution_id']
        user_role = "admin"
        
        # Validate required fields
        if  not email or not institution_id:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify if the institution exists
        institution = get_object_or_404(Institution, id=institution_id)
        
        # Check if the user already exists
        if User.objects.filter(email=email).exists():
            return Response({'error': 'A user with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate a secure random password
        password = get_random_string(length=8)
        
        # Validate the generated password
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
        # Get manager email
        manager = get_object_or_404(Manager, institution=institution)
        manager_email = manager.user.email
        
        # Create a new user
        user = User.objects.create_user(
            username=email.split('@')[0],
            email=email,
            password=password,
            user_role=user_role,
            institution=institution
        )
        
        # Create a Admin object based on the user_role
        if user_role == 'admin':
            profile = Admin.objects.create(user=user, institution=institution)
            serializer = AdminSerializer(profile)
        else:
            return Response({'error': 'Invalid user role'}, status=status.HTTP_400_BAD_REQUEST)

        # Send email with login details
        context = {
            "username": user.username,
            "password": password,
            "email": email
        }
        subject = "Your Admin Account for Institution Management System"
        text_body = render_to_string('manager/create_admin.txt', context)
        html_body = render_to_string('manager/create_admin.html', context)
        message = EmailMultiAlternatives(
            subject=subject,
            from_email=manager_email,  # Use manager's email as the sender
            to=[user.email],
            body=text_body,
        )
        message.attach_alternative(html_body, "text/html")
        message.send()

        # Return the serialized user data
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class AdminList(generics.ListAPIView):
    serializer_class = AdminSerializer
    # TODO: update permissions to IsOwnerOrAdmin
    permission_classes = [AllowAny]

    def get_queryset(self):
        institution_id = self.kwargs['institution_id']
        institution = get_object_or_404(Institution, id=institution_id)
        return Admin.objects.filter(institution=institution)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })

class AdminDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdminSerializer
    # TODO: update permissions to IsOwnerOrAdmin
    permission_classes = [AllowAny]

    def get_object(self):
        institution_id = self.kwargs['institution_id']
        admin_id = self.kwargs['admin_id']
        institution = get_object_or_404(Institution, id=institution_id)
        return get_object_or_404(Admin, id=admin_id, institution=institution)
