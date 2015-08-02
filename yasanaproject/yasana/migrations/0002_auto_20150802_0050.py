# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yasana', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='users_assigned',
        ),
        migrations.AlterField(
            model_name='task',
            name='details',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.IntegerField(choices=[(0, 'Low'), (1, 'Medium'), (2, 'High'), (3, 'Critical')], default=0),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.IntegerField(db_index=True, choices=[(0, 'In progress'), (1, 'Completed')], default=0),
        ),
    ]
