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
            name='Event',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=255)),
                ('details', models.TextField(max_length=255, null=True, blank=True)),
                ('start', models.DateTimeField(null=True, blank=True)),
                ('end', models.DateTimeField()),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='core.Location', null=True)),
            ],
            options={
                'ordering': ['-end'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=255, choices=[(b'attending', b'Attending'), (b'pending', b'Pending'), (b'not-attending', b'Not Attending')])),
                ('contact', models.ForeignKey(to='identities.Contact')),
                ('event', models.ForeignKey(to='events.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
