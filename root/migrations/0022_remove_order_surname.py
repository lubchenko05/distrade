# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-28 18:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0021_auto_20171028_1442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='surname',
        ),
    ]
