# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-11 11:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0038_auto_20170724_0708'),
    ]

    operations = [
        migrations.AddField(
            model_name='billinglog',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
