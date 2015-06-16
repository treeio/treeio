# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField(default=b'', null=True, blank=True)),
                ('ntype', models.CharField(max_length=1, choices=[(b'd', 'Daily'), (b'w', 'Weekly'), (b'm', 'Monthly')])),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('recipient', models.ForeignKey(to='core.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NotificationSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ntype', models.CharField(max_length=1, verbose_name=b'Type', choices=[(b'd', 'Daily'), (b'w', 'Weekly'), (b'm', 'Monthly')])),
                ('next_date', models.DateField(null=True, blank=True)),
                ('last_datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('enabled', models.BooleanField(default=True)),
                ('modules', models.ManyToManyField(to='core.Module')),
                ('owner', models.ForeignKey(to='core.User', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
