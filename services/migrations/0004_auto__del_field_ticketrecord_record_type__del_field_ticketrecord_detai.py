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

        # Deleting field 'TicketRecord.record_type'
        db.delete_column('services_ticketrecord', 'record_type')

        # Deleting field 'TicketRecord.details'
        db.delete_column('services_ticketrecord', 'details')

        # Deleting field 'TicketRecord.object_ptr'
        db.delete_column('services_ticketrecord', 'object_ptr_id')

        # Deleting field 'TicketRecord.ticket'
        db.delete_column('services_ticketrecord', 'ticket_id')

        # Changing field 'TicketRecord.updaterecord_ptr'
        db.alter_column('services_ticketrecord', 'updaterecord_ptr_id', self.gf(
            'django.db.models.fields.related.OneToOneField')(default=1, to=orm['core.UpdateRecord'], unique=True, primary_key=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for
        # 'TicketRecord.record_type'
        raise RuntimeError(
            "Cannot reverse this migration. 'TicketRecord.record_type' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for
        # 'TicketRecord.details'
        raise RuntimeError(
            "Cannot reverse this migration. 'TicketRecord.details' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for
        # 'TicketRecord.object_ptr'
        raise RuntimeError(
            "Cannot reverse this migration. 'TicketRecord.object_ptr' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for
        # 'TicketRecord.ticket'
        raise RuntimeError(
            "Cannot reverse this migration. 'TicketRecord.ticket' and its values cannot be restored.")

        # Changing field 'TicketRecord.updaterecord_ptr'
        db.alter_column('services_ticketrecord', 'updaterecord_ptr_id', self.gf(
            'django.db.models.fields.related.OneToOneField')(to=orm['core.UpdateRecord'], unique=True, null=True))

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
        'core.accessentity': {
            'Meta': {'object_name': 'AccessEntity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'core.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.User']", 'null': 'True', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'dislikes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'comments_disliked'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'comments_liked'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.User']"})
        },
        'core.group': {
            'Meta': {'ordering': "['name']", 'object_name': 'Group', '_ormbases': ['core.AccessEntity']},
            'accessentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.AccessEntity']", 'unique': 'True', 'primary_key': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['core.Group']"})
        },
        'core.object': {
            'Meta': {'object_name': 'Object'},
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'comments'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.Comment']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'objects_created'", 'null': 'True', 'to': "orm['core.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'dislikes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'objects_disliked'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.User']"}),
            'full_access': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'objects_full_access'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.AccessEntity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'likes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'objects_liked'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.User']"}),
            'links': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'links_rel_+'", 'null': 'True', 'to': "orm['core.Object']"}),
            'nuvius_resource': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'object_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'object_type': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'read_access': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'objects_read_access'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.AccessEntity']"}),
            'subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'subscriptions'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.User']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Tag']", 'null': 'True', 'blank': 'True'}),
            'trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.tag': {
            'Meta': {'ordering': "['name']", 'object_name': 'Tag'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'core.updaterecord': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'UpdateRecord'},
            'about': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'updates'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.Object']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sent_updates'", 'null': 'True', 'to': "orm['core.User']"}),
            'body': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'comments_on_updates'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.Comment']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'dislikes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'updates_disliked'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.User']"}),
            'format_message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'format_strings': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'updates_liked'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.User']"}),
            'recipients': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'received_updates'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.AccessEntity']"}),
            'record_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sent_updates'", 'null': 'True', 'to': "orm['core.Object']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        'core.user': {
            'Meta': {'ordering': "['name']", 'object_name': 'User', '_ormbases': ['core.AccessEntity']},
            'accessentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.AccessEntity']", 'unique': 'True', 'primary_key': 'True'}),
            'default_group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'default_user_set'", 'null': 'True', 'to': "orm['core.Group']"}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_access': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
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
            'related_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.AccessEntity']", 'null': 'True', 'blank': 'True'})
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
        'messaging.mailinglist': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'MailingList', '_ormbases': ['core.Object']},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'from_contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_contact_set'", 'to': "orm['identities.Contact']"}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'members_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['identities.Contact']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'opt_in': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['messaging.Template']", 'null': 'True', 'blank': 'True'})
        },
        'messaging.message': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'Message', '_ormbases': ['core.Object']},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['identities.Contact']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'mlist': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mlist'", 'null': 'True', 'to': "orm['messaging.MailingList']"}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'read_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'read_by_user'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.User']"}),
            'recipients': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'message_recipients'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['identities.Contact']"}),
            'reply_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['messaging.Message']"}),
            'stream': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'stream'", 'null': 'True', 'to': "orm['messaging.MessageStream']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'messaging.messagestream': {
            'Meta': {'ordering': "['name', 'last_updated']", 'object_name': 'MessageStream', '_ormbases': ['core.Object']},
            'faulty': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'incoming_password': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'incoming_server_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'incoming_server_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'incoming_server_username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'outgoing_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'outgoing_password': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'outgoing_server_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'outgoing_server_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'outgoing_server_username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'messaging.template': {
            'Meta': {'object_name': 'Template', '_ormbases': ['core.Object']},
            'body': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            'Meta': {'ordering': "['-date_created']", 'object_name': 'TicketRecord', '_ormbases': ['core.UpdateRecord']},
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['messaging.Message']", 'null': 'True', 'blank': 'True'}),
            'notify': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updaterecord_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.UpdateRecord']", 'unique': 'True', 'primary_key': 'True'})
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
