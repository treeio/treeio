# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KnowledgeCategory',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=255)),
                ('details', models.TextField(max_length=255, null=True, blank=True)),
                ('treepath', models.CharField(max_length=800)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='KnowledgeFolder',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=255)),
                ('details', models.TextField(max_length=255, null=True, blank=True)),
                ('treepath', models.CharField(max_length=800)),
                ('parent', models.ForeignKey(related_name='child_set', blank=True, to='knowledge.KnowledgeFolder', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='KnowledgeItem',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=255)),
                ('body', models.TextField(null=True, blank=True)),
                ('treepath', models.CharField(max_length=800)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='knowledge.KnowledgeCategory', null=True)),
                ('folder', models.ForeignKey(to='knowledge.KnowledgeFolder')),
            ],
            options={
                'ordering': ['-last_updated'],
            },
            bases=('core.object',),
        ),
    ]
