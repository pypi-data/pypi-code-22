# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-08 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banktransfer', '0002_auto_20160908_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='banktransaction',
            name='comment',
            field=models.TextField(blank=True),
        ),
    ]
