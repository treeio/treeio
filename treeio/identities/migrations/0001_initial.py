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
            name='Contact',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='ContactField',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=256)),
                ('label', models.CharField(max_length=256)),
                ('field_type', models.CharField(max_length=64, choices=[(b'text', b'Text'), (b'textarea', b'Multiline Text'), (b'details', b'Details'), (b'url', b'URL'), (b'email', b'E-mail'), (b'phone', b'Phone'), (b'picture', b'Picture'), (b'date', b'Date')])),
                ('required', models.BooleanField(default=False)),
                ('allowed_values', models.TextField(null=True, blank=True)),
                ('details', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='ContactType',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=256)),
                ('slug', models.CharField(max_length=256)),
                ('details', models.TextField(null=True, blank=True)),
                ('fields', models.ManyToManyField(to='identities.ContactField', null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='ContactValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=1024, null=True, blank=True)),
                ('contact', models.ForeignKey(to='identities.Contact')),
                ('field', models.ForeignKey(to='identities.ContactField')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contact',
            name='contact_type',
            field=models.ForeignKey(to='identities.ContactType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='parent',
            field=models.ForeignKey(related_name='child_set', blank=True, to='identities.Contact', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='related_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='core.AccessEntity', null=True),
            preserve_default=True,
        ),
    ]
