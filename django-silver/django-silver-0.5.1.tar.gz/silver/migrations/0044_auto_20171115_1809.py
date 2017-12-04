# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 18:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0043_auto_20171113_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billinglog',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='billing_logs', to='silver.Subscription'),
        ),
    ]
