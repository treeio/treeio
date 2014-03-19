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

        # Adding model 'MailingList'
        db.create_table('messaging_mailinglist', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
            ('from_contact', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='from_contact_set', to=orm['identities.Contact'])),
            ('opt_in', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['messaging.Template'], null=True, blank=True)),
        ))
        db.send_create_signal('messaging', ['MailingList'])

        # Adding M2M table for field members on 'MailingList'
        db.create_table('messaging_mailinglist_members', (
            ('id', models.AutoField(
                verbose_name='ID', primary_key=True, auto_created=True)),
            ('mailinglist', models.ForeignKey(
                orm['messaging.mailinglist'], null=False)),
            ('contact', models.ForeignKey(
                orm['identities.contact'], null=False))
        ))
        db.create_unique(
            'messaging_mailinglist_members', ['mailinglist_id', 'contact_id'])

        # Adding model 'Template'
        db.create_table('messaging_template', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=255)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('subject', self.gf('django.db.models.fields.CharField')
             (max_length=255)),
        ))
        db.send_create_signal('messaging', ['Template'])

        # Adding field 'Message.mlist'
        db.add_column('messaging_message', 'mlist', self.gf('django.db.models.fields.related.ForeignKey')(
            blank=True, related_name='mlist', null=True, to=orm['messaging.MailingList']), keep_default=False)

        # Adding M2M table for field recipients on 'Message'
        db.create_table('messaging_message_recipients', (
            ('id', models.AutoField(
                verbose_name='ID', primary_key=True, auto_created=True)),
            ('message', models.ForeignKey(
                orm['messaging.message'], null=False)),
            ('contact', models.ForeignKey(
                orm['identities.contact'], null=False))
        ))
        db.create_unique(
            'messaging_message_recipients', ['message_id', 'contact_id'])

        # Changing field 'Message.stream'
        db.alter_column('messaging_message', 'stream_id', self.gf(
            'django.db.models.fields.related.ForeignKey')(null=True, to=orm['messaging.MessageStream']))

        # Adding field 'MessageStream.incoming_server_name'
        db.add_column('messaging_messagestream', 'incoming_server_name', self.gf(
            'django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'MessageStream.incoming_server_type'
        db.add_column('messaging_messagestream', 'incoming_server_type', self.gf(
            'django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'MessageStream.incoming_server_username'
        db.add_column('messaging_messagestream', 'incoming_server_username', self.gf(
            'django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'MessageStream.incoming_password'
        db.add_column('messaging_messagestream', 'incoming_password', self.gf(
            'django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'MessageStream.outgoing_email'
        db.add_column('messaging_messagestream', 'outgoing_email', self.gf(
            'django.db.models.fields.EmailField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'MessageStream.outgoing_server_name'
        db.add_column('messaging_messagestream', 'outgoing_server_name', self.gf(
            'django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'MessageStream.outgoing_server_type'
        db.add_column('messaging_messagestream', 'outgoing_server_type', self.gf(
            'django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'MessageStream.outgoing_server_username'
        db.add_column('messaging_messagestream', 'outgoing_server_username', self.gf(
            'django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'MessageStream.outgoing_password'
        db.add_column('messaging_messagestream', 'outgoing_password', self.gf(
            'django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'MessageStream.faulty'
        db.add_column('messaging_messagestream', 'faulty', self.gf(
            'django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'MessageStream.last_checked'
        db.add_column('messaging_messagestream', 'last_checked', self.gf(
            'django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

    def backwards(self, orm):

        # Deleting model 'MailingList'
        db.delete_table('messaging_mailinglist')

        # Removing M2M table for field members on 'MailingList'
        db.delete_table('messaging_mailinglist_members')

        # Deleting model 'Template'
        db.delete_table('messaging_template')

        # Deleting field 'Message.mlist'
        db.delete_column('messaging_message', 'mlist_id')

        # Removing M2M table for field recipients on 'Message'
        db.delete_table('messaging_message_recipients')

        # User chose to not deal with backwards NULL issues for
        # 'Message.stream'
        raise RuntimeError(
            "Cannot reverse this migration. 'Message.stream' and its values cannot be restored.")

        # Deleting field 'MessageStream.incoming_server_name'
        db.delete_column('messaging_messagestream', 'incoming_server_name')

        # Deleting field 'MessageStream.incoming_server_type'
        db.delete_column('messaging_messagestream', 'incoming_server_type')

        # Deleting field 'MessageStream.incoming_server_username'
        db.delete_column('messaging_messagestream', 'incoming_server_username')

        # Deleting field 'MessageStream.incoming_password'
        db.delete_column('messaging_messagestream', 'incoming_password')

        # Deleting field 'MessageStream.outgoing_email'
        db.delete_column('messaging_messagestream', 'outgoing_email')

        # Deleting field 'MessageStream.outgoing_server_name'
        db.delete_column('messaging_messagestream', 'outgoing_server_name')

        # Deleting field 'MessageStream.outgoing_server_type'
        db.delete_column('messaging_messagestream', 'outgoing_server_type')

        # Deleting field 'MessageStream.outgoing_server_username'
        db.delete_column('messaging_messagestream', 'outgoing_server_username')

        # Deleting field 'MessageStream.outgoing_password'
        db.delete_column('messaging_messagestream', 'outgoing_password')

        # Deleting field 'MessageStream.faulty'
        db.delete_column('messaging_messagestream', 'faulty')

        # Deleting field 'MessageStream.last_checked'
        db.delete_column('messaging_messagestream', 'last_checked')

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
            'email_incoming': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'incoming'", 'null': 'True', 'to': "orm['messaging.EmailBox']"}),
            'email_outgoing': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'outgoing'", 'null': 'True', 'to': "orm['messaging.EmailBox']"}),
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
        }
    }

    complete_apps = ['messaging']
