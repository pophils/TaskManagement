

from django.test import TestCase
from django.contrib.auth import get_user_model
from account.core.forms.create_user_form import CreateUserForm
# from unittest import skip


class CreateUserFormTestCase(TestCase):

    def test_form_is_valid(self):
        form = CreateUserForm(data={'email': 'k@gmail.com', 'password': 'pass1', 'first_name': 'name1',
                                    'confirm_password': 'pass1', 'gender': 'm', 'phone': '+23470876564'})
        self.assertTrue(form.is_valid())

    def test_form_is_invalid(self):
        form = CreateUserForm(data={'email': '', 'password': 'pass1', 'first_name': 'name1',
                                    'confirm_password': 'pass1', 'gender': 'm'})
        self.assertFalse(form.is_valid())

        form = CreateUserForm(data={'email': 'invalid email', 'password': 'pass1', 'first_name': 'name1',
                                    'confirm_password': 'pass1', 'gender': 'm'})
        self.assertFalse(form.is_valid())

        form = CreateUserForm(data={'email': 'k@gmail.com', 'password': '', 'first_name': 'name1',
                                    'confirm_password': 'pass1', 'gender': 'm'})
        self.assertFalse(form.is_valid())

        form = CreateUserForm(data={'email': 'k@gmail.com', 'password': 'pass1', 'first_name': '',
                                    'confirm_password': 'pass1', 'gender': 'm'})
        self.assertFalse(form.is_valid())

        form = CreateUserForm(data={'email': 'k@gmail.com', 'password': 'pass1', 'first_name': 'name1',
                                    'confirm_password': '', 'gender': 'm'})
        self.assertFalse(form.is_valid())

        form = CreateUserForm(data={'email': 'k@gmail.com', 'password': 'pass1', 'first_name': 'name1',
                                    'confirm_password': 'pass1', 'gender': ''})
        self.assertFalse(form.is_valid())

        form = CreateUserForm(data={'email': 'k@gmail.com', 'password': 'pass1', 'first_name': 'name1',
                                    'confirm_password': 'pass2', 'gender': 'm'})
        self.assertFalse(form.is_valid())

        form = CreateUserForm(data={'email': 'k@gmail.com', 'password': 'pass1', 'first_name': 'name1',
                                    'confirm_password': 'pass1', 'gender': '-1'})
        self.assertFalse(form.is_valid())

        form = CreateUserForm(data={'email': 'k@gmail.com', 'password': 'pass1', 'first_name': 'name1',
                                    'confirm_password': 'pass1', 'gender': 'm', 'phone': 'invalid_phone_number'})
        self.assertFalse(form.is_valid())

        get_user_model().objects.create_user(email='k@gmail.com', first_name='name1', password='pass1')

        form = CreateUserForm(data={'email': 'k@gmail.com', 'password': 'pass1', 'first_name': 'name1',
                                    'confirm_password': 'pass1', 'gender': 'm'})
        self.assertFalse(form.is_valid())

    def test_form_validation_messages(self):
        form = CreateUserForm(data={'email': '', 'password': 'pass1', 'first_name': 'name1',
                                    'confirm_password': 'pass1', 'gender': 'm'})
        self.assertIn('Please enter email address.', form.errors['email'])

        form = CreateUserForm(data={'email': 'gmail', 'password': 'pass1', 'first_name': 'name1',
                                    'confirm_password': 'pass1', 'gender': 'm'})
        self.assertIn('Please enter a valid email address.', form.errors['email'])

        form = CreateUserForm(data={'email': 'k@gmail.com', 'password': '', 'first_name': 'name1',
                                    'confirm_password': 'pass1', 'gender': 'f'})
        self.assertIn('Please enter password.', form.errors['password'])

        form = CreateUserForm(data={'email': 'k@gmail.com', 'password': 'pass1', 'first_name': 'name1',
                                    'confirm_password': '', 'gender': 'p'})
        self.assertIn('Please confirm entered password.', form.errors['confirm_password'])

        form = CreateUserForm(data={'email': 'k@gmail.com', 'password': 'pass1', 'first_name': 'name1',
                                    'confirm_password': 'pass2', 'gender': 'm'})
        self.assertIn('Password confirmation does not match.', form.errors['confirm_password'])

        form = CreateUserForm(data={'email': 'k@gmail.com', 'password': 'pass1', 'first_name': '',
                                    'confirm_password': 'pass1', 'gender': 'm'})
        self.assertIn('Please enter first name.', form.errors['first_name'])

        form = CreateUserForm(data={'email': 'k@gmail.com', 'password': 'pass1', 'first_name': 'name1',
                                    'confirm_password': 'pass1', 'gender': ''})
        self.assertIn('Please select a gender.', form.errors['gender'])

        form = CreateUserForm(data={'email': 'k@gmail.com', 'password': 'pass1', 'first_name': 'name1',
                                    'confirm_password': 'pass1', 'gender': '-1'})
        self.assertIn('Please select a valid gender.', form.errors['gender'])

        form = CreateUserForm(data={'email': 'k@gmail.com', 'password': 'pass1', 'first_name': 'name1',
                                    'confirm_password': 'pass1', 'gender': 'm', 'phone': 'invalid_phone_number'})

        self.assertIn('Phone number is invalid.', form.errors['phone'])

        get_user_model().objects.create_user(email='k@gmail.com', first_name='name1', password='pass1')

        form = CreateUserForm(data={'email': 'k@gmail.com', 'password': 'pass1', 'first_name': 'name1',
                                    'confirm_password': 'pass1', 'gender': 'm'})
        self.assertIn('Please enter a new email address, email already exist.', form.errors['email'])
