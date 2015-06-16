# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('identities', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=255)),
                ('details', models.TextField(max_length=255, null=True, blank=True)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ['start_date', 'name'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=255)),
                ('details', models.TextField(max_length=255, null=True, blank=True)),
                ('client', models.ForeignKey(related_name='client', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='identities.Contact', null=True)),
                ('manager', models.ForeignKey(related_name='manager', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='identities.Contact', null=True)),
                ('parent', models.ForeignKey(related_name='child_set', blank=True, to='projects.Project', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=255)),
                ('details', models.TextField(max_length=255, null=True, blank=True)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('priority', models.IntegerField(default=3, choices=[(5, 'Highest'), (4, 'High'), (3, 'Normal'), (2, 'Low'), (1, 'Lowest')])),
                ('estimated_time', models.IntegerField(null=True, blank=True)),
                ('assigned', models.ManyToManyField(to='core.User', null=True, blank=True)),
                ('caller', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='identities.Contact', null=True)),
                ('depends', models.ForeignKey(related_name='blocked_set', blank=True, to='projects.Task', null=True)),
                ('milestone', models.ForeignKey(blank=True, to='projects.Milestone', null=True)),
                ('parent', models.ForeignKey(related_name='child_set', blank=True, to='projects.Task', null=True)),
                ('project', models.ForeignKey(to='projects.Project')),
            ],
            options={
                'ordering': ('-priority', 'name'),
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=255)),
                ('details', models.TextField(max_length=255, null=True, blank=True)),
                ('active', models.BooleanField(default=False)),
                ('hidden', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('hidden', '-active', 'name'),
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='TaskTimeSlot',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('time_from', models.DateTimeField()),
                ('time_to', models.DateTimeField(null=True, blank=True)),
                ('timezone', models.IntegerField(default=0)),
                ('details', models.TextField(max_length=255, null=True, blank=True)),
                ('task', models.ForeignKey(to='projects.Task')),
                ('user', models.ForeignKey(to='core.User')),
            ],
            options={
                'ordering': ['-date_created'],
            },
            bases=('core.object',),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.ForeignKey(default=26, to='projects.TaskStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='milestone',
            name='project',
            field=models.ForeignKey(to='projects.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='milestone',
            name='status',
            field=models.ForeignKey(to='projects.TaskStatus'),
            preserve_default=True,
        ),
    ]
