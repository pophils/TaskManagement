

from django.test import TestCase
from django.core.exceptions import ValidationError
from account.core.validators import validate_user_phone_no


class EntityValidationsTestCase(TestCase):

    def test_validate_user_phone_returns_validation_error_on_invalid_value(self):

        with self.assertRaises(ValidationError):
            validate_user_phone_no([])

    def test_validate_user_gender_returns_no_error_on_valid_value(self):
        self.assertTrue(validate_user_phone_no('2348094637282') == '2348094637282')
        self.assertTrue(validate_user_phone_no('+2348094637282') == '+2348094637282')
