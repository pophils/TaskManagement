
from django.conf import settings
from django.db import models
from .abstract_base_entity import AbstractBaseEntity
from .organisation import Organisation


class Task(AbstractBaseEntity, models.Model):

    priorities = (
        (0, 'Low'),
        (1, 'Medium'),
        (2, 'High'),
        (3, 'Critical'),
    )

    status = (
        (0, 'Not started'),
        (1, 'In progress'),
        (2, 'Completed'),
        (3, 'Stopped'),
        (4, 'Failed'),
    )

    organisation = models.ForeignKey(Organisation, related_name='tasks', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks')
    users_assigned = models.ManyToManyField(settings.AUTH_USER_MODEL)
    priority = models.IntegerField(choices=priorities)
    status = models.IntegerField(choices=status, db_index=True)

    title = models.CharField(max_length=30, db_index=True)
    details = models.CharField(max_length=200, blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    start_date = models.DateField(blank=True, null=True)
    expected_end_date = models.DateField(blank=True, null=True)
    actual_end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return ' {} created on {} and assigned to {} users with current status: {}'.\
            format(self.title, self.created_date, self.users_assigned.count(), self.status)

    class Meta:
        db_table = 'task'
