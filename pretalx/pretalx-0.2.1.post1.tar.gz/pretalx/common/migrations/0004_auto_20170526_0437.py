# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-26 09:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_activitylog_is_orga_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitylog',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='log_entries', to='event.Event'),
        ),
    ]
