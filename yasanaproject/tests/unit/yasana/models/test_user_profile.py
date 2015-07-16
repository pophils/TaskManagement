
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


# noinspection PyCallingNonCallable
class UserProfileTestCase(TestCase):

    def setUp(self):
        self.User = get_user_model()

    def tearDown(self):
        if self.User is not None:
            self.User = None

    def test_user_can_save(self):

        user = self.User.objects.create(email='email@gmail.com', first_name='name1', password='pass1')

        saved_users = self.User.objects.all()

        self.assertEqual(saved_users.count(), 1, 'User save error.')
        first_user = saved_users[0]
        self.assertEqual(user.email, first_user.email)
        self.assertEqual(user.first_name, first_user.first_name)

    def test_invalid_user_raise_validation_error(self):
        with self.assertRaises(ValidationError):
            user = self.User.objects.create(first_name='name1', password='pass1')
            user.full_clean()

    def test_invalid_user_email_raise_validation_error(self):
        with self.assertRaises(ValidationError):
            user = self.User.objects.create(email='adan@gmail', first_name='name1', password='pass1')
            user.full_clean()

    def test_get_short_name(self):
        user = self.User(email='email@gmail.com', first_name='name1', password='pass1')
        self.assertEqual(user.get_short_name(), user.first_name)

    def test_get_full_name(self):
        user = self.User(email='email@gmail.com', first_name='name1', password='pass1', last_name='Brian',
                         other_name='Chesky')
        self.assertEqual(user.get_full_name(), '%s %s, %s' % (user.first_name, user.other_name, user.last_name))

    def test_user_profile_to_string(self):
        user = self.User(email='email@gmail.com', first_name='name1', password='pass1', last_name='Brian',
                         other_name='Chesky')
        self.assertEqual(str(user), user.get_full_name())

    def test_username_field(self):
        user = self.User.objects.create(first_name='name1', password='pass1')
        self.assertEqual(user.USERNAME_FIELD, 'email')

    def test_is_staff_property(self):
        user = self.User.objects.create(first_name='name1', password='pass1')
        self.assertTrue(user.is_admin == user.is_staff)

    def test_required_field(self):
        user = self.User.objects.create(first_name='name1', password='pass1')
        self.assertEqual(user.REQUIRED_FIELDS, ['first_name'])
