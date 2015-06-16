# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import treeio.documents.models
import treeio.documents.files


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['-last_updated'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=255)),
                ('content', models.FileField(storage=treeio.documents.files.FileStorage(), upload_to=treeio.documents.models.generate_filename)),
            ],
            options={
                'ordering': ['-last_updated'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=255)),
                ('parent', models.ForeignKey(related_name='child_set', blank=True, to='documents.Folder', null=True)),
            ],
            options={
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='WebLink',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('title', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('folder', models.ForeignKey(to='documents.Folder')),
            ],
            options={
                'ordering': ['-last_updated'],
            },
            bases=('core.object',),
        ),
        migrations.AddField(
            model_name='file',
            name='folder',
            field=models.ForeignKey(to='documents.Folder'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='folder',
            field=models.ForeignKey(to='documents.Folder'),
            preserve_default=True,
        ),
    ]
