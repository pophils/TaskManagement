
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, first_name, password=None):

        if not email:
            raise ValueError('the email address for a user must be provided.')
        if not first_name:
            raise ValueError('the user first name must be provided.')

        if not password:
            raise ValueError('the user password must be provided.')

        user = self.model(email=self.normalize_email(email), first_name=first_name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, password):
        if not password:
            raise ValueError('the user must have a password.')

        user = self.create_user(email, first_name, password)
        user.is_admin = True
        user.is_superuser = True

        user.save(using=self._db)

        return user
