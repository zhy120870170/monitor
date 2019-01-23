# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_weibocontent_weibopinglun_weibospider'),
    ]

    operations = [
        migrations.CreateModel(
            name='XieChengAskAnswer',
            fields=[
                ('answer_id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('answer_parent_id', models.CharField(max_length=255, null=True, blank=True)),
                ('answer_ask_id', models.CharField(max_length=255, null=True, blank=True)),
                ('answer_con', models.CharField(max_length=4000, null=True, blank=True)),
                ('answer_user', models.CharField(max_length=255, null=True, blank=True)),
                ('answer_date', models.DateTimeField(null=True, blank=True)),
                ('answer_sub_counts', models.CharField(max_length=10, null=True, blank=True)),
                ('answer_uesd_counts', models.CharField(max_length=10, null=True, blank=True)),
                ('answer_is_best', models.CharField(max_length=1, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='XieChengAskCon',
            fields=[
                ('ask_id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('ask_task_name', models.CharField(max_length=255, null=True, blank=True)),
                ('ask_title', models.CharField(max_length=1000, null=True, blank=True)),
                ('ask_question', models.CharField(max_length=4000, null=True, blank=True)),
                ('ask_user', models.CharField(max_length=255, null=True, blank=True)),
                ('ask_date', models.DateTimeField(null=True, blank=True)),
                ('ask_collects', models.CharField(max_length=10, null=True, blank=True)),
                ('ask_shares', models.CharField(max_length=10, null=True, blank=True)),
                ('ask_answers', models.CharField(max_length=10, null=True, blank=True)),
                ('ask_url', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='XieChengPingLun',
            fields=[
                ('pl_id', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('pl_user', models.CharField(max_length=50, null=True, blank=True)),
                ('pl_travel_type', models.CharField(max_length=20, null=True, blank=True)),
                ('pl_compGradeContent', models.CharField(max_length=10, null=True, blank=True)),
                ('pl_compTextContent', models.CharField(max_length=5000, null=True, blank=True)),
                ('pl_date', models.DateTimeField(null=True, blank=True)),
                ('pl_prodect_name', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='XieChengSpider',
            fields=[
                ('name', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=2, null=True, blank=True)),
                ('search_count', models.CharField(max_length=255, null=True, blank=True)),
                ('start_url', models.CharField(max_length=255, null=True, blank=True)),
                ('satisfaction_score', models.CharField(max_length=255, null=True, blank=True)),
                ('satisfaction_count', models.CharField(max_length=255, null=True, blank=True)),
                ('fell_a_score', models.CharField(max_length=255, null=True, blank=True)),
                ('fell_a_count', models.CharField(max_length=255, null=True, blank=True)),
                ('fell_b_score', models.CharField(max_length=255, null=True, blank=True)),
                ('fell_b_count', models.CharField(max_length=255, null=True, blank=True)),
                ('fell_c_score', models.CharField(max_length=255, null=True, blank=True)),
                ('fell_c_count', models.CharField(max_length=255, null=True, blank=True)),
                ('location_traffic', models.CharField(max_length=255, null=True, blank=True)),
                ('travel_schedule', models.CharField(max_length=255, null=True, blank=True)),
                ('dining_room', models.CharField(max_length=255, null=True, blank=True)),
                ('travel_traffic', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='XieChengSubPingLun',
            fields=[
                ('sub_pl_id', models.IntegerField(serialize=False, primary_key=True)),
                ('sub_pl_notes', models.CharField(max_length=200, null=True, blank=True)),
                ('sub_showGradeValue', models.CharField(max_length=50, null=True, blank=True)),
                ('sub_parent_id', models.CharField(max_length=20, null=True, blank=True)),
                ('sub_pl_text', models.CharField(max_length=1000, null=True, blank=True)),
                ('sub_pl_type', models.IntegerField(default=9999, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='XieChengTravelNote',
            fields=[
                ('note_id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('note_task_name', models.CharField(max_length=255, null=True, blank=True)),
                ('note_title', models.CharField(max_length=1000, null=True, blank=True)),
                ('note_content', models.TextField(null=True, blank=True)),
                ('note_user', models.CharField(max_length=255, null=True, blank=True)),
                ('note_date', models.DateTimeField(null=True, blank=True)),
                ('note_scrapy_date', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('note_answers', models.CharField(max_length=10, null=True, blank=True)),
                ('note_url', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='XieChengTravelNoteAnswer',
            fields=[
                ('answer_id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('answer_note_id', models.CharField(max_length=255, null=True, blank=True)),
                ('answer_content', models.CharField(max_length=1000, null=True, blank=True)),
                ('answer_parent_content', models.CharField(max_length=1000, null=True, blank=True)),
                ('answer_user', models.CharField(max_length=255, null=True, blank=True)),
                ('answer_date', models.DateTimeField(null=True, blank=True)),
                ('answer_scrapy_date', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
            ],
        ),
    ]
