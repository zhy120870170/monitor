# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeiBoContent',
            fields=[
                ('content_id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('spider_id', models.CharField(max_length=50, null=True, blank=True)),
                ('content_text', models.CharField(max_length=5000, null=True, blank=True)),
                ('reposts_count', models.CharField(max_length=20, null=True, blank=True)),
                ('comments_count', models.CharField(max_length=20, null=True, blank=True)),
                ('attitudes_count', models.CharField(max_length=20, null=True, blank=True)),
                ('create_user', models.CharField(max_length=50, null=True, blank=True)),
                ('weibo_url', models.CharField(max_length=200, null=True, blank=True)),
                ('created_at', models.DateTimeField(null=True, blank=True)),
                ('update_at', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='WeiBoPinglun',
            fields=[
                ('pinglun_id', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('pinglun_parent_id', models.CharField(max_length=100, null=True, blank=True)),
                ('pinglun_text', models.CharField(max_length=5000, null=True, blank=True)),
                ('created_at', models.DateTimeField(null=True, blank=True)),
                ('sub_pinglun_count', models.CharField(max_length=20, null=True, blank=True)),
                ('like_count', models.CharField(max_length=20, null=True, blank=True)),
                ('floor_number', models.CharField(max_length=20, null=True, blank=True)),
                ('pinglun_user', models.CharField(max_length=100, null=True, blank=True)),
                ('weibo_content_id', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='WeiboSpider',
            fields=[
                ('name', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=2, null=True, blank=True)),
                ('start_url', models.CharField(max_length=255, null=True, blank=True)),
                ('weibo_uid', models.CharField(max_length=255, null=True, blank=True)),
                ('fensi_count', models.CharField(max_length=20, null=True, blank=True)),
                ('weibo_count', models.CharField(max_length=20, null=True, blank=True)),
            ],
        ),
    ]
