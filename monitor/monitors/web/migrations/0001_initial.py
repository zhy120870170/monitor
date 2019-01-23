# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MonitorTask',
            fields=[
                ('mt_name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('mt_keys', models.CharField(max_length=50, null=True, blank=True)),
                ('mt_sources', models.CharField(max_length=200, null=True, blank=True)),
                ('mt_source_counts', models.IntegerField(default=0)),
                ('mt_remark', models.CharField(max_length=200, null=True, blank=True)),
                ('mt_status', models.IntegerField(default=0)),
                ('mt_create_date', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('mt_last_date', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
            ],
        ),
    ]
