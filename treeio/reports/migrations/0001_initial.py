# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=255)),
                ('options', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=512)),
                ('model', models.TextField(null=True, blank=True)),
                ('content', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['-date_created'],
            },
            bases=('core.object',),
        ),
        migrations.AddField(
            model_name='chart',
            name='report',
            field=models.ForeignKey(to='reports.Report'),
            preserve_default=True,
        ),
    ]
