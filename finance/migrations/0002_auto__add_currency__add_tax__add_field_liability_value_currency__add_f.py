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

        # Adding model 'Currency'
        db.create_table('finance_currency', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')
             (max_length=3)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=255)),
            ('symbol', self.gf('django.db.models.fields.CharField')
             (max_length=1, null=True, blank=True)),
            ('factor', self.gf('django.db.models.fields.DecimalField')
             (default=1, max_digits=10, decimal_places=4)),
            ('is_active', self.gf(
                'django.db.models.fields.BooleanField')(default=True)),
            ('is_default', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('finance', ['Currency'])

        # Adding model 'Tax'
        db.create_table('finance_tax', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=512)),
            ('rate', self.gf('django.db.models.fields.DecimalField')
             (max_digits=4, decimal_places=2)),
            ('compound', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('finance', ['Tax'])

        # Adding field 'Liability.value_currency'
        db.add_column('finance_liability', 'value_currency', self.gf(
            'django.db.models.fields.related.ForeignKey')(default=1, to=orm['finance.Currency']), keep_default=False)

        # Adding field 'Liability.value_display'
        db.add_column('finance_liability', 'value_display', self.gf('django.db.models.fields.DecimalField')(
            default=0, max_digits=20, decimal_places=2), keep_default=False)

        # Changing field 'Liability.value'
        db.alter_column('finance_liability', 'value', self.gf(
            'django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2))

        # Changing field 'Asset.initial_value'
        db.alter_column('finance_asset', 'initial_value', self.gf(
            'django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2))

        # Changing field 'Asset.current_value'
        db.alter_column('finance_asset', 'current_value', self.gf(
            'django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2))

        # Changing field 'Asset.endlife_value'
        db.alter_column('finance_asset', 'endlife_value', self.gf(
            'django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=2))

        # Changing field 'Asset.lifetime'
        db.alter_column('finance_asset', 'lifetime', self.gf(
            'django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=0))

        # Changing field 'Asset.depreciation_rate'
        db.alter_column('finance_asset', 'depreciation_rate', self.gf(
            'django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2))

        # Adding field 'Account.balance_currency'
        db.add_column('finance_account', 'balance_currency', self.gf(
            'django.db.models.fields.related.ForeignKey')(default=1, to=orm['finance.Currency']), keep_default=False)

        # Adding field 'Account.balance_display'
        db.add_column('finance_account', 'balance_display', self.gf('django.db.models.fields.DecimalField')(
            default=0, max_digits=20, decimal_places=2), keep_default=False)

        # Changing field 'Account.balance'
        db.alter_column('finance_account', 'balance', self.gf(
            'django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2))

        # Adding field 'Transaction.value_currency'
        db.add_column('finance_transaction', 'value_currency', self.gf(
            'django.db.models.fields.related.ForeignKey')(default=1, to=orm['finance.Currency']), keep_default=False)

        # Adding field 'Transaction.value_display'
        db.add_column('finance_transaction', 'value_display', self.gf('django.db.models.fields.DecimalField')(
            default=0, max_digits=20, decimal_places=2), keep_default=False)

        # Changing field 'Transaction.value'
        db.alter_column('finance_transaction', 'value', self.gf(
            'django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2))

        # Changing field 'Equity.issue_price'
        db.alter_column('finance_equity', 'issue_price', self.gf(
            'django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2))

        # Changing field 'Equity.sell_price'
        db.alter_column('finance_equity', 'sell_price', self.gf(
            'django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2))

    def backwards(self, orm):

        # Deleting model 'Currency'
        db.delete_table('finance_currency')

        # Deleting model 'Tax'
        db.delete_table('finance_tax')

        # Deleting field 'Liability.value_currency'
        db.delete_column('finance_liability', 'value_currency_id')

        # Deleting field 'Liability.value_display'
        db.delete_column('finance_liability', 'value_display')

        # Changing field 'Liability.value'
        db.alter_column('finance_liability', 'value', self.gf(
            'django.db.models.fields.FloatField')())

        # Changing field 'Asset.initial_value'
        db.alter_column('finance_asset', 'initial_value', self.gf(
            'django.db.models.fields.FloatField')())

        # Changing field 'Asset.current_value'
        db.alter_column('finance_asset', 'current_value', self.gf(
            'django.db.models.fields.FloatField')())

        # Changing field 'Asset.endlife_value'
        db.alter_column('finance_asset', 'endlife_value', self.gf(
            'django.db.models.fields.FloatField')(null=True))

        # Changing field 'Asset.lifetime'
        db.alter_column('finance_asset', 'lifetime', self.gf(
            'django.db.models.fields.FloatField')(null=True))

        # Changing field 'Asset.depreciation_rate'
        db.alter_column('finance_asset', 'depreciation_rate', self.gf(
            'django.db.models.fields.FloatField')(null=True))

        # Deleting field 'Account.balance_currency'
        db.delete_column('finance_account', 'balance_currency_id')

        # Deleting field 'Account.balance_display'
        db.delete_column('finance_account', 'balance_display')

        # Changing field 'Account.balance'
        db.alter_column('finance_account', 'balance', self.gf(
            'django.db.models.fields.FloatField')())

        # Deleting field 'Transaction.value_currency'
        db.delete_column('finance_transaction', 'value_currency_id')

        # Deleting field 'Transaction.value_display'
        db.delete_column('finance_transaction', 'value_display')

        # Changing field 'Transaction.value'
        db.alter_column('finance_transaction', 'value', self.gf(
            'django.db.models.fields.FloatField')())

        # Changing field 'Equity.issue_price'
        db.alter_column('finance_equity', 'issue_price', self.gf(
            'django.db.models.fields.FloatField')())

        # Changing field 'Equity.sell_price'
        db.alter_column('finance_equity', 'sell_price', self.gf(
            'django.db.models.fields.FloatField')())

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
            'trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.User']", 'null': 'True', 'blank': 'True'})
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
        'finance.account': {
            'Meta': {'ordering': "['name']", 'object_name': 'Account', '_ormbases': ['core.Object']},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '2'}),
            'balance_currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['finance.Currency']"}),
            'balance_display': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '2'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['identities.Contact']"})
        },
        'finance.asset': {
            'Meta': {'ordering': "['-purchase_date']", 'object_name': 'Asset', '_ormbases': ['core.Object']},
            'asset_type': ('django.db.models.fields.CharField', [], {'default': "'fixed'", 'max_length': '32'}),
            'current_value': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '2'}),
            'depreciation_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'depreciation_type': ('django.db.models.fields.CharField', [], {'default': "'straight'", 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'endlife_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '2', 'blank': 'True'}),
            'initial_value': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '2'}),
            'lifetime': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '0', 'blank': 'True'}),
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
        'finance.currency': {
            'Meta': {'object_name': 'Currency', '_ormbases': ['core.Object']},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'factor': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '10', 'decimal_places': '4'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'})
        },
        'finance.equity': {
            'Meta': {'ordering': "['-purchase_date']", 'object_name': 'Equity', '_ormbases': ['core.Object']},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'equity_type': ('django.db.models.fields.CharField', [], {'default': "'share'", 'max_length': '32'}),
            'issue_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'finance_equity_issued'", 'to': "orm['identities.Contact']"}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'finance_equity_owned'", 'to': "orm['identities.Contact']"}),
            'purchase_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'sell_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'})
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
            'value': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '2'}),
            'value_currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['finance.Currency']"}),
            'value_display': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '2'})
        },
        'finance.tax': {
            'Meta': {'object_name': 'Tax', '_ormbases': ['core.Object']},
            'compound': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'})
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
            'value': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '2'}),
            'value_currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['finance.Currency']"}),
            'value_display': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '2'})
        },
        'identities.contact': {
            'Meta': {'ordering': "['name']", 'object_name': 'Contact', '_ormbases': ['core.Object']},
            'contact_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['identities.ContactType']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['identities.Contact']"}),
            'related_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Group']", 'null': 'True', 'blank': 'True'}),
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
        }
    }

    complete_apps = ['finance']
