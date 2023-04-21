from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_superuser=False):
        if not email:
            raise ValueError('email is required')
        if not password:
            raise ValueError('password is required')
        user_instance = self.model(
            email=email
        )
        user_instance.password = make_password(password)
        user_instance.is_staff = is_staff
        user_instance.is_superuser = is_superuser
        user_instance.is_active = is_active
        user_instance.save(using=self._db)
        return user_instance

    def create_admin(self, email, password=None):
        admin = self.create_user(
            email=email,
            password=password
        )
        admin.is_staff = True
        admin.is_superuser = False
        admin.save(using=self._db)
        return admin

    def create_superuser(self, email, password=None):
        superuser = self.create_user(
            email=email,
            password=password
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save(using=self._db)
        return superuser


class BaseUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_('last modification'))
    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('Base User')
        verbose_name_plural = _('Base Users')

