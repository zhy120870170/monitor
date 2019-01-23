# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_xiechengaskanswer_xiechengaskcon_xiechengpinglun_xiechengspider_xiechengsubpinglun_xiechengtravelnot'),
    ]

    operations = [
        migrations.CreateModel(
            name='MafwAsk',
            fields=[
                ('ask_id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('ask_task_name', models.CharField(max_length=255, null=True, blank=True)),
                ('ask_title', models.CharField(max_length=1000, null=True, blank=True)),
                ('ask_content', models.TextField(null=True, blank=True)),
                ('ask_user', models.CharField(max_length=255, null=True, blank=True)),
                ('ask_date', models.DateTimeField(null=True, blank=True)),
                ('ask_scrapy_date', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('ask_used_counts', models.IntegerField(null=True, blank=True)),
                ('ask_answer_counts', models.IntegerField(null=True, blank=True)),
                ('ask_same_counts', models.IntegerField(null=True, blank=True)),
                ('ask_url', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MafwAskAnswer',
            fields=[
                ('answer_id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('answer_ask_id', models.CharField(max_length=255, null=True, blank=True)),
                ('answer_parent_id', models.CharField(max_length=255, null=True, blank=True)),
                ('answer_content', models.CharField(max_length=8000, null=True, blank=True)),
                ('answer_user', models.CharField(max_length=255, null=True, blank=True)),
                ('answer_date', models.DateTimeField(null=True, blank=True)),
                ('answer_scrapy_date', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('answer_sub_counts', models.IntegerField(null=True, blank=True)),
                ('answer_like_counts', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MafwSpider',
            fields=[
                ('name', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=2, null=True, blank=True)),
                ('search_count', models.IntegerField(null=True, blank=True)),
                ('start_url', models.CharField(max_length=255, null=True, blank=True)),
                ('is_all', models.CharField(max_length=1, null=True, blank=True)),
                ('last_scrapy_time', models.CharField(max_length=25, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MafwTravelBook',
            fields=[
                ('book_id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('book_task_name', models.CharField(max_length=255, null=True, blank=True)),
                ('book_title', models.CharField(max_length=1000, null=True, blank=True)),
                ('book_content', models.TextField(null=True, blank=True)),
                ('book_user', models.CharField(max_length=255, null=True, blank=True)),
                ('book_date', models.DateTimeField(null=True, blank=True)),
                ('book_scrapy_date', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('book_scan_counts', models.IntegerField(null=True, blank=True)),
                ('booker_answer_counts', models.IntegerField(null=True, blank=True)),
                ('book_url', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='QyerAsk',
            fields=[
                ('ask_id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('ask_task_name', models.CharField(max_length=255, null=True, blank=True)),
                ('ask_title', models.CharField(max_length=1000, null=True, blank=True)),
                ('ask_content', models.TextField(null=True, blank=True)),
                ('ask_user', models.CharField(max_length=255, null=True, blank=True)),
                ('ask_date', models.DateTimeField(null=True, blank=True)),
                ('ask_scrapy_date', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('ask_answer_counts', models.IntegerField(null=True, blank=True)),
                ('ask_url', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='QyerAskAnswer',
            fields=[
                ('answer_id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('answer_ask_id', models.CharField(max_length=255, null=True, blank=True)),
                ('answer_parent_id', models.CharField(max_length=255, null=True, blank=True)),
                ('answer_content', models.CharField(max_length=1000, null=True, blank=True)),
                ('answer_user', models.CharField(max_length=255, null=True, blank=True)),
                ('answer_date', models.DateTimeField(null=True, blank=True)),
                ('answer_scrapy_date', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('answer_sub_counts', models.IntegerField(null=True, blank=True)),
                ('answer_like_counts', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='QyerBbs',
            fields=[
                ('bbs_id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('bbs_task_name', models.CharField(max_length=255, null=True, blank=True)),
                ('bbs_title', models.CharField(max_length=1000, null=True, blank=True)),
                ('bbs_content', models.TextField(null=True, blank=True)),
                ('bbs_user', models.CharField(max_length=255, null=True, blank=True)),
                ('bbs_date', models.DateTimeField(null=True, blank=True)),
                ('bbs_scrapy_date', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('bbs_scan_counts', models.IntegerField(null=True, blank=True)),
                ('bbs_answer_counts', models.IntegerField(null=True, blank=True)),
                ('bbs_like_counts', models.IntegerField(null=True, blank=True)),
                ('bbs_url', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='QyerSpider',
            fields=[
                ('name', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=2, null=True, blank=True)),
                ('search_count', models.IntegerField(null=True, blank=True)),
                ('start_url', models.CharField(max_length=255, null=True, blank=True)),
                ('is_all', models.CharField(max_length=1, null=True, blank=True)),
                ('last_scrapy_time', models.CharField(max_length=25, null=True, blank=True)),
            ],
        ),
    ]
