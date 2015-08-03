

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

    def test_landing_summary_shows_user_summary_div_on_admin_login(self):
        self.client.post('/account/login/', data={'email': 'admin@admin.com', 'password': 'admin'})

        response = self.client.get('/')
        self.assertContains(response, 'class="summary-count users"')

    def test_landing_summary_shows_manage_user_link_on_admin_login(self):
        self.client.post('/account/login/', data={'email': 'admin@admin.com', 'password': 'admin'})

        response = self.client.get('/')
        self.assertContains(response, 'id="manage-user-link"')

    def test_landing_summary_does_not_show_user_summary_div_on_non_admin_login(self):
        self.client.post('/account/login/', data={'email': 'admin@admin.com', 'password': 'admin'})
        self.client.logout()

        self.User.objects.create_user(email='user1@gmail.com', first_name='User1', password='pass1')
        self.client.login(username='user1@gmail.com', password='pass1')

        response = self.client.get('/')

        self.assertNotContains(response, 'class="summary-count users"')

    def test_landing_summary_does_not_show_manage_user_link_on_non_admin_login(self):
        self.client.post('/account/login/', data={'email': 'admin@admin.com', 'password': 'admin'})
        self.client.logout()

        self.User.objects.create_user(email='user1@gmail.com', first_name='User1', password='pass1')
        self.client.login(username='user1@gmail.com', password='pass1')

        response = self.client.get('/')

        self.assertNotContains(response, 'id="manage-user-link"')
