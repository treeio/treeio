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

        # Adding model 'Category'
        db.create_table('finance_category', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=512)),
            ('details', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('finance', ['Category'])

        # Adding model 'Asset'
        db.create_table('finance_asset', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=512)),
            ('asset_type', self.gf('django.db.models.fields.CharField')
             (default='fixed', max_length=32)),
            ('initial_value', self.gf(
                'django.db.models.fields.FloatField')(default=0)),
            ('lifetime', self.gf('django.db.models.fields.FloatField')
             (null=True, blank=True)),
            ('endlife_value', self.gf('django.db.models.fields.FloatField')
             (null=True, blank=True)),
            ('depreciation_rate', self.gf(
                'django.db.models.fields.FloatField')(null=True, blank=True)),
            ('depreciation_type', self.gf('django.db.models.fields.CharField')
             (default='straight', max_length=32, null=True, blank=True)),
            ('purchase_date', self.gf('django.db.models.fields.DateField')
             (default=datetime.datetime.now, null=True, blank=True)),
            ('current_value', self.gf(
                'django.db.models.fields.FloatField')(default=0)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['identities.Contact'])),
            ('details', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('finance', ['Asset'])

        # Adding model 'Account'
        db.create_table('finance_account', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=512)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['identities.Contact'])),
            ('balance', self.gf(
                'django.db.models.fields.FloatField')(default=0)),
            ('details', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('finance', ['Account'])

        # Adding model 'Equity'
        db.create_table('finance_equity', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('equity_type', self.gf('django.db.models.fields.CharField')
             (default='share', max_length=32)),
            ('issue_price', self.gf('django.db.models.fields.FloatField')()),
            ('sell_price', self.gf('django.db.models.fields.FloatField')()),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='finance_equity_issued', to=orm['identities.Contact'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='finance_equity_owned', to=orm['identities.Contact'])),
            ('amount', self.gf(
                'django.db.models.fields.PositiveIntegerField')(default=1)),
            ('purchase_date', self.gf('django.db.models.fields.DateField')
             (default=datetime.datetime.now)),
            ('details', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('finance', ['Equity'])

        # Adding model 'Liability'
        db.create_table('finance_liability', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=512)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='finance_liability_source', to=orm['identities.Contact'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='finance_liability_target', to=orm['identities.Contact'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['finance.Category'], null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['finance.Account'])),
            ('due_date', self.gf('django.db.models.fields.DateField')
             (null=True, blank=True)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('details', self.gf(
                'django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('finance', ['Liability'])

        # Adding model 'Transaction'
        db.create_table('finance_transaction', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=512)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='finance_transaction_source', to=orm['identities.Contact'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='finance_transaction_target', to=orm['identities.Contact'])),
            ('liability', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['finance.Liability'], null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['finance.Category'], null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['finance.Account'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')
             (default=datetime.datetime.now)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('details', self.gf(
                'django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('finance', ['Transaction'])

    def backwards(self, orm):

        # Deleting model 'Category'
        db.delete_table('finance_category')

        # Deleting model 'Asset'
        db.delete_table('finance_asset')

        # Deleting model 'Account'
        db.delete_table('finance_account')

        # Deleting model 'Equity'
        db.delete_table('finance_equity')

        # Deleting model 'Liability'
        db.delete_table('finance_liability')

        # Deleting model 'Transaction'
        db.delete_table('finance_transaction')

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
        'finance.equity': {
            'Meta': {'ordering': "['-purchase_date']", 'object_name': 'Equity', '_ormbases': ['core.Object']},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'equity_type': ('django.db.models.fields.CharField', [], {'default': "'share'", 'max_length': '32'}),
            'issue_price': ('django.db.models.fields.FloatField', [], {}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'finance_equity_issued'", 'to': "orm['identities.Contact']"}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'finance_equity_owned'", 'to': "orm['identities.Contact']"}),
            'purchase_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'sell_price': ('django.db.models.fields.FloatField', [], {})
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
        }
    }

    complete_apps = ['finance']
