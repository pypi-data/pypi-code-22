# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-29 00:06
from __future__ import unicode_literals

import django.contrib.postgres.fields.ranges
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0037_auto_20171028_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentplacement',
            name='run_date',
            field=django.contrib.postgres.fields.ranges.DateRangeField(),
        ),
    ]
