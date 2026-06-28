from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    """
    Permission class to check if the authenticated user is a student.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == "student"


class IsAdminUser(permissions.BasePermission):
    """
    Permission class to check if the authenticated user is an admin or superadmin.
    Uses Django's is_staff or is_superuser flags for admin identification.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)
