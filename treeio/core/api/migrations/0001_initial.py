# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('key', models.CharField(unique=True, max_length=18)),
                ('secret', models.CharField(max_length=32)),
                ('status', models.CharField(default=b'accepted', max_length=16, choices=[(b'pending', b'Pending'), (b'accepted', b'Accepted'), (b'canceled', b'Canceled'), (b'rejected', b'Rejected')])),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Nonce',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token_key', models.CharField(max_length=18)),
                ('consumer_key', models.CharField(max_length=18)),
                ('key', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=18)),
                ('secret', models.CharField(max_length=32)),
                ('verifier', models.CharField(max_length=10)),
                ('token_type', models.IntegerField(choices=[(1, 'Request'), (2, 'Access')])),
                ('timestamp', models.IntegerField(default=1433872772L)),
                ('is_approved', models.BooleanField(default=False)),
                ('consumer_id', models.IntegerField(null=True, blank=True)),
                ('callback', models.CharField(max_length=255, null=True, blank=True)),
                ('callback_confirmed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(related_name='tokens', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
