

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from api.controller.task import task_summary, api_get_tasks, get_task_total_count
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

    def test_api_tasks_resolve_correctly(self):
        resolved_func = resolve('/api/tasks/')

        self.assertEqual(resolved_func.func, api_get_tasks)

    def test_get_total_tasks_url_resolve_correctly(self):
        resolved_func = resolve('/api/total-tasks/')

        self.assertEqual(resolved_func.func, get_task_total_count)

    def test_get_total_pending_tasks_url_return_bad_request_if_status_query_param_not_passed(self):

        self.client.post('/account/login/', data={'email': 'admin@admin.com', 'password': 'admin'})
        user = get_user_model().objects.get(email='admin@admin.com')
        Task.objects.create(title='task a', details='details a', priority='0', status=0, start_date='2015-10-12',
                            expected_end_date='2016-10-12', created_by=user)
        Task.objects.create(title='task b', details='details b', priority='0', status=0, start_date='2015-10-12',
                            expected_end_date='2016-10-12', created_by=user)
        Task.objects.create(title='task c', details='details c', priority='0', status=0, start_date='2015-10-12',
                            expected_end_date='2016-10-12', created_by=user)

        response = self.client.get('/api/total-tasks/')

        self.assertEqual(response.status_code, 400)

    def test_get_total_pending_tasks_url_return_bad_request_if_invalid_status_query_param_not_passed(self):

        self.client.post('/account/login/', data={'email': 'admin@admin.com', 'password': 'admin'})
        user = get_user_model().objects.get(email='admin@admin.com')
        Task.objects.create(title='task a', details='details a', priority='0', status=0, start_date='2015-10-12',
                            expected_end_date='2016-10-12', created_by=user)
        Task.objects.create(title='task b', details='details b', priority='0', status=0, start_date='2015-10-12',
                            expected_end_date='2016-10-12', created_by=user)
        Task.objects.create(title='task c', details='details c', priority='0', status=0, start_date='2015-10-12',
                            expected_end_date='2016-10-12', created_by=user)

        response = self.client.get('/api/total-tasks/?status=shdu')

        self.assertEqual(response.status_code, 400)

    def test_get_total_pending_tasks_url_return_the_right_num(self):

        self.client.post('/account/login/', data={'email': 'admin@admin.com', 'password': 'admin'})
        user = get_user_model().objects.get(email='admin@admin.com')
        Task.objects.create(title='task a', details='details a', priority='0', status=0, start_date='2015-10-12',
                            expected_end_date='2016-10-12', created_by=user)
        Task.objects.create(title='task b', details='details b', priority='0', status=0, start_date='2015-10-12',
                            expected_end_date='2016-10-12', created_by=user)
        Task.objects.create(title='task c', details='details c', priority='0', status=0, start_date='2015-10-12',
                            expected_end_date='2016-10-12', created_by=user)

        response = self.client.get('/api/total-tasks/?status=0')

        self.assertContains(response, 3)
        self.assertNotContains(response, 4)

    def test_api_tasks_returns_right_response_for_pending_status(self):
        self.client.post('/account/login/', data={'email': 'admin@admin.com', 'password': 'admin'})

        self.client.post('/api/tasks/', data={'title': 'task a', "details": 'details a', "priority": '0',
                                              'status': '0', 'start_date': '2015-10-12',
                                              'expected_end_date': '2016-10-12'})

        self.client.post('/api/tasks/', data={'title': 'task b', "details": 'details b', "priority": '0',
                                              'status': '0', 'start_date': '2015-10-12',
                                              'expected_end_date': '2017-10-12'})

        response = self.client.get('/api/tasks/?status=0')
        self.assertContains(response, 'task a')
        self.assertContains(response, 'task b')
        self.assertContains(response, 'details b')
        self.assertContains(response, '2015-10-12')
        self.assertContains(response, '2017-10-12')

    def test_api_tasks_returns_bad_request_on_invalid_or_no_status_value(self):
        self.client.post('/account/login/', data={'email': 'admin@admin.com', 'password': 'admin'})

        self.client.post('/api/tasks/', data={'title': 'task a', "details": 'details a', "priority": '0',
                                              'status': '0', 'start_date': '2015-10-12',
                                              'expected_end_date': '2016-10-12'})

        self.client.post('/api/tasks/', data={'title': 'task b', "details": 'details b', "priority": '0',
                                              'status': '0', 'start_date': '2015-10-12',
                                              'expected_end_date': '2017-10-12'})

        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, 400)

        response = self.client.get('/api/tasks/?status=invalid_status_value')
        self.assertEqual(response.status_code, 400)

    def test_api_tasks_can_save_on_valid_data_post(self):
        self.client.post('/account/login/', data={'email': 'admin@admin.com', 'password': 'admin'})
        response = self.client.post('/api/tasks/', data={'title': 'task a', "details": 'details a', "priority": '0',
                                                         'status': '0', 'start_date': '2015-10-12',
                                                         'expected_end_date': '2016-10-12'})

        self.assertContains(response, '"save_status":true')
        saved_task = Task.objects.all().select_related('created_by')

        self.assertEqual(saved_task.count(), 1)
        self.assertEqual(saved_task[0].created_by.email, 'admin@admin.com')
        self.assertEqual(saved_task[0].title, 'task a')

    def test_api_tasks_cannot_save_on_invalid_data_post(self):
        response = self.client.post('/api/tasks/', data={'title': '', "details": 'details a', "priority": '0',
                                                         'status': '0', 'start_date': '2015-10-12',
                                                         'expected_end_date': '2016-10-12'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Task.objects.count(), 0)

        response = self.client.post('/api/tasks/', data={'title': 'task a', "details": '', "priority": '0',
                                                         'status': '0', 'start_date': '2015-10-12',
                                                         'expected_end_date': '2016-10-12'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Task.objects.count(), 0)

        response = self.client.post('/api/tasks/', data={'title': 'task a', "details": 'details a', "priority": '',
                                                         'status': '0', 'start_date': '2015-10-12',
                                                         'expected_end_date': '2016-10-12'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Task.objects.count(), 0)

    def test_api_task_can_update_on_valid_data_put_request(self):
        self.client.post('/account/login/', data={'email': 'admin@admin.com', 'password': 'admin'})
        client = APIClient()

        self.client.post('/api/tasks/', data={'title': 'task a', "details": 'details a', "priority": '0',
                                              'status': '0', 'start_date': '2015-10-12',
                                              'expected_end_date': '2016-10-12'})

        saved_task = Task.objects.all()[0]

        response = client.put('/api/tasks/', data={'title': 'task b', "details": 'details a', "priority": '0',
                                                   'status': '0', 'start_date': '2015-10-12',
                                                   'expected_end_date': '2016-10-12', 'id': '{}'.format(saved_task.id)},
                              format='json')

        saved_task = Task.objects.all()[0]

        self.assertEqual(response.data, {'save_status': True})
        self.assertEqual(saved_task.title, 'task b')
        self.assertNotEqual(saved_task.title, 'task a')

    def test_api_task_cannot_update_on_invalid_data_put_request(self):
        self.client.post('/account/login/', data={'email': 'admin@admin.com', 'password': 'admin'})
        client = APIClient()

        self.client.post('/api/tasks/', data={'title': 'task a', "details": 'details a', "priority": '0',
                                              'status': '0', 'start_date': '2015-10-12',
                                              'expected_end_date': '2016-10-12'})

        saved_task = Task.objects.all()[0]

        response = client.put('/api/tasks/', data={'title': '', "details": 'details a', "priority": '0',
                                                   'status': '0', 'start_date': '2015-10-12',
                                                   'expected_end_date': '2016-10-12', 'id': '{}'.format(saved_task.id)},
                              format='json')

        saved_task = Task.objects.all()[0]

        self.assertEqual(response.status_code, 400)
        self.assertEqual(saved_task.title, 'task a')
        self.assertNotEqual(saved_task.title, '')

        response = client.put('/api/tasks/', data={'title': 'a', "details": 'details a', "priority": '0',
                                                   'status': '0', 'start_date': '2015-10-12',
                                                   'expected_end_date': '2016-10-12', 'id': '{}'},
                              format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(saved_task.title, 'task a')

        response = client.put('/api/tasks/', data={'title': 'a', "details": 'details a', "priority": '0',
                                                   'status': '0', 'start_date': '2015-10-12',
                                                   'expected_end_date': '2016-10-12'},
                              format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(saved_task.title, 'task a')

    def test_api_tasks_can_delete_task_on_delete_request(self):

        self.client.post('/account/login/', data={'email': 'admin@admin.com', 'password': 'admin'})
        client = APIClient()

        self.client.post('/api/tasks/', data={'title': 'task a', "details": 'details a', "priority": '0',
                                              'status': '0', 'start_date': '2015-10-12',
                                              'expected_end_date': '2016-10-12'})

        saved_task = Task.objects.all()[0]

        client.delete('/api/tasks/', data={'id': '{}'.format(saved_task.id)}, format='json')

        self.assertEqual(Task.objects.count(), 0)

    def test_api_tasks_cannot_delete_task_and_returns_bad_request_on_delete_request(self):

        self.client.post('/account/login/', data={'email': 'admin@admin.com', 'password': 'admin'})
        client = APIClient()

        self.client.post('/api/tasks/', data={'title': 'task a', "details": 'details a', "priority": '0',
                                              'status': '0', 'start_date': '2015-10-12',
                                              'expected_end_date': '2016-10-12'})

        response = client.delete('/api/tasks/', data={'id': '{}'}, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Task.objects.count(), 1)

        response = client.delete('/api/tasks/', format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Task.objects.count(), 1)
