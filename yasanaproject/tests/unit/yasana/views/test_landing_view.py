

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.contrib.auth import get_user_model
from yasana.controller.landing import LandingView, landing_task_summary
from yasana.models import Task


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

    def test_landing_summary_url_resolves(self):
        resolved_func = resolve('/landing-task-summary/')
        self.assertEqual(resolved_func.func, landing_task_summary)

    def test_task_summary_returned_right_values_for_admin(self):

        self.client.post('/account/login/', data={'email': 'admin@admin.com', 'password': 'admin'})
        self.User.objects.create_user(email='user1@gmail.com', first_name='User1', password='pass1')
        self.User.objects.create_user(email='user2@gmail.com', first_name='User2', password='pass2')
        self.User.objects.create_user(email='user3@gmail.com', first_name='User3', password='pass3')

        user = get_user_model()
        user = user.objects.get(email='admin@admin.com')

        Task.objects.create(title='Development of feedback.', status=0, priority=1, created_by=user, is_completed=False)

        Task.objects.create(title='Development of feedback.', status=1, priority=1, created_by=user, is_completed=False)

        Task.objects.create(title='Development of feedback.', status=1, priority=1, created_by=user, is_completed=False)

        Task.objects.create(title='Development of feedback.', status=2, priority=1, created_by=user, is_completed=True)

        response = self.client.get('/landing-task-summary/?is_admin=1')

        self.assertIn('"users":3', response.content.decode())
        self.assertIn('"new":1', response.content.decode())
        self.assertIn('"pending":2', response.content.decode())
        self.assertIn('"completed":1', response.content.decode())

    def test_task_summary_returned_right_values_for_non_admin(self):

        self.client.post('/account/login/', data={'email': 'admin@admin.com', 'password': 'admin'})
        self.client.logout()
        user = self.User.objects.create_user(email='user1@gmail.com', first_name='User1', password='pass1')
        self.client.login(username='user1@gmail.com', password='pass1')

        Task.objects.create(title='Development of feedback.', status=0, priority=1, created_by=user, is_completed=False)

        Task.objects.create(title='Development of feedback.', status=1, priority=1, created_by=user, is_completed=False)

        Task.objects.create(title='Development of feedback.', status=1, priority=1, created_by=user, is_completed=False)

        Task.objects.create(title='Development of feedback.', status=2, priority=1, created_by=user, is_completed=True)

        response = self.client.get('/landing-task-summary/?is_admin=0')

        self.assertIn('"new":1', response.content.decode())
        self.assertIn('"pending":2', response.content.decode())
        self.assertIn('"completed":1', response.content.decode())
        self.assertNotIn('"users":3', response.content.decode())

    def test_landing_summary_shows_user_summary_div_on_admin_login(self):
        self.client.post('/account/login/', data={'email': 'admin@admin.com', 'password': 'admin'})

        response = self.client.get('/')
        self.assertContains(response, 'class="summary-count users"')

    def test_landing_summary_does_not_show_user_summary_div_on_non_admin_login(self):
        self.client.post('/account/login/', data={'email': 'admin@admin.com', 'password': 'admin'})
        self.client.logout()

        self.User.objects.create_user(email='user1@gmail.com', first_name='User1', password='pass1')
        self.client.login(username='user1@gmail.com', password='pass1')

        response = self.client.get('/')

        self.assertNotContains(response, 'class="summary-count users"')
