# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-24 16:57
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


def assign_checkin_lists(apps, schema_editor):
    AppConfiguration = apps.get_model('pretixdroid', 'AppConfiguration')

    for ac in AppConfiguration.objects.all():
        cl = ac.event.checkin_lists.get_or_create(subevent=ac.subevent, all_products=True, defaults={
            'name': ac.subevent.name if ac.subevent else 'Default'
        })[0]
        ac.list = cl
        ac.save()


class Migration(migrations.Migration):
    dependencies = [
        ('pretixbase', '0077_auto_20171124_1629'),
        ('pretixdroid', '0003_appconfiguration'),
    ]

    operations = [
        migrations.AddField(
            model_name='appconfiguration',
            name='list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='pretixbase.CheckinList'),
        ),
        migrations.AlterField(
            model_name='appconfiguration',
            name='all_items',
            field=models.BooleanField(default=True, verbose_name='Can scan all products'),
        ),
        migrations.AlterField(
            model_name='appconfiguration',
            name='allow_search',
            field=models.BooleanField(default=True,
                                      help_text='If disabled, the device can not search for attendees by name. pretixdroid 1.6 or newer only.',
                                      verbose_name='Search allowed'),
        ),
        migrations.AlterField(
            model_name='appconfiguration',
            name='items',
            field=models.ManyToManyField(blank=True, to='pretixbase.Item', verbose_name='Can scan these products'),
        ),
        migrations.AlterField(
            model_name='appconfiguration',
            name='show_info',
            field=models.BooleanField(default=True,
                                      help_text='If disabled, the device can not see how many tickets exist and how many are already scanned. pretixdroid 1.6 or newer only.',
                                      verbose_name='Show information'),
        ),
        migrations.RunPython(
            assign_checkin_lists,
            migrations.RunPython.noop
        ),
        migrations.RemoveField(
            model_name='appconfiguration',
            name='subevent',
        ),
        migrations.AlterField(
            model_name='appconfiguration',
            name='list',
            field=models.ForeignKey(blank=False, null=False, on_delete=django.db.models.deletion.CASCADE,
                                    to='pretixbase.CheckinList'),
        ),
    ]
