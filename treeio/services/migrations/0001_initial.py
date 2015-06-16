# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('identities', '0001_initial'),
        ('core', '0001_initial'),
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=256)),
                ('details', models.TextField(null=True, blank=True)),
                ('parent', models.ForeignKey(related_name='child_set', blank=True, to='services.Service', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='ServiceAgent',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('active', models.BooleanField(default=True)),
                ('occupied', models.BooleanField(default=False)),
                ('available_from', models.TimeField(null=True, blank=True)),
                ('available_to', models.TimeField(null=True, blank=True)),
                ('related_user', models.ForeignKey(to='core.User')),
            ],
            options={
                'ordering': ('related_user', '-active', 'occupied'),
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='ServiceLevelAgreement',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=256)),
                ('default', models.BooleanField(default=False)),
                ('response_time', models.PositiveIntegerField(null=True, blank=True)),
                ('uptime_rate', models.FloatField(null=True, blank=True)),
                ('available_from', models.TimeField(null=True, blank=True)),
                ('available_to', models.TimeField(null=True, blank=True)),
                ('client', models.ForeignKey(related_name='client_sla', blank=True, to='identities.Contact', null=True)),
                ('provider', models.ForeignKey(related_name='provider_sla', to='identities.Contact')),
                ('service', models.ForeignKey(to='services.Service')),
            ],
            options={
                'ordering': ('name', 'client'),
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('reference', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=256)),
                ('urgency', models.IntegerField(default=3, choices=[(5, 'Highest'), (4, 'High'), (3, 'Normal'), (2, 'Low'), (1, 'Lowest')])),
                ('priority', models.IntegerField(default=3, choices=[(5, 'Highest'), (4, 'High'), (3, 'Normal'), (2, 'Low'), (1, 'Lowest')])),
                ('details', models.TextField(null=True, blank=True)),
                ('resolution', models.TextField(null=True, blank=True)),
                ('assigned', models.ManyToManyField(to='services.ServiceAgent', null=True, blank=True)),
                ('caller', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='identities.Contact', null=True)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='messaging.Message', null=True)),
            ],
            options={
                'ordering': ('-priority', 'reference'),
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='TicketQueue',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=256)),
                ('active', models.BooleanField(default=True)),
                ('default_ticket_priority', models.IntegerField(default=3, choices=[(5, b'Highest'), (4, b'High'), (3, b'Normal'), (2, b'Low'), (1, b'Lowest')])),
                ('waiting_time', models.PositiveIntegerField(null=True, blank=True)),
                ('ticket_code', models.CharField(default=b'', max_length=8, null=True, blank=True)),
                ('details', models.TextField(null=True, blank=True)),
                ('default_service', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='services.Service', null=True)),
            ],
            options={
                'ordering': ('name', '-active', 'ticket_code'),
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='TicketRecord',
            fields=[
                ('updaterecord_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.UpdateRecord')),
                ('notify', models.BooleanField(default=False)),
                ('message', models.ForeignKey(blank=True, to='messaging.Message', null=True)),
            ],
            options={
            },
            bases=('core.updaterecord',),
        ),
        migrations.CreateModel(
            name='TicketStatus',
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
            model_name='ticketqueue',
            name='default_ticket_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='services.TicketStatus', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticketqueue',
            name='message_stream',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='messaging.MessageStream', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticketqueue',
            name='next_queue',
            field=models.ForeignKey(related_name='previous_set', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='services.TicketQueue', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticketqueue',
            name='parent',
            field=models.ForeignKey(related_name='child_set', blank=True, to='services.TicketQueue', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='queue',
            field=models.ForeignKey(blank=True, to='services.TicketQueue', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='services.Service', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='sla',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='services.ServiceLevelAgreement', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='status',
            field=models.ForeignKey(to='services.TicketStatus'),
            preserve_default=True,
        ),
    ]
