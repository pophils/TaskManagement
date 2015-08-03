

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.contrib.auth import get_user_model
from api.controller.task import task_summary
from yasana.models.user_task import Task


class TaskManagementTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.User = get_user_model()

    @classmethod
    def tearDownClass(cls):
        if cls.User is not None:
            cls.User = None

    def test_landing_summary_url_resolves(self):
        resolved_func = resolve('/api/task-summary/')
        self.assertEqual(resolved_func.func, task_summary)

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

        response = self.client.get('/api/task-summary/?is_admin=1')

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

        response = self.client.get('/api/task-summary/?is_admin=0')

        self.assertIn('"new":1', response.content.decode())
        self.assertIn('"pending":2', response.content.decode())
        self.assertIn('"completed":1', response.content.decode())
        self.assertNotIn('"users":3', response.content.decode())
