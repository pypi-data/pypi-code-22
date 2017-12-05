# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 02:21
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislative', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='billaction',
            name='extras',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='eventagendaitem',
            name='extras',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
    ]
