
from django.conf import settings
from django.db import models
from .abstract_base_entity import AbstractBaseEntity


class Task(AbstractBaseEntity, models.Model):

    priorities = (
        (0, 'Low'),
        (1, 'Medium'),
        (2, 'High'),
        (3, 'Critical'),
    )

    status = (
        (0, 'In progress'),
        (1, 'Completed'),
    )

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks')
    priority = models.IntegerField(choices=priorities, default=0)
    status = models.IntegerField(choices=status, db_index=True, default=0)
    title = models.CharField(max_length=50, db_index=True)
    details = models.CharField(max_length=300)
    is_completed = models.BooleanField(default=False)
    start_date = models.DateField(blank=True, null=True)
    expected_end_date = models.DateField(blank=True, null=True)
    actual_end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return ' {} created on {} with current status: {}'.\
            format(self.title, self.created_date, self.status)

    class Meta:
        db_table = 'task'
