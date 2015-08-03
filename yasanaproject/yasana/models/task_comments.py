
from django.conf import settings
from django.db import models
from .abstract_base_entity import AbstractBaseEntity
from .user_task import Task


class TaskComment(AbstractBaseEntity, models.Model):
    task = models.ForeignKey(Task, related_name='comments', db_index=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments')
    details = models.CharField(max_length=200)

    def __str__(self):
        return self.details.capitalize()

    class Meta:
        db_table = 'task_comment'
