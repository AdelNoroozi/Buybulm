from rest_framework.permissions import BasePermission, SAFE_METHODS

from accounts.models import Admin, Profile
from music_bot.models import Song
from store.models import Payment


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
        if request.method in SAFE_METHODS or view.action == 'add_play':
            return True
        if user.is_superuser:
            return True
        if user.is_staff:
            if not Admin.objects.filter(parent_base_user=user).exists():
                return False
            admin = Admin.objects.get(parent_base_user=user)
            return admin.section == 'B'

    def has_object_permission(self, request, view, obj: Song):
        if not isinstance(obj, Song):
            return True
        else:
            user = request.user
            if user.is_superuser:
                return True
            if user.is_staff:
                if not Admin.objects.filter(parent_base_user=user).exists():
                    return False
                admin = Admin.objects.get(parent_base_user=user)
                return admin.section == 'B'
            if (obj.album is None) or obj.album.is_public:
                return True
            else:
                try:
                    profile = Profile.objects.get(parent_base_user=user)
                except:
                    return False
                return Payment.objects.filter(album=obj.album, user=profile).exists()


class PlaySongPermission(BasePermission):
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

    def has_object_permission(self, request, view, obj: Song):
        if (obj.album is None) or obj.album.is_public:
            return True
        else:
            try:
                user = request.user
                profile = Profile.objects.get(parent_base_user=user)
            except:
                return False
            return Payment.objects.filter(album=obj.album, user=profile).exists()


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
