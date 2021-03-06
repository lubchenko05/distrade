# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-28 11:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0018_auto_20171027_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='root.Product'),
        ),
    ]
