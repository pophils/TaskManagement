# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('email', models.CharField(max_length=255, verbose_name='Email Address', db_column='EmailAddress', unique=True, db_index=True)),
                ('first_name', models.CharField(max_length=255)),
                ('other_name', models.CharField(max_length=255, blank=True, null=True)),
                ('last_name', models.CharField(max_length=255, blank=True, null=True)),
                ('username', models.CharField(max_length=255, blank=True, unique=True, null=True, db_index=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('website', models.URLField(max_length=255, blank=True, null=True)),
                ('gender', models.CharField(default='m', choices=[('m', 'Male'), ('f', 'Female'), ('p', 'Prefer not to say')], max_length=1)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', blank=True, related_name='user_set', to='auth.Group', verbose_name='groups', related_query_name='user')),
            ],
            options={
                'db_table': 'UserProfile',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('org_id', models.AutoField(auto_created=True, serialize=False, db_index=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=12, blank=True, null=True)),
                ('email', models.EmailField(max_length=200, blank=True, null=True)),
            ],
            options={
                'db_table': 'organisation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('priority', models.IntegerField(choices=[(0, 'Low'), (1, 'Medium'), (2, 'High'), (3, 'Critical')])),
                ('status', models.IntegerField(choices=[(0, 'Not started'), (1, 'In progress'), (2, 'Completed'), (3, 'Stopped'), (4, 'Failed')], db_index=True)),
                ('title', models.CharField(max_length=30, db_index=True)),
                ('details', models.CharField(max_length=200, blank=True, null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('expected_end_date', models.DateField(blank=True, null=True)),
                ('actual_end_date', models.DateField(blank=True, null=True)),
                ('created_by', models.ForeignKey(related_name='tasks', to=settings.AUTH_USER_MODEL)),
                ('organisation', models.ForeignKey(blank=True, related_name='tasks', to='yasana.Organisation', null=True)),
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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('details', models.CharField(max_length=200)),
                ('created_by', models.ForeignKey(related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(related_name='comments', to='yasana.Task')),
            ],
            options={
                'db_table': 'task_comment',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='organisation',
            field=models.ForeignKey(to='yasana.Organisation', blank=True, related_name='users', default=None, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(help_text='Specific permissions for this user.', blank=True, related_name='user_set', to='auth.Permission', verbose_name='user permissions', related_query_name='user'),
            preserve_default=True,
        ),
    ]
