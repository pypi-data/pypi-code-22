# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 22:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0005_auto_20160531_1058'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrintPublication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
                ('priority', models.PositiveSmallIntegerField(default=10, help_text=b'In the list of all active print publications, how high should this entry show up?')),
                ('is_active', models.BooleanField(default=True, help_text=b'Should this publication be included in the current options users can choose from? If false, this publication will be archived, but it may be re-activated in the future.')),
            ],
            options={
                'ordering': ['priority', 'is_active', 'slug'],
            },
        ),
        migrations.AddField(
            model_name='package',
            name='print_publication',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='budget.PrintPublication'),
        ),
    ]
