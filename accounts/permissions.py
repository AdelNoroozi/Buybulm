from rest_framework.permissions import BasePermission, SAFE_METHODS


class NotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_anonymous


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff
