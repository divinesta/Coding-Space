from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..serializers import InstitutionSerializer, InstitutionManagerSerializer, AdminCreationSerializer, AdminSerializer
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
    serializer_class = AdminCreationSerializer
    # TODO: update permissions to IsOwnerOrAdmin
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        institution = self.request.user.institution
        admin = serializer.save(institution=institution)
        
        # Generate a secure random password
        password = User.objects.make_random_password(length=12)
        admin.user.set_password(password)
        admin.user.save()

        # Get manager email
        manager = get_object_or_404(Manager, institution=institution)
        manager_email = manager.user.email

        # Send email with login details
        context = {
            "username": admin.user.username,
            "password": password,
            "email": admin.user.email,
        }
        subject = "Your Admin Account for Institution Management System"
        text_body = render_to_string('manager/create_admin.txt', context)
        html_body = render_to_string('manager/create_admin.html', context)
        message = EmailMultiAlternatives(
            subject=subject,
            from_email=manager_email,  # Use manager's email as the sender
            to=[admin.user.email],
            body=text_body,
        )
        message.attach_alternative(html_body, "text/html")
        message.send()

        return admin

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        admin = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": f"Admin account created successfully for {admin.user.email}. An email with login details has been sent."},
            status=status.HTTP_201_CREATED,
            headers=headers
        )
        
class AdminList(generics.ListAPIView):
    serializer_class = AdminSerializer
    # TODO: update permissions to IsOwnerOrAdmin
    permission_classes = [AllowAny]

    def get_queryset(self):
        institution = self.request.user.institution
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
        institution = self.request.user.institution
        admin_id = self.kwargs['id']
        return get_object_or_404(Admin, id=admin_id, institution=institution)
