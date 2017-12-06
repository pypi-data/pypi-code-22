# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-14 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0009_auto_20171106_0608'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpermission',
            name='review_override_count',
            field=models.PositiveIntegerField(default=0, help_text='How many times may this user cast an overriding votes or vetos?', verbose_name='Override votes for reviews'),
        ),
    ]
