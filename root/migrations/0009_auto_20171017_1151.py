# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-17 11:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0008_auto_20171017_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 17, 11, 51, 32, 569296, tzinfo=utc)),
        ),
    ]
