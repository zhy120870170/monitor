# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20190109_1117'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('u_id', models.IntegerField(serialize=False, primary_key=True)),
                ('u_name', models.CharField(max_length=50, null=True, blank=True)),
                ('u_pwd', models.CharField(max_length=50, null=True, blank=True)),
                ('u_last_login_date', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
            ],
        ),
    ]
