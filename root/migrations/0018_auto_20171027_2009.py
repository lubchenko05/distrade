# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-27 20:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0017_auto_20171027_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
