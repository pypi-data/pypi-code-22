# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('make_payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='makepayment',
            name='reference_number',
            field=models.CharField(default=b'', max_length=20, blank=True),
        ),
    ]
