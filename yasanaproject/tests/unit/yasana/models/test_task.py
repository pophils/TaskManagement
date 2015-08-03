

from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from yasana.models.user_task import Task


class TaskTestCase(TestCase):

    def test_task_can_save(self):

        user = get_user_model()
        user = user.objects.create(email='email@gmail.com', first_name='name1', password='pass1')

        task = Task.objects.create(title='Development of feedback.', status=0, priority=1,
                                   created_by=user, is_completed=False)

        saved_tasks = Task.objects.all()

        self.assertEqual(saved_tasks.count(), 1, 'Task save error.')
        self.assertEqual(task.created_by, saved_tasks[0].created_by)

    def test_invalid_task_raise_integrity_error(self):
        with self.assertRaises(IntegrityError):
            Task.objects.create(title='Development of feedback.', status=0, priority=1)
