

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .abstract_base_entity import AbstractBaseEntity
from ..core.managers.custom_user_manager import CustomUserManager


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
    department = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    image_src = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=Gender_Choices, default='p')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    @property
    def is_staff(self):
        return self.is_admin

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):

        if self.other_name and not self.last_name:
            return '%s %s' % (self.first_name, self.other_name)
        elif not self.other_name and self.last_name:
            return '%s, %s' % (self.last_name, self.first_name)
        elif self.other_name and self.last_name:
            return '%s, %s %s' % (self.last_name, self.first_name, self.other_name)

        return self.first_name

    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        if self.first_name:
            self.first_name = self.first_name.capitalize()
        if self.other_name:
            self.other_name = self.other_name.capitalize()
        if self.last_name:
            self.last_name = self.last_name.capitalize()
        if self.department:
            self.department = self.department.capitalize()

        super().save(*args, **kwargs)


    class Meta:
        db_table = 'UserProfile'
        permissions = (
            ('can_manage_users', 'Can manage users'),
        )
