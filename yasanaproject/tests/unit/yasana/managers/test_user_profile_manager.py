

from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserManagerTestCase(TestCase):

    def setUp(self):
        self.User = get_user_model()

    def tearDown(self):
        if self.User is not None:
            self.User = None

    def test_create_user_can_save(self):
        user = self.User.objects.create_user(email='email@gmail.com', first_name='sean', password='pass1')

        saved_users = self.User.objects.all()

        self.assertEqual(saved_users.count(), 1, 'create_user save error.')
        first_user = saved_users[0]
        self.assertEqual(user.email, first_user.email)
        self.assertEqual(user.first_name, first_user.first_name)

    def test_create_super_user_can_save(self):
        user = self.User.objects.create_user(email='email@gmail.com', first_name='sean', password='pass1')

        saved_users = self.User.objects.all()

        self.assertEqual(saved_users.count(), 1, 'create_user save error.')
        first_user = saved_users[0]
        self.assertEqual(user.email, first_user.email)
        self.assertEqual(user.first_name, first_user.first_name)

    def test_create_user_raise_value_error_and_cannot_save_on_invalid_data(self):

        with self.assertRaises(ValueError):
            self.User.objects.create_user(email='', first_name='sean', password='pass1')
            self.User.objects.create_user(email='email@gmail.com', first_name='', password='pass1')
            self.User.objects.create_user(email='email@gmail.com', first_name='sean', password='')

        self.assertEqual(self.User.objects.count(), 0, 'create_user save on invalid data.')

    def test_create_superuser_raise_value_error_and_cannot_save_on_invalid_data(self):

        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(email='', first_name='sean', password='pass1')
            self.User.objects.create_superuser(email='email@gmail.com', first_name='', password='pass1')
            self.User.objects.create_superuser(email='email@gmail.com', first_name='sean', password='')

        self.assertEqual(self.User.objects.count(), 0, 'create_superuser save on invalid data.')

    def test_create_super_user_save_correctly(self):
        user = self.User.objects.create_superuser(email='email@gmail.com', first_name='sean', password='pass1')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_admin)

