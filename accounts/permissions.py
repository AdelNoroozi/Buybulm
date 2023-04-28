from rest_framework.permissions import BasePermission, SAFE_METHODS

from accounts.models import Admin


class NotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_anonymous


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsUserAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser:
            return True
        if (not Admin.objects.filter(parent_base_user=user).exists()) or (not user.is_staff):
            return False
        admin = Admin.objects.get(parent_base_user=user)
        return admin.section == 'U'


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAuthenticatedAndNormalUser(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_staff


class BotPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in SAFE_METHODS:
            return True
        if user.is_superuser:
            return True
        if user.is_staff:
            if not Admin.objects.filter(parent_base_user=user).exists():
                return False
            admin = Admin.objects.get(parent_base_user=user)
            return admin.section == 'B'


class StorePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser:
            return True
        if user.is_staff:
            try:
                admin = Admin.objects.get(parent_base_user=user)
            except:
                return False
            return admin.section == 'S'
        return False
