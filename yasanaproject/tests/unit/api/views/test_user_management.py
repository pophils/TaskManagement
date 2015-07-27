

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.contrib.auth import get_user_model
from api.controller.account import api_get_users


class UserManagementApiTestCase(TestCase):

    def test_api_users_resolve_correctly(self):
        resolved_func = resolve('/api/users/')

        self.assertEqual(resolved_func.func, api_get_users)

    def test_api_users_returns_right_response(self):

        get_user_model().objects.create_user(email='user1@gmail.com',
                                             first_name='user1', password='pass1')

        get_user_model().objects.create_user(email='user2@gmail.com',
                                             first_name='user2', password='pass1')

        response = self.client.get('/api/users/')

        self.assertContains(response, 'user1@gmail.com')
        self.assertContains(response, 'user2@gmail.com')
        self.assertContains(response, 'user1')
        self.assertContains(response, 'user2')
