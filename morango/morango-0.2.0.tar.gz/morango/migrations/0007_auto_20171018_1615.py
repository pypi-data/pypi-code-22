# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-10-18 21:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone
import morango.utils.uuids


class Migration(migrations.Migration):

    dependencies = [
        ('morango', '0006_instanceidmodel_system_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nonce',
            fields=[
                ('id', morango.utils.uuids.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('ip', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='scopedefinition',
            old_name='read_scope_def',
            new_name='read_filter_template',
        ),
        migrations.RenameField(
            model_name='scopedefinition',
            old_name='read_write_scope_def',
            new_name='read_write_filter_template',
        ),
        migrations.RenameField(
            model_name='scopedefinition',
            old_name='write_scope_def',
            new_name='write_filter_template',
        ),
        migrations.RenameField(
            model_name='transfersession',
            old_name='incoming',
            new_name='push',
        ),
        migrations.RemoveField(
            model_name='syncsession',
            name='host',
        ),
        migrations.RemoveField(
            model_name='syncsession',
            name='local_scope',
        ),
        migrations.RemoveField(
            model_name='syncsession',
            name='remote_scope',
        ),
        migrations.RemoveField(
            model_name='transfersession',
            name='chunksize',
        ),
        migrations.RemoveField(
            model_name='transfersession',
            name='records_remaining',
        ),
        migrations.AddField(
            model_name='buffer',
            name='_self_ref_fk',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name='buffer',
            name='source_id',
            field=models.CharField(default=datetime.datetime(2017, 10, 18, 21, 13, 11, 488565, tzinfo=utc), max_length=96),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='certificate',
            name='salt',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name='databasemaxcounter',
            name='partition',
            field=models.CharField(default=b'', max_length=128),
        ),
        migrations.AddField(
            model_name='store',
            name='_self_ref_fk',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name='store',
            name='dirty_bit',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='store',
            name='source_id',
            field=models.CharField(default=datetime.datetime(2017, 10, 18, 21, 15, 6, 842850, tzinfo=utc), max_length=96),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='syncsession',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='syncsession',
            name='connection_kind',
            field=models.CharField(choices=[('network', 'Network'), ('disk', 'Disk')], default=datetime.datetime(2017, 10, 18, 21, 15, 12, 858664, tzinfo=utc), max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='syncsession',
            name='connection_path',
            field=models.CharField(default=datetime.datetime(2017, 10, 18, 21, 15, 21, 147686, tzinfo=utc), max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='syncsession',
            name='is_server',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='syncsession',
            name='local_certificate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='syncsessions_local', to='morango.Certificate'),
        ),
        migrations.AddField(
            model_name='syncsession',
            name='local_instance',
            field=models.TextField(default='{}'),
        ),
        migrations.AddField(
            model_name='syncsession',
            name='local_ip',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='syncsession',
            name='profile',
            field=models.CharField(default=datetime.datetime(2017, 10, 18, 21, 15, 27, 811735, tzinfo=utc), max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='syncsession',
            name='remote_certificate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='syncsessions_remote', to='morango.Certificate'),
        ),
        migrations.AddField(
            model_name='syncsession',
            name='remote_instance',
            field=models.TextField(default='{}'),
        ),
        migrations.AddField(
            model_name='syncsession',
            name='remote_ip',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='transfersession',
            name='last_activity_timestamp',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 10, 18, 21, 15, 30, 154629, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transfersession',
            name='local_fsic',
            field=models.TextField(blank=True, default=b'{}'),
        ),
        migrations.AddField(
            model_name='transfersession',
            name='records_transferred',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='transfersession',
            name='remote_fsic',
            field=models.TextField(blank=True, default=b'{}'),
        ),
        migrations.AddField(
            model_name='transfersession',
            name='start_timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='syncsession',
            name='id',
            field=morango.utils.uuids.UUIDField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='transfersession',
            name='id',
            field=morango.utils.uuids.UUIDField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='transfersession',
            name='records_total',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='buffer',
            unique_together=set([('transfer_session', 'model_uuid')]),
        ),
        migrations.RemoveField(
            model_name='databasemaxcounter',
            name='filter',
        ),
        migrations.AlterUniqueTogether(
            name='databasemaxcounter',
            unique_together=set([('instance_id', 'partition')]),
        ),
    ]
