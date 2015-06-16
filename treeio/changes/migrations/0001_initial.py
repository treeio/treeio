# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Change',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('change_type', models.CharField(max_length=255, null=True, blank=True)),
                ('field', models.CharField(max_length=255, null=True, blank=True)),
                ('change_from', models.TextField(null=True, blank=True)),
                ('change_to', models.TextField(null=True, blank=True)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'ordering': ['-date_created'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChangeSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('resolved_on', models.DateTimeField(null=True, blank=True)),
                ('details', models.TextField(null=True, blank=True)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('author', models.ForeignKey(related_name='author', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='core.User', null=True)),
            ],
            options={
                'ordering': ('-date_created', 'name'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChangeSetStatus',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=256)),
                ('details', models.TextField(null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('hidden', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('hidden', '-active', 'name'),
            },
            bases=('core.object',),
        ),
        migrations.AddField(
            model_name='changeset',
            name='object',
            field=models.ForeignKey(related_name='changeset_object_set', to='core.Object'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='changeset',
            name='resolved_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='core.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='changeset',
            name='status',
            field=models.ForeignKey(to='changes.ChangeSetStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='change',
            name='change_set',
            field=models.ForeignKey(to='changes.ChangeSet'),
            preserve_default=True,
        ),
    ]
