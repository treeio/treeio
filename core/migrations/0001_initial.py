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

        # Adding model 'Group'
        db.create_table('core_group', (
            ('id', self.gf('django.db.models.fields.AutoField')
             (primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=256)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(
                blank=True, related_name='child_set', null=True, to=orm['core.Group'])),
            ('details', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')
             (auto_now=True, blank=True)),
        ))
        db.send_create_signal('core', ['Group'])

        # Adding model 'User'
        db.create_table('core_user', (
            ('id', self.gf('django.db.models.fields.AutoField')
             (primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=256)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['auth.User'])),
            ('default_group', self.gf('django.db.models.fields.related.ForeignKey')(
                blank=True, related_name='default_user_set', null=True, to=orm['core.Group'])),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')
             (auto_now=True, blank=True)),
        ))
        db.send_create_signal('core', ['User'])

        # Adding M2M table for field other_groups on 'User'
        db.create_table('core_user_other_groups', (
            ('id', models.AutoField(
                verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm['core.user'], null=False)),
            ('group', models.ForeignKey(orm['core.group'], null=False))
        ))
        db.create_unique('core_user_other_groups', ['user_id', 'group_id'])

        # Adding model 'Object'
        db.create_table('core_object', (
            ('id', self.gf('django.db.models.fields.AutoField')
             (primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['core.User'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['core.Group'])),
            ('object_name', self.gf('django.db.models.fields.CharField')
             (max_length=512, null=True, blank=True)),
            ('object_type', self.gf('django.db.models.fields.CharField')
             (max_length=512, null=True, blank=True)),
            ('trash', self.gf('django.db.models.fields.BooleanField')
             (default=False)),
            ('user_read', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
            ('user_write', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
            ('user_execute', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
            ('group_read', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
            ('group_write', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
            ('group_execute', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
            ('everybody_read', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
            ('everybody_write', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
            ('everybody_execute', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')
             (auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')
             (default=datetime.datetime.now)),
            ('nuvius_resource', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Object'])

        # Adding M2M table for field links on 'Object'
        db.create_table('core_object_links', (
            ('id', models.AutoField(
                verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_object', models.ForeignKey(orm['core.object'], null=False)),
            ('to_object', models.ForeignKey(orm['core.object'], null=False))
        ))
        db.create_unique(
            'core_object_links', ['from_object_id', 'to_object_id'])

        # Adding M2M table for field subscribers on 'Object'
        db.create_table('core_object_subscribers', (
            ('id', models.AutoField(
                verbose_name='ID', primary_key=True, auto_created=True)),
            ('object', models.ForeignKey(orm['core.object'], null=False)),
            ('user', models.ForeignKey(orm['core.user'], null=False))
        ))
        db.create_unique('core_object_subscribers', ['object_id', 'user_id'])

        # Adding model 'Module'
        db.create_table('core_module', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=256)),
            ('title', self.gf('django.db.models.fields.CharField')
             (max_length=256)),
            ('details', self.gf(
                'django.db.models.fields.TextField')(blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')
             (max_length=512)),
            ('display', self.gf(
                'django.db.models.fields.BooleanField')(default=True)),
            ('system', self.gf('django.db.models.fields.BooleanField')
             (default=True)),
        ))
        db.send_create_signal('core', ['Module'])

        # Adding model 'Perspective'
        db.create_table('core_perspective', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=256)),
            ('details', self.gf(
                'django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('core', ['Perspective'])

        # Adding M2M table for field modules on 'Perspective'
        db.create_table('core_perspective_modules', (
            ('id', models.AutoField(
                verbose_name='ID', primary_key=True, auto_created=True)),
            ('perspective', models.ForeignKey(
                orm['core.perspective'], null=False)),
            ('module', models.ForeignKey(orm['core.module'], null=False))
        ))
        db.create_unique(
            'core_perspective_modules', ['perspective_id', 'module_id'])

        # Adding model 'ModuleSetting'
        db.create_table('core_modulesetting', (
            ('id', self.gf('django.db.models.fields.AutoField')
             (primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=512)),
            ('label', self.gf('django.db.models.fields.CharField')
             (max_length=512)),
            ('perspective', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['core.Perspective'], null=True, blank=True)),
            ('module', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['core.Module'], null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['core.User'], null=True, blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['core.Group'], null=True, blank=True)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('core', ['ModuleSetting'])

        # Adding model 'Location'
        db.create_table('core_location', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=512)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(
                blank=True, related_name='child_set', null=True, to=orm['core.Location'])),
        ))
        db.send_create_signal('core', ['Location'])

        # Adding model 'PageFolder'
        db.create_table('core_pagefolder', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=256)),
            ('details', self.gf(
                'django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('core', ['PageFolder'])

        # Adding model 'Page'
        db.create_table('core_page', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=256)),
            ('title', self.gf('django.db.models.fields.CharField')
             (max_length=256)),
            ('folder', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['core.PageFolder'])),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('published', self.gf(
                'django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('core', ['Page'])

        # Adding model 'Notification'
        db.create_table('core_notification', (
            ('id', self.gf('django.db.models.fields.AutoField')
             (primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['core.User'])),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(
                blank=True, related_name='notification_sent_set', null=True, to=orm['core.User'])),
            ('type', self.gf('django.db.models.fields.CharField')
             (max_length=32)),
            ('object', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['core.Object'], null=True, blank=True)),
            ('object_type', self.gf('django.db.models.fields.CharField')
             (max_length=512, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')
             (max_length=512, null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
            ('format_message', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
            ('format_strings', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')
             (auto_now=True, blank=True)),
        ))
        db.send_create_signal('core', ['Notification'])

        # Adding model 'Widget'
        db.create_table('core_widget', (
            ('id', self.gf('django.db.models.fields.AutoField')
             (primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['core.User'])),
            ('perspective', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['core.Perspective'])),
            ('module_name', self.gf(
                'django.db.models.fields.CharField')(max_length=256)),
            ('widget_name', self.gf(
                'django.db.models.fields.CharField')(max_length=256)),
            ('weight', self.gf(
                'django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('core', ['Widget'])

    def backwards(self, orm):

        # Deleting model 'Group'
        db.delete_table('core_group')

        # Deleting model 'User'
        db.delete_table('core_user')

        # Removing M2M table for field other_groups on 'User'
        db.delete_table('core_user_other_groups')

        # Deleting model 'Object'
        db.delete_table('core_object')

        # Removing M2M table for field links on 'Object'
        db.delete_table('core_object_links')

        # Removing M2M table for field subscribers on 'Object'
        db.delete_table('core_object_subscribers')

        # Deleting model 'Module'
        db.delete_table('core_module')

        # Deleting model 'Perspective'
        db.delete_table('core_perspective')

        # Removing M2M table for field modules on 'Perspective'
        db.delete_table('core_perspective_modules')

        # Deleting model 'ModuleSetting'
        db.delete_table('core_modulesetting')

        # Deleting model 'Location'
        db.delete_table('core_location')

        # Deleting model 'PageFolder'
        db.delete_table('core_pagefolder')

        # Deleting model 'Page'
        db.delete_table('core_page')

        # Deleting model 'Notification'
        db.delete_table('core_notification')

        # Deleting model 'Widget'
        db.delete_table('core_widget')

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
        'core.location': {
            'Meta': {'object_name': 'Location', '_ormbases': ['core.Object']},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['core.Location']"})
        },
        'core.module': {
            'Meta': {'ordering': "['name']", 'object_name': 'Module', '_ormbases': ['core.Object']},
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'system': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'core.modulesetting': {
            'Meta': {'object_name': 'ModuleSetting'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Group']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Module']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'perspective': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Perspective']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.User']", 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'core.notification': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'Notification'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'format_message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'format_strings': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Object']", 'null': 'True', 'blank': 'True'}),
            'object_type': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'notification_sent_set'", 'null': 'True', 'to': "orm['core.User']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.User']"})
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
        'core.page': {
            'Meta': {'ordering': "['name']", 'object_name': 'Page', '_ormbases': ['core.Object']},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.PageFolder']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'core.pagefolder': {
            'Meta': {'object_name': 'PageFolder', '_ormbases': ['core.Object']},
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'})
        },
        'core.perspective': {
            'Meta': {'object_name': 'Perspective', '_ormbases': ['core.Object']},
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modules': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Module']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'})
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
        'core.widget': {
            'Meta': {'ordering': "['weight']", 'object_name': 'Widget'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'perspective': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Perspective']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.User']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'widget_name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['core']
