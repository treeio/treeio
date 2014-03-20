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

        # Adding model 'Project'
        db.create_table('projects_project', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=255)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(
                blank=True, related_name='child_set', null=True, to=orm['projects.Project'])),
            ('manager', self.gf('django.db.models.fields.related.ForeignKey')(
                blank=True, related_name='manager', null=True, to=orm['identities.Contact'])),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(
                blank=True, related_name='client', null=True, to=orm['identities.Contact'])),
            ('details', self.gf('django.db.models.fields.TextField')
             (max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('projects', ['Project'])

        # Adding model 'TaskStatus'
        db.create_table('projects_taskstatus', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=255)),
            ('details', self.gf('django.db.models.fields.TextField')
             (max_length=255, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')
             (default=False)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')
             (default=False)),
        ))
        db.send_create_signal('projects', ['TaskStatus'])

        # Adding model 'Milestone'
        db.create_table('projects_milestone', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['projects.Project'])),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=255)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['projects.TaskStatus'])),
            ('details', self.gf('django.db.models.fields.TextField')
             (max_length=255, null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')
             (null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('projects', ['Milestone'])

        # Adding model 'Task'
        db.create_table('projects_task', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(
                blank=True, related_name='child_set', null=True, to=orm['projects.Task'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['projects.Project'])),
            ('milestone', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['projects.Milestone'], null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['projects.TaskStatus'])),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=255)),
            ('details', self.gf('django.db.models.fields.TextField')
             (max_length=255, null=True, blank=True)),
            ('caller', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['identities.Contact'], null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')
             (null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')
             (null=True, blank=True)),
            ('priority', self.gf(
                'django.db.models.fields.IntegerField')(default=3)),
            ('estimated_time', self.gf('django.db.models.fields.IntegerField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('projects', ['Task'])

        # Adding M2M table for field assigned on 'Task'
        db.create_table('projects_task_assigned', (
            ('id', models.AutoField(
                verbose_name='ID', primary_key=True, auto_created=True)),
            ('task', models.ForeignKey(orm['projects.task'], null=False)),
            ('user', models.ForeignKey(orm['core.user'], null=False))
        ))
        db.create_unique('projects_task_assigned', ['task_id', 'user_id'])

        # Adding model 'TaskTimeSlot'
        db.create_table('projects_tasktimeslot', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['projects.Task'])),
            ('time_from', self.gf('django.db.models.fields.DateTimeField')()),
            ('time_to', self.gf('django.db.models.fields.DateTimeField')
             (null=True, blank=True)),
            ('timezone', self.gf(
                'django.db.models.fields.IntegerField')(default=0)),
            ('details', self.gf('django.db.models.fields.TextField')
             (max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('projects', ['TaskTimeSlot'])

        # Adding model 'TaskRecord'
        db.create_table('projects_taskrecord', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['projects.Task'])),
            ('record_type', self.gf(
                'django.db.models.fields.CharField')(max_length=256)),
            ('details', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('projects', ['TaskRecord'])

    def backwards(self, orm):

        # Deleting model 'Project'
        db.delete_table('projects_project')

        # Deleting model 'TaskStatus'
        db.delete_table('projects_taskstatus')

        # Deleting model 'Milestone'
        db.delete_table('projects_milestone')

        # Deleting model 'Task'
        db.delete_table('projects_task')

        # Removing M2M table for field assigned on 'Task'
        db.delete_table('projects_task_assigned')

        # Deleting model 'TaskTimeSlot'
        db.delete_table('projects_tasktimeslot')

        # Deleting model 'TaskRecord'
        db.delete_table('projects_taskrecord')

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
        'projects.milestone': {
            'Meta': {'ordering': "['name']", 'object_name': 'Milestone', '_ormbases': ['core.Object']},
            'details': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Project']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.TaskStatus']"})
        },
        'projects.project': {
            'Meta': {'ordering': "['name']", 'object_name': 'Project', '_ormbases': ['core.Object']},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'client'", 'null': 'True', 'to': "orm['identities.Contact']"}),
            'details': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'manager'", 'null': 'True', 'to': "orm['identities.Contact']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['projects.Project']"})
        },
        'projects.task': {
            'Meta': {'ordering': "('-priority', 'name')", 'object_name': 'Task', '_ormbases': ['core.Object']},
            'assigned': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.User']", 'null': 'True', 'blank': 'True'}),
            'caller': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['identities.Contact']", 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'estimated_time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'milestone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Milestone']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['projects.Task']"}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Project']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.TaskStatus']"})
        },
        'projects.taskrecord': {
            'Meta': {'object_name': 'TaskRecord', '_ormbases': ['core.Object']},
            'details': ('django.db.models.fields.TextField', [], {}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'record_type': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Task']"})
        },
        'projects.taskstatus': {
            'Meta': {'ordering': "('hidden', '-active', 'name')", 'object_name': 'TaskStatus', '_ormbases': ['core.Object']},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'details': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'})
        },
        'projects.tasktimeslot': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'TaskTimeSlot', '_ormbases': ['core.Object']},
            'details': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Task']"}),
            'time_from': ('django.db.models.fields.DateTimeField', [], {}),
            'time_to': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['projects']
