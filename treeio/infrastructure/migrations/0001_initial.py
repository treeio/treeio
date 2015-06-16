# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('identities', '0001_initial'),
        ('finance', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=512)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='finance.Asset', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='ItemField',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=256)),
                ('label', models.CharField(max_length=256)),
                ('field_type', models.CharField(max_length=64, choices=[(b'text', b'Text'), (b'details', b'Details'), (b'url', b'URL'), (b'picture', b'Picture'), (b'date', b'Date')])),
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
            name='ItemServicing',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=256)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('expiry_date', models.DateField(null=True, blank=True)),
                ('details', models.TextField(blank=True)),
                ('items', models.ManyToManyField(to='infrastructure.Item', null=True, blank=True)),
                ('payments', models.ManyToManyField(to='finance.Transaction', null=True, blank=True)),
                ('supplier', models.ForeignKey(related_name='itemservice_supplied', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='identities.Contact', null=True)),
            ],
            options={
                'ordering': ['-expiry_date'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='ItemStatus',
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
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=512)),
                ('details', models.TextField(null=True, blank=True)),
                ('fields', models.ManyToManyField(to='infrastructure.ItemField', null=True, blank=True)),
                ('parent', models.ForeignKey(related_name='child_set', blank=True, to='infrastructure.ItemType', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='ItemValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField(blank=True)),
                ('field', models.ForeignKey(to='infrastructure.ItemField')),
                ('item', models.ForeignKey(to='infrastructure.Item')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='item',
            name='item_type',
            field=models.ForeignKey(to='infrastructure.ItemType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='core.Location', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='manufacturer',
            field=models.ForeignKey(related_name='items_manufactured', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='identities.Contact', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(related_name='items_owned', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='identities.Contact', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='parent',
            field=models.ForeignKey(related_name='child_set', blank=True, to='infrastructure.Item', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.ForeignKey(to='infrastructure.ItemStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='supplier',
            field=models.ForeignKey(related_name='items_supplied', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='identities.Contact', null=True),
            preserve_default=True,
        ),
    ]
