

from django.test import TestCase
from account.core.forms.login_form import LoginForm
from django.contrib.auth import get_user_model


class LoginFormTestCase(TestCase):

    def test_form_is_valid(self):
        form = LoginForm(data={'email': 'k@gmail.com', 'password': 'pass1'})
        self.assertTrue(form.is_valid())

    def test_form_is_invalid(self):
        form = LoginForm(data={'email': '', 'password': 'pass1'})

        self.assertFalse(form.is_valid())

    def test_form_validation_messages(self):
        form = LoginForm(data={'email': '', 'password': 'pass1'})
        self.assertIn('Please enter your email address.', form.errors['email'])

        form = LoginForm(data={'email': 'bad mail', 'password': 'pass1'})
        self.assertIn('Enter a valid email address.', form.errors['email'])

        form = LoginForm(data={'email': 'b@gmail.com', 'password': ''})
        self.assertIn('Please enter your password.', form.errors['password'])

