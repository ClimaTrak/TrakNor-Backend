"""Role-based permission classes."""

from rest_framework.permissions import BasePermission

from traknor.infrastructure.accounts.user import User


class IsAdmin(BasePermission):
    """Allow access only to admin users."""

    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.role == User.Roles.ADMIN)


class IsManager(BasePermission):
    """Allow access only to manager users."""

    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.role == User.Roles.MANAGER)


class IsTechnician(BasePermission):
    """Allow access only to technician users."""

    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.role == User.Roles.TECHNICIAN)
