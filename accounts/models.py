from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
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
        if self.is_superuser:
            type_string = 'superuser'
        elif self.is_staff:
            type_string = 'admin'
        else:
            type_string = 'user'
        return f'{self.email}-{type_string}'

    class Meta:
        verbose_name = _('Base User')
        verbose_name_plural = _('Base Users')


class Profile(models.Model):
    phone_regex_validator = RegexValidator(
        regex=r'^(09)\d{9}$',
        message='invalid phone number'
    )
    parent_base_user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='profile',
                                            verbose_name=_('parent base user'))
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('first name'))
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('last name'))
    phone_number = models.CharField(validators=[phone_regex_validator], max_length=20, blank=True, null=True,
                                    verbose_name=_('phone number'))
    avatar = models.ImageField(blank=True, null=True, verbose_name='avatar',
                               upload_to='images/',
                               )

    def __str__(self):
        return self.parent_base_user.email

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')


class Admin(models.Model):
    SECTIONS = (('B', 'bot'),
                ('S', 'store'),
                ('UD', 'undefined'))
    parent_base_user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='admin',
                                            verbose_name=_('parent base user'))
    section = models.CharField(max_length=10, choices=SECTIONS, verbose_name=_('section'))

    def __str__(self):
        if self.section == 'B':
            section_string = 'bot'
        elif self.section == 'S':
            section_string = 'store'
        elif self.section == 'UD':
            section_string = 'undefined'

        return f'{self.parent_base_user.email}-{section_string} section'
