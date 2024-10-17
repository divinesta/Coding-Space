from rest_framework import permissions
from .models import Teacher, Student, Admin, Institution

class IsOwner(permissions.BasePermission):
    """
    Allows access only to Owners of the institution.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the object is an Institution and if the request user is the owner
        if isinstance(obj, Institution):
            return obj.owner == request.user
        return False
    

class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_role == 'admin')


class IsManagerUser(permissions.BasePermission):
    """
    Allows access only to manager users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_role == 'manager')

class IsAdmin(permissions.BasePermission):
    """
    Allows access only to Admins of the institution.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_role == 'admin'

    def has_object_permission(self, request, view, obj):
        # Check if the object is an Institution and if the user is an admin of that institution
        if isinstance(obj, Institution):
            return Admin.objects.filter(user=request.user, institution=obj).exists()
        return False

class IsTeacher(permissions.BasePermission):
    """
    Allows access only to Teachers.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_role =='teacher'


class IsStudent(permissions.BasePermission):
    """
    Allows access only to Students.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_role == 'student'

class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission to allow Owners or Admins.
    """

    def has_permission(self, request, view):
        # Check if the user is an admin or a superuser
        return hasattr(request.user, 'admin') or request.user.is_superuser

# class IsOwnerOrAdmin(permissions.BasePermission):
#     """
#     Custom permission to allow Owners or Admins for object-level permissions.
#     """

#     def has_object_permission(self, request, view, obj):
#         # Check if the object is an Institution and if the user is either the owner or an admin
#         if isinstance(obj, Institution):
#             return obj.owner == request.user or Admin.objects.filter(user=request.user, institution=obj).exists()
#         return False
    

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow access to Owners (Managers) or Admins.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (hasattr(request.user, 'manager') or hasattr(request.user, 'admin'))


class IsTeacherOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow teachers of a course to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only access for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check if the user is a teacher and if they are the teacher of the course
        return hasattr(request.user, 'teacher') and obj.teacher == request.user.teacher
