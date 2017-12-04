# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-01 16:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MC2PConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=12, verbose_name='Key')),
                ('secret_key', models.CharField(max_length=32, verbose_name='Secret Key')),
            ],
            options={
                'verbose_name': 'MyChoice2Pay Configuration',
                'verbose_name_plural': 'MyChoice2Pay Configuration',
            },
        ),
    ]
