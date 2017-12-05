# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-28 09:01
from __future__ import unicode_literals

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import pretix.base.models.base


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0074_auto_20170825_1258'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventMetaProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Can not contain spaces or special characters execpt underscores', max_length=50, validators=[django.core.validators.RegexValidator(message='The property name may only contain letters, numbers and underscores.', regex='^[a-zA-Z0-9_]+$')], verbose_name='Name')),
                ('default', models.TextField()),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meta_properties', to='pretixbase.Organizer')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, pretix.base.models.base.LoggingMixin),
        ),
        migrations.CreateModel(
            name='EventMetaValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meta_values', to='pretixbase.Event')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_values', to='pretixbase.EventMetaProperty')),
            ],
            bases=(models.Model, pretix.base.models.base.LoggingMixin),
        ),
        migrations.CreateModel(
            name='SubEventMetaValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subevent_values', to='pretixbase.EventMetaProperty')),
                ('subevent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meta_values', to='pretixbase.SubEvent')),
            ],
            bases=(models.Model, pretix.base.models.base.LoggingMixin),
        ),
        migrations.AlterUniqueTogether(
            name='subeventmetavalue',
            unique_together=set([('subevent', 'property')]),
        ),
        migrations.AlterUniqueTogether(
            name='eventmetavalue',
            unique_together=set([('event', 'property')]),
        ),
    ]
