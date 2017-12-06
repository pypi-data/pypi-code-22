# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 13:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('submission', '0008_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='answers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='target',
            field=models.CharField(choices=[('submission', 'per submission'), ('speaker', 'per speaker')], default='submission', max_length=10),
        ),
        migrations.AlterField(
            model_name='answer',
            name='submission',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='answers', to='submission.Submission'),
        ),
    ]
