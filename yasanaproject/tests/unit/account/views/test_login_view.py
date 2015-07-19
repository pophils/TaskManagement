

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.contrib.auth import get_user_model, SESSION_KEY
from mock import patch
from account.controller.authentication_view import signin, signout
from account.core.forms.login_form import LoginForm


class AuthenticationViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.User = get_user_model()

    @classmethod
    def tearDownClass(cls):
        if cls.User is not None:
            cls.User = None

    def test_view_url_resolve_successfully(self):
        resolved_url = resolve('/account/login/')

        self.assertEqual(resolved_url.func, signin)

    def test_view_uses_the_right_template(self):

        response = self.client.get('/account/login/')

        self.assertTemplateUsed(response, 'account/login.html')

    def test_view_context_uses_the_login_form_class(self):
        response = self.client.get('/account/login/')

        self.assertIsNotNone(response.context['login_form'])

    def test_view_context_uses_the_right_form_class(self):
        response = self.client.get('/account/login/')

        self.assertIsInstance(response.context['login_form'], LoginForm)

    @patch('account.controller.authentication_view.authenticate')
    def test_view_authenticate_is_rightly_patched(self, mock_authenticate):

        mock_authenticate.return_value = None
        self.client.post('/account/login/', data={'email': 'user1@gmail.com', 'password': 'pass1'})

        mock_authenticate.assert_called_once_with(username='user1@gmail.com', password='pass1')

    @patch('account.controller.authentication_view.authenticate')
    def test_view_can_login_valid_user_and_redirect_to_landing(self, mock_authenticate):

        user = self.User.objects.create_user(email='k@gmail.com', first_name='Tola', password='pass1')

        user.backend = ''
        mock_authenticate.return_value = user
        self.client.login(username='k@gmail.com', password='pass1')
        response = self.client.post('/account/login/', data={'email': 'k@gmail.com', 'password': 'pass1'})
        self.assertRedirects(response, '/')

    @patch('account.controller.authentication_view.authenticate')
    def test_view_cannot_login_invalid_user(self, mock_authenticate):
        mock_authenticate.return_value = None
        response = self.client.post('/account/login/', data={'email': 'user1@gmail.com', 'password': 'pass1'})

        self.assertContains(response, 'Invalid username or password.')

    @patch('account.controller.authentication_view.authenticate')
    def test_view_got_error_context_on_invalid_user_login(self, mock_authenticate):
        mock_authenticate.return_value = None
        response = self.client.post('/account/login/', data={'email': 'user1@gmail.com', 'password': 'pass1'})

        self.assertIsNotNone(response.context['error_message'])

    def test_view_redirect_to_landing_if_user_is_already_login(self):
        self.User.objects.create_user(email='user1@gmail.com', first_name='Tola', password='pass1')
        self.client.login(username='user1@gmail.com', password='pass1')

        response = self.client.get('/account/login/')

        self.assertRedirects(response, '/')

    @patch('account.controller.authentication_view.authenticate')
    def test_view_create_right_auth_session_on_login(self, mock_authenticate):
        user = self.User.objects.create_user(email='user1@gmail.com', first_name='Tola', password='pass1')
        user.backend = ''

        mock_authenticate.return_value = user

        self.client.post('/account/login/', data={'email': 'user1@gmail.com', 'password': 'pass1'})

        self.assertIn(SESSION_KEY, self.client.session, 'User logged in but session not set')

    @patch('account.controller.authentication_view.authenticate')
    def test_view_does_not_create_auth_session_on_invalid_login(self, mock_authenticate):
        mock_authenticate.return_value = None

        self.client.post('/account/login/', data={'email': 'user1@gmail.com', 'password': 'pass1'})

        self.assertNotIn(SESSION_KEY, self.client.session, 'Invalid User logged in.')

    def test_logout_view_url_resolved_properly(self):
        resolved_url = resolve('/account/logout/')
        self.assertEqual(resolved_url.func, signout)

    def test_view_logout_redirect_to_login_page(self):

        response = self.client.get('/account/logout/')
        self.assertRedirects(response, '/account/login/')

    def test_logout_view_removed_user_session(self):
        self.client.get('/account/logout/')
        self.assertNotIn(SESSION_KEY, self.client.session, 'User session still valid after logout.')
