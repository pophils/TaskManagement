

from django.test import TestCase
from account.core.forms.edit_user_form import EditUserForm


class CreateUserFormTestCase(TestCase):

    def test_form_is_valid(self):
        form = EditUserForm(data={'first_name': 'name2', 'last_name': 'larry', 'other_name': 'page',
                                  'phone': '0768040383', 'gender': "f", 'department': 'Deep Learning.',
                                  'email': 'name@name.com'})
        self.assertTrue(form.is_valid())

    def test_form_is_invalid(self):
        form = EditUserForm(data={'first_name': '', 'last_name': 'larry', 'other_name': 'page',
                                  'phone': '0768040383', 'gender': "f", 'department': 'Deep Learning.',
                                  'email': 'name@name.com'})
        self.assertFalse(form.is_valid())

        form = EditUserForm(data={'first_name': 'name2', 'last_name': 'larry', 'other_name': 'page',
                                  'phone': '0768040383', 'gender': "", 'department': 'Deep Learning.',
                                  'email': 'name@name.com'})
        self.assertFalse(form.is_valid())

        form = EditUserForm(data={'first_name': 'name2', 'last_name': 'larry', 'other_name': 'page',
                                  'phone': '0768040383', 'gender': "-1", 'department': 'Deep Learning.',
                                  'email': 'name@name.com'})
        self.assertFalse(form.is_valid())
