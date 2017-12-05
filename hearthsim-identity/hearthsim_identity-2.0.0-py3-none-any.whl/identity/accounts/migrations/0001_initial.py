# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-13 22:42
from __future__ import unicode_literals

import uuid

import django.contrib.auth.models
import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
import django.utils.timezone
import django_intenum
import hearthstone.enums
from django.conf import settings
from django.db import migrations, models

import hearthsim.identity.accounts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('battletag', models.CharField(blank=True, help_text="The user's primary Battle.net username.", max_length=24)),
                ('is_fake', models.BooleanField(default=False)),
                ('locale', models.CharField(choices=[('enUS', 'English'), ('zhTW', 'Chinese (TW)'), ('zhCN', 'Chinese (CN)'), ('frFR', 'French'), ('deDE', 'German'), ('itIT', 'Italian'), ('jaJP', 'Japanese'), ('koKR', 'Korean'), ('plPL', 'Polish'), ('ptBR', 'Portuguese (BR)'), ('ruRU', 'Russian'), ('esES', 'Spanish (ES)'), ('esMX', 'Spanish (MX)'), ('thTH', 'Thai')], default='enUS', help_text="The user's preferred Hearthstone locale for display", max_length=8)),
                ('default_replay_visibility', django_intenum.IntEnumField(default=1, enum=hearthsim.identity.accounts.models.Visibility, verbose_name='Default replay visibility')),
                ('exclude_from_statistics', models.BooleanField(default=False)),
                ('joust_autoplay', models.BooleanField(default=True)),
                ('settings', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={})),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'users',
                'abstract': False,
                'verbose_name': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AccountClaim',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('api_key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.APIKey')),
            ],
        ),
        migrations.CreateModel(
            name='AccountDeleteRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(blank=True)),
                ('delete_replay_data', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AuthToken',
            fields=[
                ('key', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Key')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('test_data', models.BooleanField(default=False)),
                ('creation_apikey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tokens', to='api.APIKey')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='auth_tokens', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'api_authtoken',
            },
        ),
        migrations.CreateModel(
            name='BlizzardAccount',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('account_hi', models.BigIntegerField(help_text='The region value from account hilo', verbose_name='Account Hi')),
                ('account_lo', models.BigIntegerField(help_text='The account ID value from account hilo', verbose_name='Account Lo')),
                ('region', django_intenum.IntEnumField(enum=hearthstone.enums.BnetRegion)),
                ('battletag', models.CharField(blank=True, max_length=64)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blizzard_accounts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'games_pegasusaccount',
            },
        ),
        migrations.AddField(
            model_name='accountclaim',
            name='token',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.AuthToken'),
        ),
        migrations.AlterUniqueTogether(
            name='blizzardaccount',
            unique_together=set([('account_hi', 'account_lo')]),
        ),
    ]
