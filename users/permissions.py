from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminUser(BasePermission):
    """
    Custom permission to grant full access to admins only.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow read-only access to users, but full access to admins.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  # Read access for everyone
        return (
            request.user.is_authenticated and request.user.is_staff
        )  # Full access for admin


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission:
    - Admins can CREATE, UPDATE, DELETE.
    - Authenticated users can only READ (GET requests).
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.is_staff
