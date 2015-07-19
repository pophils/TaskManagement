

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.contrib.auth import get_user_model
from yasana.controller.landing import LandingView


class LandingViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.User = get_user_model()

    @classmethod
    def tearDownClass(cls):
        if cls.User is not None:
            cls.User = None

    def test_landing_url_resolve_properly(self):
        resolved_url = resolve('/')

        self.assertEqual(resolved_url.func.__name__, LandingView.as_view().__name__, msg='Landing url resolve fails')

    def test_landing_get_returns_right_template_for_logged_in_user(self):

        self.User.objects.create_user(email='user1@gmail.com', first_name='Tola', password='pass1')
        self.client.login(username='user1@gmail.com', password='pass1')
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'yasana/landing.html')

    def test_landing_get_contains_yasana_in_title_for_logged_in_user(self):

        self.User.objects.create_user(email='user1@gmail.com', first_name='Tola', password='pass1')
        self.client.login(username='user1@gmail.com', password='pass1')
        response = self.client.get('/')
        self.assertContains(response, 'yasana')

    def test_landing_redirect_to_login_page_if_user_is_not_yet_logged_in(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/account/login/')
