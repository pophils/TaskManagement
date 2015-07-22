

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.contrib.auth import get_user_model
from account.controller.authentication_view import selenium_login_helper


class SeleniumViewTest(TestCase):

    def test_view_url_resolved_correctly(self):
        resolved_function = resolve('/account/selenium-login/')
        self.assertEqual(resolved_function.func, selenium_login_helper)

    def test_view_can_login(self):
        user = get_user_model().objects.create_user(email='selenium_user@gmail.com', first_name='user1', password='pass1')

        response = self.client.get('/account/selenium-login/', data={'email': user.email, 'password': 'pass1'})

        self.assertContains(response, 'ok')
