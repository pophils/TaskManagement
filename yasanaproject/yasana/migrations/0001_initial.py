# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('priority', models.IntegerField(choices=[(0, 'Low'), (1, 'Medium'), (2, 'High'), (3, 'Critical')])),
                ('status', models.IntegerField(choices=[(0, 'Not started'), (1, 'In progress'), (2, 'Completed'), (3, 'Stopped'), (4, 'Failed')], db_index=True)),
                ('title', models.CharField(max_length=30, db_index=True)),
                ('details', models.CharField(null=True, max_length=200, blank=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('expected_end_date', models.DateField(null=True, blank=True)),
                ('actual_end_date', models.DateField(null=True, blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='tasks')),
                ('users_assigned', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'task',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskComment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('details', models.CharField(max_length=200)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='comments')),
                ('task', models.ForeignKey(to='yasana.Task', related_name='comments')),
            ],
            options={
                'db_table': 'task_comment',
            },
            bases=(models.Model,),
        ),
    ]
