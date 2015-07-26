# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=255, db_column='EmailAddress', unique=True, db_index=True, verbose_name='Email Address')),
                ('first_name', models.CharField(max_length=255)),
                ('other_name', models.CharField(null=True, max_length=255, blank=True)),
                ('last_name', models.CharField(null=True, max_length=255, blank=True)),
                ('username', models.CharField(null=True, max_length=255, db_index=True, unique=True, blank=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('website', models.URLField(null=True, max_length=255, blank=True)),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female'), ('p', 'Prefer not to say')], max_length=1, default='p')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_name='user_set', related_query_name='user', verbose_name='groups', blank=True)),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', verbose_name='user permissions', blank=True)),
            ],
            options={
                'db_table': 'UserProfile',
                'permissions': (('can_manage_users', 'Can manage users'),),
            },
            bases=(models.Model,),
        ),
    ]
