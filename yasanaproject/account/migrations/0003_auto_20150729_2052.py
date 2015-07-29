# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20150727_0225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='is_admin',
            field=models.BooleanField(default=True),
        ),
    ]
