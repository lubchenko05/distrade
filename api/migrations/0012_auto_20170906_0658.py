# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-06 06:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20170906_0646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(blank='True', max_length=255),
        ),
    ]
