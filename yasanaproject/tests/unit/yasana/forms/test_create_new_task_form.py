

from django.test import TestCase
from yasana.core.forms.task_form import CreateTaskForm
# from unittest import skip


class CreateUserFormTestCase(TestCase):

    def test_form_is_valid(self):
        form = CreateTaskForm(data={'title': 'task a', 'details': 'details a', 'priority': '0',
                                    'start_date': '10/12/2015', 'expected_end_date': '12/10/2016'})
        self.assertTrue(form.is_valid())

    def test_form_is_invalid(self):
        form = CreateTaskForm(data={'title': '', 'details': 'details a', 'priority': '0',
                                    'start_date': '10/12/2015', 'expected_end_date': '12/10/2016'})
        self.assertFalse(form.is_valid())

        form = CreateTaskForm(data={'title': 'task a', 'details': '', 'priority': '0',
                                    'start_date': '10/12/2015', 'expected_end_date': '12/10/2016'})
        self.assertFalse(form.is_valid())

        CreateTaskForm(data={'title': 'task a', 'details': 'details a', 'priority': '',
                             'start_date': '10/12/2015', 'expected_end_date': '12/10/2016'})
        self.assertFalse(form.is_valid())

        form = CreateTaskForm(data={'title': 'task a', 'details': 'details a', 'priority': '12',
                                    'start_date': '10/12/2015', 'expected_end_date': '12/10/2016'})
        self.assertFalse(form.is_valid())

    def test_form_validation_messages(self):

        form = CreateTaskForm(data={'title': '', 'details': 'details a', 'priority': '0',
                                    'start_date': '10/12/2015', 'expected_end_date': '12/10/2016'})
        self.assertIn('Please enter task title.', form.errors['title'])

        form = CreateTaskForm(data={'title': 'task a', 'details': '', 'priority': '0',
                                    'start_date': '10/12/2015', 'expected_end_date': '12/10/2016'})
        self.assertIn('Please enter task details.', form.errors['details'])

        form = CreateTaskForm(data={'title': 'task a', 'details': 'details a', 'priority': '12',
                                    'start_date': '10/12/2015', 'expected_end_date': '12/10/2016'})
        self.assertIn('Please select a valid priority.', form.errors['priority'])
