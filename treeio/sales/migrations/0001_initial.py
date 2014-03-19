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

        # Adding model 'SaleStatus'
        db.create_table('sales_salestatus', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=512)),
            ('use_leads', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
            ('use_opportunities', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
            ('use_sales', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
            ('active', self.gf('django.db.models.fields.BooleanField')
             (default=False)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')
             (default=False)),
            ('details', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('sales', ['SaleStatus'])

        # Adding model 'Product'
        db.create_table('sales_product', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=512)),
            ('product_type', self.gf(
                'django.db.models.fields.CharField')(max_length=32)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(
                blank=True, related_name='child_set', null=True, to=orm['sales.Product'])),
            ('code', self.gf('django.db.models.fields.CharField')
             (max_length=512, null=True, blank=True)),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['identities.Contact'], null=True, blank=True)),
            ('supplier_code', self.gf('django.db.models.fields.IntegerField')
             (null=True, blank=True)),
            ('buy_price', self.gf('django.db.models.fields.FloatField')
             (null=True, blank=True)),
            ('sell_price', self.gf('django.db.models.fields.FloatField')
             (null=True, blank=True)),
            ('stock_quantity', self.gf('django.db.models.fields.IntegerField')
             (null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')
             (default=False)),
            ('runout_action', self.gf('django.db.models.fields.CharField')
             (max_length=32, null=True, blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('sales', ['Product'])

        # Adding model 'SaleSource'
        db.create_table('sales_salesource', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (max_length=512)),
            ('active', self.gf('django.db.models.fields.BooleanField')
             (default=False)),
            ('details', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('sales', ['SaleSource'])

        # Adding model 'Lead'
        db.create_table('sales_lead', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['identities.Contact'])),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['sales.SaleSource'], null=True, blank=True)),
            ('contact_method', self.gf(
                'django.db.models.fields.CharField')(max_length=32)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['sales.SaleStatus'])),
            ('details', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('sales', ['Lead'])

        # Adding M2M table for field products_interested on 'Lead'
        db.create_table('sales_lead_products_interested', (
            ('id', models.AutoField(
                verbose_name='ID', primary_key=True, auto_created=True)),
            ('lead', models.ForeignKey(orm['sales.lead'], null=False)),
            ('product', models.ForeignKey(orm['sales.product'], null=False))
        ))
        db.create_unique(
            'sales_lead_products_interested', ['lead_id', 'product_id'])

        # Adding M2M table for field assigned on 'Lead'
        db.create_table('sales_lead_assigned', (
            ('id', models.AutoField(
                verbose_name='ID', primary_key=True, auto_created=True)),
            ('lead', models.ForeignKey(orm['sales.lead'], null=False)),
            ('user', models.ForeignKey(orm['core.user'], null=False))
        ))
        db.create_unique('sales_lead_assigned', ['lead_id', 'user_id'])

        # Adding model 'Opportunity'
        db.create_table('sales_opportunity', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('lead', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['sales.Lead'], null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['identities.Contact'])),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['sales.SaleSource'], null=True, blank=True)),
            ('expected_date', self.gf('django.db.models.fields.DateField')
             (null=True, blank=True)),
            ('closed_date', self.gf('django.db.models.fields.DateField')
             (null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['sales.SaleStatus'])),
            ('probability', self.gf('django.db.models.fields.FloatField')
             (null=True, blank=True)),
            ('amount', self.gf(
                'django.db.models.fields.FloatField')(default=0)),
            ('details', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('sales', ['Opportunity'])

        # Adding M2M table for field products_interested on 'Opportunity'
        db.create_table('sales_opportunity_products_interested', (
            ('id', models.AutoField(
                verbose_name='ID', primary_key=True, auto_created=True)),
            ('opportunity', models.ForeignKey(
                orm['sales.opportunity'], null=False)),
            ('product', models.ForeignKey(orm['sales.product'], null=False))
        ))
        db.create_unique(
            'sales_opportunity_products_interested', ['opportunity_id', 'product_id'])

        # Adding M2M table for field assigned on 'Opportunity'
        db.create_table('sales_opportunity_assigned', (
            ('id', models.AutoField(
                verbose_name='ID', primary_key=True, auto_created=True)),
            ('opportunity', models.ForeignKey(
                orm['sales.opportunity'], null=False)),
            ('user', models.ForeignKey(orm['core.user'], null=False))
        ))
        db.create_unique(
            'sales_opportunity_assigned', ['opportunity_id', 'user_id'])

        # Adding model 'SaleOrder'
        db.create_table('sales_saleorder', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('reference', self.gf('django.db.models.fields.CharField')
             (max_length=512, null=True, blank=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')
             (default=datetime.datetime.now)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['identities.Contact'], null=True, blank=True)),
            ('opportunity', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['sales.Opportunity'], null=True, blank=True)),
            ('payment', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['finance.Transaction'], null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['sales.SaleSource'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['sales.SaleStatus'])),
            ('details', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('sales', ['SaleOrder'])

        # Adding M2M table for field assigned on 'SaleOrder'
        db.create_table('sales_saleorder_assigned', (
            ('id', models.AutoField(
                verbose_name='ID', primary_key=True, auto_created=True)),
            ('saleorder', models.ForeignKey(
                orm['sales.saleorder'], null=False)),
            ('user', models.ForeignKey(orm['core.user'], null=False))
        ))
        db.create_unique(
            'sales_saleorder_assigned', ['saleorder_id', 'user_id'])

        # Adding model 'Subscription'
        db.create_table('sales_subscription', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['identities.Contact'], null=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['sales.Product'], null=True, blank=True)),
            ('start', self.gf('django.db.models.fields.DateField')
             (default=datetime.datetime.now)),
            ('expiry', self.gf('django.db.models.fields.DateField')
             (null=True, blank=True)),
            ('cycle_period', self.gf('django.db.models.fields.CharField')
             (default='month', max_length=32)),
            ('cycle_end', self.gf('django.db.models.fields.DateField')
             (null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')
             (default=False)),
            ('details', self.gf('django.db.models.fields.CharField')
             (max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal('sales', ['Subscription'])

        # Adding model 'OrderedProduct'
        db.create_table('sales_orderedproduct', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('subscription', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['sales.Subscription'], null=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['sales.Product'])),
            ('quantity', self.gf(
                'django.db.models.fields.PositiveIntegerField')(default=1)),
            ('discount', self.gf('django.db.models.fields.FloatField')
             (null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['sales.SaleOrder'])),
            ('fulfilled', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('sales', ['OrderedProduct'])

        # Adding model 'UpdateRecord'
        db.create_table('sales_updaterecord', (
            ('object_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['core.Object'], unique=True, primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['sales.SaleOrder'], null=True, blank=True)),
            ('opportunity', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['sales.Opportunity'], null=True, blank=True)),
            ('lead', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['sales.Lead'], null=True, blank=True)),
            ('record_type', self.gf(
                'django.db.models.fields.CharField')(max_length=32)),
            ('details', self.gf('django.db.models.fields.TextField')
             (null=True, blank=True)),
        ))
        db.send_create_signal('sales', ['UpdateRecord'])

    def backwards(self, orm):

        # Deleting model 'SaleStatus'
        db.delete_table('sales_salestatus')

        # Deleting model 'Product'
        db.delete_table('sales_product')

        # Deleting model 'SaleSource'
        db.delete_table('sales_salesource')

        # Deleting model 'Lead'
        db.delete_table('sales_lead')

        # Removing M2M table for field products_interested on 'Lead'
        db.delete_table('sales_lead_products_interested')

        # Removing M2M table for field assigned on 'Lead'
        db.delete_table('sales_lead_assigned')

        # Deleting model 'Opportunity'
        db.delete_table('sales_opportunity')

        # Removing M2M table for field products_interested on 'Opportunity'
        db.delete_table('sales_opportunity_products_interested')

        # Removing M2M table for field assigned on 'Opportunity'
        db.delete_table('sales_opportunity_assigned')

        # Deleting model 'SaleOrder'
        db.delete_table('sales_saleorder')

        # Removing M2M table for field assigned on 'SaleOrder'
        db.delete_table('sales_saleorder_assigned')

        # Deleting model 'Subscription'
        db.delete_table('sales_subscription')

        # Deleting model 'OrderedProduct'
        db.delete_table('sales_orderedproduct')

        # Deleting model 'UpdateRecord'
        db.delete_table('sales_updaterecord')

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
        'sales.lead': {
            'Meta': {'ordering': "['contact']", 'object_name': 'Lead', '_ormbases': ['core.Object']},
            'assigned': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'sales_lead_assigned'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.User']"}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['identities.Contact']"}),
            'contact_method': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'products_interested': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sales.Product']", 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.SaleSource']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.SaleStatus']"})
        },
        'sales.opportunity': {
            'Meta': {'ordering': "['-expected_date']", 'object_name': 'Opportunity', '_ormbases': ['core.Object']},
            'amount': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'assigned': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'sales_opportunity_assigned'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.User']"}),
            'closed_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['identities.Contact']"}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expected_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'lead': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.Lead']", 'null': 'True', 'blank': 'True'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'probability': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'products_interested': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sales.Product']", 'symmetrical': 'False'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.SaleSource']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.SaleStatus']"})
        },
        'sales.orderedproduct': {
            'Meta': {'ordering': "['product']", 'object_name': 'OrderedProduct', '_ormbases': ['core.Object']},
            'discount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fulfilled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.SaleOrder']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.Product']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.Subscription']", 'null': 'True', 'blank': 'True'})
        },
        'sales.product': {
            'Meta': {'ordering': "['code']", 'object_name': 'Product', '_ormbases': ['core.Object']},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'buy_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['sales.Product']"}),
            'product_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'runout_action': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'sell_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'stock_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['identities.Contact']", 'null': 'True', 'blank': 'True'}),
            'supplier_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'sales.saleorder': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'SaleOrder', '_ormbases': ['core.Object']},
            'assigned': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'sales_saleorder_assigned'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.User']"}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['identities.Contact']", 'null': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'opportunity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.Opportunity']", 'null': 'True', 'blank': 'True'}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['finance.Transaction']", 'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.SaleSource']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.SaleStatus']"})
        },
        'sales.salesource': {
            'Meta': {'ordering': "('-active', 'name')", 'object_name': 'SaleSource', '_ormbases': ['core.Object']},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'})
        },
        'sales.salestatus': {
            'Meta': {'ordering': "('hidden', '-active', 'name')", 'object_name': 'SaleStatus', '_ormbases': ['core.Object']},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'use_leads': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_opportunities': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_sales': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'sales.subscription': {
            'Meta': {'ordering': "['expiry']", 'object_name': 'Subscription', '_ormbases': ['core.Object']},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['identities.Contact']", 'null': 'True', 'blank': 'True'}),
            'cycle_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cycle_period': ('django.db.models.fields.CharField', [], {'default': "'month'", 'max_length': '32'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'expiry': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.Product']", 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'})
        },
        'sales.updaterecord': {
            'Meta': {'ordering': "['order']", 'object_name': 'UpdateRecord', '_ormbases': ['core.Object']},
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'lead': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.Lead']", 'null': 'True', 'blank': 'True'}),
            'object_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Object']", 'unique': 'True', 'primary_key': 'True'}),
            'opportunity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.Opportunity']", 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.SaleOrder']", 'null': 'True', 'blank': 'True'}),
            'record_type': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['sales']
