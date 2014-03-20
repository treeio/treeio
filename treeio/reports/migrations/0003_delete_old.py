# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):

    def forwards(self, orm):
        "Removes all old reports (these need to be re-created manually)"
        for report in orm['reports.Report'].objects.all():
            report.delete()

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

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
            'Meta': {'ordering': "['name']", 'object_name': 'Group'},
            'accessentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.AccessEntity']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'Meta': {'ordering': "['name']", 'object_name': 'User'},
            'accessentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.AccessEntity']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'default_group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'default_user_set'", 'null': 'True', 'to': "orm['core.AccessEntity']"}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_access': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'other_groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Group']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'reports.chart': {
            'Meta': {'object_name': 'Chart', '_ormbases': ['core.Object']},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'options': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reports.Report']"})
        },
        'reports.report': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'Report', '_ormbases': ['core.Object']},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'model': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['reports']
