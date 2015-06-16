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
            name='MailingList',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('from_contact', models.ForeignKey(related_name='from_contact_set', to='identities.Contact')),
                ('members', models.ManyToManyField(related_name='members_set', null=True, to='identities.Contact', blank=True)),
            ],
            options={
                'ordering': ['-date_created'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('body', models.TextField()),
                ('author', models.ForeignKey(to='identities.Contact')),
                ('mlist', models.ForeignKey(related_name='mlist', blank=True, to='messaging.MailingList', null=True)),
                ('read_by', models.ManyToManyField(related_name='read_by_user', null=True, to='core.User', blank=True)),
                ('recipients', models.ManyToManyField(related_name='message_recipients', null=True, to='identities.Contact', blank=True)),
                ('reply_to', models.ForeignKey(related_name='child_set', blank=True, to='messaging.Message', null=True)),
            ],
            options={
                'ordering': ['-date_created'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='MessageStream',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=255)),
                ('incoming_server_name', models.CharField(max_length=255, null=True, blank=True)),
                ('incoming_server_type', models.CharField(blank=True, max_length=255, null=True, choices=[(b'POP3', b'POP3'), (b'POP3-SSL', b'POP3-SSL'), (b'IMAP', b'IMAP'), (b'IMAP-SSL', b'IMAP-SSL')])),
                ('incoming_server_username', models.CharField(max_length=255, null=True, blank=True)),
                ('incoming_password', models.CharField(max_length=255, null=True, blank=True)),
                ('outgoing_email', models.EmailField(max_length=255, null=True, blank=True)),
                ('outgoing_server_name', models.CharField(max_length=255, null=True, blank=True)),
                ('outgoing_server_type', models.CharField(blank=True, max_length=255, null=True, choices=[(b'SMTP', b'SMTP'), (b'SMTP-SSL', b'SMTP-SSL')])),
                ('outgoing_server_username', models.CharField(max_length=255, null=True, blank=True)),
                ('outgoing_password', models.CharField(max_length=255, null=True, blank=True)),
                ('faulty', models.BooleanField(default=False)),
                ('last_checked', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ['name', 'last_updated'],
                'verbose_name': 'Stream',
                'verbose_name_plural': 'Streams',
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('subject', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=('core.object',),
        ),
        migrations.AddField(
            model_name='message',
            name='stream',
            field=models.ForeignKey(related_name='stream', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='messaging.MessageStream', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mailinglist',
            name='opt_in',
            field=models.ForeignKey(blank=True, to='messaging.Template', null=True),
            preserve_default=True,
        ),
    ]
