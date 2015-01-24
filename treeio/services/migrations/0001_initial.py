# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'TicketStatus'
        db.create_table('services_ticketstatus', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=256)),
            ('details', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')
             (default=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')
             (default=False)),
        ))
        db.send_create_signal('services', ['TicketStatus'])

        # Adding model 'Service'
        db.create_table('services_service', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=256)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(
                blank=True, related_name='child_set', null=True, to=orm['services.Service'])),
            ('details', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('services', ['Service'])

        # Adding model 'ServiceLevelAgreement'
        db.create_table('services_servicelevelagreement', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=256)),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['services.Service'])),
            ('default', self.gf('django.db.models.fields.BooleanField')
             (default=False)),
            ('response_time', self.gf('django.db.models.fields.PositiveIntegerField')(
                null=True, blank=True)),
            ('uptime_rate', self.gf('django.db.models.fields.FloatField')
             (null=True, blank=True)),
            ('available_from', self.gf('django.db.models.fields.TimeField')
             (null=True, blank=True)),
            ('available_to', self.gf('django.db.models.fields.TimeField')
             (null=True, blank=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(
                blank=True, related_name='client_sla', null=True, to=orm['identities.Contact'])),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')
             (related_name='provider_sla', to=orm['identities.Contact'])),
        ))
        db.send_create_signal('services', ['ServiceLevelAgreement'])

        # Adding model 'ServiceAgent'
        db.create_table('services_serviceagent', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('related_user', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['core.User'])),
            ('active', self.gf('django.db.models.fields.BooleanField')
             (default=True)),
            ('occupied', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
            ('available_from', self.gf('django.db.models.fields.TimeField')
             (null=True, blank=True)),
            ('available_to', self.gf('django.db.models.fields.TimeField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('services', ['ServiceAgent'])

        # Adding model 'TicketQueue'
        db.create_table('services_ticketqueue', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=256)),
            ('active', self.gf('django.db.models.fields.BooleanField')
             (default=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(
                blank=True, related_name='child_set', null=True, to=orm['services.TicketQueue'])),
            ('default_ticket_status', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['services.TicketStatus'], null=True, blank=True)),
            ('default_ticket_priority', self.gf(
                'django.db.models.fields.IntegerField')(default=3)),
            ('default_service', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['services.Service'], null=True, blank=True)),
            ('waiting_time', self.gf('django.db.models.fields.PositiveIntegerField')(
                null=True, blank=True)),
            ('next_queue', self.gf('django.db.models.fields.related.ForeignKey')(
                blank=True, related_name='previous_set', null=True, to=orm['services.TicketQueue'])),
            ('ticket_code', self.gf('django.db.models.fields.CharField')
             (default='', max_length=8, null=True, blank=True)),
            ('message_stream', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['messaging.MessageStream'], null=True, blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('services', ['TicketQueue'])

        # Adding model 'Ticket'
        db.create_table('services_ticket', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('reference', self.gf(
                'django.db.models.fields.CharField')(max_length=256)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=256)),
            ('caller', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['identities.Contact'], null=True, blank=True)),
            ('urgency', self.gf(
                'django.db.models.fields.IntegerField')(default=3)),
            ('priority', self.gf(
                'django.db.models.fields.IntegerField')(default=3)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['services.TicketStatus'])),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['services.Service'], null=True, blank=True)),
            ('sla', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['services.ServiceLevelAgreement'], null=True, blank=True)),
            ('queue', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['services.TicketQueue'], null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['messaging.Message'], null=True, blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
            ('resolution', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('services', ['Ticket'])

        # Adding M2M table for field assigned on 'Ticket'
        db.create_table('services_ticket_assigned', (
            ('id', models.AutoField(
                verbose_name='ID', primary_key=True, auto_created=True)),
            ('ticket', models.ForeignKey(orm['services.ticket'], null=False)),
            ('serviceagent', models.ForeignKey(
                orm['services.serviceagent'], null=False))
        ))
        db.create_unique(
            'services_ticket_assigned', ['ticket_id', 'serviceagent_id'])

        # Adding model 'TicketRecord'
        db.create_table('services_ticketrecord', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('ticket', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['services.Ticket'])),
            ('record_type', self.gf(
                'django.db.models.fields.CharField')(max_length=256)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['messaging.Message'], null=True, blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')()),
            ('notify', self.gf('django.db.models.fields.BooleanField')
             (default=False)),
        ))
        db.send_create_signal('services', ['TicketRecord'])

    def backwards(self, orm):

        # Deleting model 'TicketStatus'
        db.delete_table('services_ticketstatus')

        # Deleting model 'Service'
        db.delete_table('services_service')

        # Deleting model 'ServiceLevelAgreement'
        db.delete_table('services_servicelevelagreement')

        # Deleting model 'ServiceAgent'
        db.delete_table('services_serviceagent')

        # Deleting model 'TicketQueue'
        db.delete_table('services_ticketqueue')

        # Deleting model 'Ticket'
        db.delete_table('services_ticket')

        # Removing M2M table for field assigned on 'Ticket'
        db.delete_table('services_ticket_assigned')

        # Deleting model 'TicketRecord'
        db.delete_table('services_ticketrecord')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.group': {
            'Meta': {'ordering': "['name']", 'object_name': 'Group'},
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['core.Group']"})
        },
        'core.object': {
            'Meta': {'object_name': 'Object'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'everybody_execute': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'everybody_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'everybody_write': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Group']"}),
            'group_execute': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'group_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'group_write': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'links': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'links_rel_+'", 'null': 'True', 'to': "orm['core.Object']"}),
            'nuvius_resource': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'object_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'object_type': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'subscriptions'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.User']"}),
            'trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.User']"}),
            'user_execute': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_write': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.user': {
            'Meta': {'ordering': "['name']", 'object_name': 'User'},
            'default_group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'default_user_set'", 'null': 'True', 'to': "orm['core.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'other_groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Group']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'identities.contact': {
            'Meta': {'ordering': "['name']", 'object_name': 'Contact', '_ormbases': ['core.Object']},
            'contact_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['identities.ContactType']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['identities.Contact']"}),
            'related_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Group']", 'null': 'True', 'blank': 'True'}),
            'related_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.User']", 'null': 'True', 'blank': 'True'})
        },
        'identities.contactfield': {
            'Meta': {'ordering': "['name']", 'object_name': 'ContactField', '_ormbases': ['core.Object']},
            'allowed_values': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'identities.contacttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ContactType', '_ormbases': ['core.Object']},
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fields': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['identities.ContactField']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'messaging.emailbox': {
            'Meta': {'ordering': "['last_updated']", 'object_name': 'EmailBox', '_ormbases': ['core.Object']},
            'email_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'server_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'server_password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'server_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'server_username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'messaging.message': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'Message', '_ormbases': ['core.Object']},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['identities.Contact']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'read_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'read_by_user'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.User']"}),
            'reply_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['messaging.Message']"}),
            'stream': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stream'", 'to': "orm['messaging.MessageStream']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'messaging.messagestream': {
            'Meta': {'ordering': "['name']", 'object_name': 'MessageStream', '_ormbases': ['core.Object']},
            'email_incoming': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'incoming'", 'null': 'True', 'to': "orm['messaging.EmailBox']"}),
            'email_outgoing': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'outgoing'", 'null': 'True', 'to': "orm['messaging.EmailBox']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'})
        },
        'services.service': {
            'Meta': {'ordering': "['name']", 'object_name': 'Service', '_ormbases': ['core.Object']},
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['services.Service']"})
        },
        'services.serviceagent': {
            'Meta': {'ordering': "('related_user', '-active', 'occupied')", 'object_name': 'ServiceAgent', '_ormbases': ['core.Object']},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'available_from': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'available_to': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'occupied': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'related_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.User']"})
        },
        'services.servicelevelagreement': {
            'Meta': {'ordering': "('name', 'client')", 'object_name': 'ServiceLevelAgreement', '_ormbases': ['core.Object']},
            'available_from': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'available_to': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'client_sla'", 'null': 'True', 'to': "orm['identities.Contact']"}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'provider_sla'", 'to': "orm['identities.Contact']"}),
            'response_time': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['services.Service']"}),
            'uptime_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'services.ticket': {
            'Meta': {'ordering': "('-priority', 'reference')", 'object_name': 'Ticket', '_ormbases': ['core.Object']},
            'assigned': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['services.ServiceAgent']", 'null': 'True', 'blank': 'True'}),
            'caller': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['identities.Contact']", 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['messaging.Message']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'queue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['services.TicketQueue']", 'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'resolution': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['services.Service']", 'null': 'True', 'blank': 'True'}),
            'sla': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['services.ServiceLevelAgreement']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['services.TicketStatus']"}),
            'urgency': ('django.db.models.fields.IntegerField', [], {'default': '3'})
        },
        'services.ticketqueue': {
            'Meta': {'ordering': "('name', '-active', 'ticket_code')", 'object_name': 'TicketQueue', '_ormbases': ['core.Object']},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'default_service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['services.Service']", 'null': 'True', 'blank': 'True'}),
            'default_ticket_priority': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'default_ticket_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['services.TicketStatus']", 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'message_stream': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['messaging.MessageStream']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'next_queue': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'previous_set'", 'null': 'True', 'to': "orm['services.TicketQueue']"}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['services.TicketQueue']"}),
            'ticket_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'waiting_time': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'services.ticketrecord': {
            'Meta': {'ordering': "['ticket']", 'object_name': 'TicketRecord', '_ormbases': ['core.Object']},
            'details': ('django.db.models.fields.TextField', [], {}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['messaging.Message']", 'null': 'True', 'blank': 'True'}),
            'notify': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'record_type': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'ticket': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['services.Ticket']"})
        },
        'services.ticketstatus': {
            'Meta': {'ordering': "('hidden', '-active', 'name')", 'object_name': 'TicketStatus', '_ormbases': ['core.Object']},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['services']
