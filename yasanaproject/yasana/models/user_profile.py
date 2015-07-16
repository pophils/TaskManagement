

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .abstract_base_entity import AbstractBaseEntity
from .organisation import Organisation
from ..core.Managers.custom_user_manager import CustomUserManager


class UserProfile(AbstractBaseEntity, AbstractBaseUser, PermissionsMixin):
    Gender_Choices = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('p', 'Prefer not to say')
    )

    email = models.EmailField(max_length=255, db_index=True, db_column='EmailAddress', verbose_name='Email Address',
                              unique=True)
    first_name = models.CharField(max_length=255)
    other_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True, unique=True, db_index=True)
    is_confirmed = models.BooleanField(default=False)
    website = models.URLField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=Gender_Choices, default='p')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    organisation = models.ForeignKey(Organisation, null=True, blank=True, default=None, related_name='users')

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    @property
    def is_staff(self):
        return self.is_admin

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return '%s %s, %s' % (self.first_name, self.other_name, self.last_name)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        db_table = 'UserProfile'
