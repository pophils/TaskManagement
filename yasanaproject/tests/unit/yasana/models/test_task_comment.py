

from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from yasana.models.user_task import Task
from yasana.models.task_comments import TaskComment


class TaskCommentTestCase(TestCase):

    def test_task_comment_can_save(self):

        user = get_user_model()
        user = user.objects.create(email='email@gmail.com', first_name='name1', password='pass1')

        task = Task.objects.create(title='Development of feedback.', status=0, priority=1,
                                   created_by=user, is_completed=False)

        comment = TaskComment.objects.create(task=task, details='Whats up with the task.', created_by=user)

        saved_comments = TaskComment.objects.all()

        self.assertEqual(saved_comments.count(), 1, 'Task comment save error.')
        self.assertEqual(comment.created_by, saved_comments[0].created_by)
        self.assertEqual(comment.task, saved_comments[0].task)

    def test_invalid_task_raise_integrity_error(self):
        with self.assertRaises(IntegrityError):
            TaskComment.objects.create(details='Whats up with the task.')

    def test_task_comment_to_string(self):
        comment = TaskComment(details='Whats up with the task.')
        self.assertEqual(str(comment), comment.details.capitalize())






