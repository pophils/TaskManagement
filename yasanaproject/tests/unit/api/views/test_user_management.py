

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.contrib.auth import get_user_model
from api.controller.account import api_get_users, get_users_total_count


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

    def test_api_users_returns_right_bad_request_response_status_on_invalid_pg_no(self):

        response = self.client.get('/api/users/?pg_no=invalid_pg_no')
        self.assertEqual(response.status_code, 400)

    def test_api_users_returns_users_from_zero_index_on_negative_pg_no(self):

        get_user_model().objects.create_user(email='user1@gmail.com',
                                             first_name='user1', password='pass1')

        get_user_model().objects.create_user(email='user2@gmail.com',
                                             first_name='user2', password='pass1')

        response = self.client.get('/api/users/?pg_no=-12')

        self.assertContains(response, 'user1@gmail.com')
        self.assertContains(response, 'user2@gmail.com')
        self.assertContains(response, 'user1')
        self.assertContains(response, 'user2')

    def test_api_users_returns_can_save_on_valid_data_post(self):
        response = self.client.post('/api/users/', data={'first_name': 'name1', 'last_name': 'name2',
                                                         'other_name': 'name3', 'phone': '090896272',
                                                         'gender': 'm', 'department': 'Deep Learning',
                                                         'email': 'name@name.com', 'password': 'pass1',
                                                         'confirm_password': 'pass1'
                                                         })

        self.assertContains(response, '"save_status":true')
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_api_users_returns_cannot_save_on_invalid_data_post(self):
        response = self.client.post('/api/users/', data={'first_name': '', 'last_name': 'name2',
                                                         'other_name': 'name3', 'phone': '090896272',
                                                         'gender': 'm', 'department': 'Deep Learning',
                                                         'email': 'name@name.com', 'password': 'pass1',
                                                         'confirm_password': 'pass1'
                                                         })

        self.assertNotContains(response, '"save_status":true')
        self.assertEqual(get_user_model().objects.count(), 0)

        response = self.client.post('/api/users/', data={'first_name': 'name1', 'last_name': 'name2',
                                                         'other_name': 'name3', 'phone': 'westdh090896272',
                                                         'gender': 'm', 'department': 'Deep Learning',
                                                         'email': 'name@name.com', 'password': 'pass1',
                                                         'confirm_password': 'pass1'
                                                         })

        self.assertNotContains(response, '"save_status":true')
        self.assertEqual(get_user_model().objects.count(), 0)

        response = self.client.post('/api/users/', data={'first_name': 'name1', 'last_name': 'name2',
                                                         'other_name': 'name3', 'phone': '090896272',
                                                         'gender': '-1', 'department': 'Deep Learning',
                                                         'email': 'name@name.com', 'password': 'pass1',
                                                         'confirm_password': 'pass1'
                                                         })

        self.assertNotContains(response, '"save_status":true')
        self.assertEqual(get_user_model().objects.count(), 0)

        response = self.client.post('/api/users/', data={'first_name': 'name1', 'last_name': 'name2',
                                                         'other_name': 'name3', 'phone': '090896272',
                                                         'gender': 'm', 'department': 'Deep Learning',
                                                         'email': '', 'password': 'pass1',
                                                         'confirm_password': 'pass1'
                                                         })

        self.assertNotContains(response, '"save_status":true')
        self.assertEqual(get_user_model().objects.count(), 0)

        response = self.client.post('/api/users/', data={'first_name': 'name1', 'last_name': 'name2',
                                                         'other_name': 'name3', 'phone': '090896272',
                                                         'gender': 'm', 'department': 'Deep Learning',
                                                         'email': 'invalid_email', 'password': 'pass1',
                                                         'confirm_password': 'pass1'
                                                         })

        self.assertNotContains(response, '"save_status":true')
        self.assertEqual(get_user_model().objects.count(), 0)

        response = self.client.post('/api/users/', data={'first_name': 'name1', 'last_name': 'name2',
                                                         'other_name': 'name3', 'phone': '090896272',
                                                         'gender': 'm', 'department': 'Deep Learning',
                                                         'email': 'name@name.com', 'password': '',
                                                         'confirm_password': 'pass1'
                                                         })

        self.assertNotContains(response, '"save_status":true')
        self.assertEqual(get_user_model().objects.count(), 0)

        response = self.client.post('/api/users/', data={'first_name': 'name1', 'last_name': 'name2',
                                                         'other_name': 'name3', 'phone': '090896272',
                                                         'gender': 'm', 'department': 'Deep Learning',
                                                         'email': 'name@name.com', 'password': 'pass1',
                                                         'confirm_password': ''
                                                         })

        self.assertNotContains(response, '"save_status":true')
        self.assertEqual(get_user_model().objects.count(), 0)

        response = self.client.post('/api/users/', data={'first_name': 'name1', 'last_name': 'name2',
                                                         'other_name': 'name3', 'phone': '090896272',
                                                         'gender': 'm', 'department': 'Deep Learning',
                                                         'email': 'name@name.com', 'password': 'pass1',
                                                         'confirm_password': 'confirm_pass'
                                                         })

        self.assertNotContains(response, '"save_status":true')
        self.assertEqual(get_user_model().objects.count(), 0)

        get_user_model().objects.create_user(email='k@gmail.com', first_name='name1', password='pass1')

        response = self.client.post('/api/users/', data={'first_name': 'name1', 'last_name': 'name2',
                                                         'other_name': 'name3', 'phone': '090896272',
                                                         'gender': 'm', 'department': 'Deep Learning',
                                                         'email': 'k@gmail.com', 'password': 'pass1',
                                                         'confirm_password': 'pass1'
                                                         })

        self.assertNotContains(response, '"save_status":true')
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_get_total_users_url_resolve_correctly(self):
        resolved_func = resolve('/api/total-users/')

        self.assertEqual(resolved_func.func, get_users_total_count)

    def test_get_total_users_url_return_the_right_num(self):

        self.client.post('/account/login/', data={'email': 'admin@admin.com', 'password': 'admin'})
        get_user_model().objects.create_user(email='k@gmail.com', first_name='name1', password='pass1')
        get_user_model().objects.create_user(email='l@gmail.com', first_name='name2', password='pass2')
        get_user_model().objects.create_user(email='m@gmail.com', first_name='name3', password='pass3')

        response = self.client.get('/api/total-users/')

        self.assertContains(response, 3)
        self.assertNotContains(response, 4)
