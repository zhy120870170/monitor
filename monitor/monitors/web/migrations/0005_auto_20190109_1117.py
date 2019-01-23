# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_mafwask_mafwaskanswer_mafwspider_mafwtravelbook_qyerask_qyeraskanswer_qyerbbs_qyerspider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qyeraskanswer',
            name='answer_content',
            field=models.CharField(max_length=4000, null=True, blank=True),
        ),
    ]
