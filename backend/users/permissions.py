from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Allows access only to Owners of the institution.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsAdmin(permissions.BasePermission):
    """
    Allows access only to Admins of the institution.
    """

    def has_permission(self, request, view):
        return request.user.user_role == 'admin'

    def has_object_permission(self, request, view, obj):
        return request.user in obj.admins.all()

class IsTeacher(permissions.BasePermission):
    """
    Allows access only to Teachers.
    """

    def has_permission(self, request, view):
        return request.user.user_role == 'teacher'

class IsStudent(permissions.BasePermission):
    """
    Allows access only to Students.
    """

    def has_permission(self, request, view):
        return request.user.user_role == 'student'

class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission to allow Owners or Admins.
    """

    def has_permission(self, request, view):
        return request.user.user_role in ['admin', 'owner']

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow Owners or Admins for object-level permissions.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.user_role == 'owner' or (request.user.user_role == 'admin' and request.user in obj.admins.all())

class IsTeacherOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow teachers of a course to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.teacher.user == request.user
