# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-25 04:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sap_success_factors', '0004_catalogtransmissionaudit_audit_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsapsuccessfactorsenterprisecustomerconfiguration',
            name='history_change_reason',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
