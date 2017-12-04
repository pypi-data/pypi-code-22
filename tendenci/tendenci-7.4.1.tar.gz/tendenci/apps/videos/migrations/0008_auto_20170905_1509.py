# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0007_auto_20170905_1455'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ('position',), 'verbose_name': 'Videos', 'verbose_name_plural': 'Videos', 'permissions': (('view_video', 'Can view video'),)},
        ),
        migrations.RemoveField(
            model_name='video',
            name='ordering',
        ),
    ]
