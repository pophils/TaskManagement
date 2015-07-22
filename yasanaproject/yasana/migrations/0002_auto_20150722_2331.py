# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yasana', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('can_manage_users', 'Can manage users'),)},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(unique=True, max_length=255, db_index=True, verbose_name='Email Address', db_column='EmailAddress'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(default='p', max_length=1, choices=[('m', 'Male'), ('f', 'Female'), ('p', 'Prefer not to say')]),
        ),
    ]
