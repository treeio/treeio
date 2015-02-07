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

        # Adding model 'ItemField'
        db.create_table('infrastructure_itemfield', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=256)),
            ('label', self.gf('django.db.models.fields.CharField')
             (max_length=256)),
            ('field_type', self.gf(
                'django.db.models.fields.CharField')(max_length=64)),
            ('required', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
            ('allowed_values', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('infrastructure', ['ItemField'])

        # Adding model 'ItemType'
        db.create_table('infrastructure_itemtype', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=512)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(
                blank=True, related_name='child_set', null=True, to=orm['infrastructure.ItemType'])),
            ('details', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('infrastructure', ['ItemType'])

        # Adding M2M table for field fields on 'ItemType'
        db.create_table('infrastructure_itemtype_fields', (
            ('id', models.AutoField(
                verbose_name='ID', primary_key=True, auto_created=True)),
            ('itemtype', models.ForeignKey(
                orm['infrastructure.itemtype'], null=False)),
            ('itemfield', models.ForeignKey(
                orm['infrastructure.itemfield'], null=False))
        ))
        db.create_unique(
            'infrastructure_itemtype_fields', ['itemtype_id', 'itemfield_id'])

        # Adding model 'ItemStatus'
        db.create_table('infrastructure_itemstatus', (
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
        db.send_create_signal('infrastructure', ['ItemStatus'])

        # Adding model 'Item'
        db.create_table('infrastructure_item', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=512)),
            ('item_type', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['infrastructure.ItemType'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['infrastructure.ItemStatus'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(
                blank=True, related_name='child_set', null=True, to=orm['infrastructure.Item'])),
            ('manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(
                blank=True, related_name='items_manufactured', null=True, to=orm['identities.Contact'])),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(
                blank=True, related_name='items_supplied', null=True, to=orm['identities.Contact'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['core.Location'], null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(
                blank=True, related_name='items_owned', null=True, to=orm['identities.Contact'])),
            ('asset', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['finance.Asset'], null=True, blank=True)),
        ))
        db.send_create_signal('infrastructure', ['Item'])

        # Adding model 'ItemValue'
        db.create_table('infrastructure_itemvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')
             (primary_key=True)),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['infrastructure.ItemField'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['infrastructure.Item'])),
            ('value', self.gf(
                'django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('infrastructure', ['ItemValue'])

        # Adding model 'ItemServicing'
        db.create_table('infrastructure_itemservicing', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=256)),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(
                blank=True, related_name='itemservice_supplied', null=True, to=orm['identities.Contact'])),
            ('start_date', self.gf('django.db.models.fields.DateField')
             (null=True, blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateField')
             (null=True, blank=True)),
            ('details', self.gf(
                'django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('infrastructure', ['ItemServicing'])

        # Adding M2M table for field items on 'ItemServicing'
        db.create_table('infrastructure_itemservicing_items', (
            ('id', models.AutoField(
                verbose_name='ID', primary_key=True, auto_created=True)),
            ('itemservicing', models.ForeignKey(
                orm['infrastructure.itemservicing'], null=False)),
            ('item', models.ForeignKey(orm['infrastructure.item'], null=False))
        ))
        db.create_unique(
            'infrastructure_itemservicing_items', ['itemservicing_id', 'item_id'])

        # Adding M2M table for field billing on 'ItemServicing'
        db.create_table('infrastructure_itemservicing_payments', (
            ('id', models.AutoField(
                verbose_name='ID', primary_key=True, auto_created=True)),
            ('itemservicing', models.ForeignKey(
                orm['infrastructure.itemservicing'], null=False)),
            ('transaction', models.ForeignKey(
                orm['finance.transaction'], null=False))
        ))
        db.create_unique(
            'infrastructure_itemservicing_payments', ['itemservicing_id', 'transaction_id'])

    def backwards(self, orm):

        # Deleting model 'ItemField'
        db.delete_table('infrastructure_itemfield')

        # Deleting model 'ItemType'
        db.delete_table('infrastructure_itemtype')

        # Removing M2M table for field fields on 'ItemType'
        db.delete_table('infrastructure_itemtype_fields')

        # Deleting model 'ItemStatus'
        db.delete_table('infrastructure_itemstatus')

        # Deleting model 'Item'
        db.delete_table('infrastructure_item')

        # Deleting model 'ItemValue'
        db.delete_table('infrastructure_itemvalue')

        # Deleting model 'ItemServicing'
        db.delete_table('infrastructure_itemservicing')

        # Removing M2M table for field items on 'ItemServicing'
        db.delete_table('infrastructure_itemservicing_items')

        # Removing M2M table for field billing on 'ItemServicing'
        db.delete_table('infrastructure_itemservicing_payments')

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
        'finance.account': {
            'Meta': {'ordering': "['name']", 'object_name': 'Account', '_ormbases': ['core.Object']},
            'balance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['identities.Contact']"})
        },
        'finance.asset': {
            'Meta': {'ordering': "['-purchase_date']", 'object_name': 'Asset', '_ormbases': ['core.Object']},
            'asset_type': ('django.db.models.fields.CharField', [], {'default': "'fixed'", 'max_length': '32'}),
            'current_value': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'depreciation_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'depreciation_type': ('django.db.models.fields.CharField', [], {'default': "'straight'", 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'endlife_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'initial_value': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'lifetime': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['identities.Contact']"}),
            'purchase_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'})
        },
        'finance.category': {
            'Meta': {'object_name': 'Category', '_ormbases': ['core.Object']},
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'})
        },
        'finance.liability': {
            'Meta': {'ordering': "['-due_date']", 'object_name': 'Liability', '_ormbases': ['core.Object']},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['finance.Account']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['finance.Category']", 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'finance_liability_source'", 'to': "orm['identities.Contact']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'finance_liability_target'", 'to': "orm['identities.Contact']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'finance.transaction': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'Transaction', '_ormbases': ['core.Object']},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['finance.Account']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['finance.Category']", 'null': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'liability': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['finance.Liability']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'finance_transaction_source'", 'to': "orm['identities.Contact']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'finance_transaction_target'", 'to': "orm['identities.Contact']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
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
        'infrastructure.item': {
            'Meta': {'ordering': "['name']", 'object_name': 'Item', '_ormbases': ['core.Object']},
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['finance.Asset']", 'null': 'True', 'blank': 'True'}),
            'item_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['infrastructure.ItemType']"}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Location']", 'null': 'True', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'items_manufactured'", 'null': 'True', 'to': "orm['identities.Contact']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'items_owned'", 'null': 'True', 'to': "orm['identities.Contact']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['infrastructure.Item']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['infrastructure.ItemStatus']"}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'items_supplied'", 'null': 'True', 'to': "orm['identities.Contact']"})
        },
        'infrastructure.itemfield': {
            'Meta': {'ordering': "['name']", 'object_name': 'ItemField', '_ormbases': ['core.Object']},
            'allowed_values': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'infrastructure.itemservicing': {
            'Meta': {'ordering': "['-expiry_date']", 'object_name': 'ItemServicing', '_ormbases': ['core.Object']},
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['infrastructure.Item']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'payments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['finance.Transaction']", 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'itemservice_supplied'", 'null': 'True', 'to': "orm['identities.Contact']"})
        },
        'infrastructure.itemstatus': {
            'Meta': {'ordering': "('hidden', '-active', 'name')", 'object_name': 'ItemStatus', '_ormbases': ['core.Object']},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'})
        },
        'infrastructure.itemtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ItemType', '_ormbases': ['core.Object']},
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fields': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['infrastructure.ItemField']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['infrastructure.ItemType']"})
        },
        'infrastructure.itemvalue': {
            'Meta': {'object_name': 'ItemValue'},
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['infrastructure.ItemField']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['infrastructure.Item']"}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['infrastructure']
