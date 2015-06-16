# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('identities', '0001_initial'),
        ('finance', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('contact_method', models.CharField(max_length=32, choices=[(b'email', b'E-Mail'), (b'phone', b'Phone'), (b'post', b'Post'), (b'face', b'Face to Face')])),
                ('details', models.TextField(null=True, blank=True)),
                ('assigned', models.ManyToManyField(related_name='sales_lead_assigned', null=True, to='core.User', blank=True)),
                ('contact', models.ForeignKey(to='identities.Contact')),
            ],
            options={
                'ordering': ['contact'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Opportunity',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('expected_date', models.DateField(null=True, blank=True)),
                ('closed_date', models.DateField(null=True, blank=True)),
                ('probability', models.DecimalField(null=True, max_digits=3, decimal_places=0, blank=True)),
                ('amount', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('amount_display', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('details', models.TextField(null=True, blank=True)),
                ('amount_currency', models.ForeignKey(to='finance.Currency')),
                ('assigned', models.ManyToManyField(related_name='sales_opportunity_assigned', null=True, to='core.User', blank=True)),
                ('contact', models.ForeignKey(to='identities.Contact')),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='sales.Lead', null=True)),
            ],
            options={
                'ordering': ['-expected_date'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='OrderedProduct',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('quantity', models.DecimalField(default=1, max_digits=30, decimal_places=2)),
                ('discount', models.DecimalField(default=0, max_digits=5, decimal_places=2)),
                ('rate', models.DecimalField(max_digits=20, decimal_places=2)),
                ('rate_display', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('description', models.TextField(null=True, blank=True)),
                ('fulfilled', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['product'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=512)),
                ('product_type', models.CharField(default=b'good', max_length=32, choices=[(b'service', b'Service'), (b'good', b'Good'), (b'subscription', b'Subscription'), (b'compound', b'Compound')])),
                ('code', models.CharField(max_length=512, null=True, blank=True)),
                ('supplier_code', models.IntegerField(null=True, blank=True)),
                ('buy_price', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('sell_price', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('stock_quantity', models.IntegerField(null=True, blank=True)),
                ('active', models.BooleanField(default=False)),
                ('runout_action', models.CharField(blank=True, max_length=32, null=True, choices=[(b'inactive', b'Mark Inactive'), (b'notify', b'Notify'), (b'ignore', b'Ignore')])),
                ('details', models.TextField(null=True, blank=True)),
                ('parent', models.ForeignKey(related_name='child_set', blank=True, to='sales.Product', null=True)),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='identities.Contact', null=True)),
            ],
            options={
                'ordering': ['code'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='SaleOrder',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('reference', models.CharField(max_length=512, null=True, blank=True)),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('total', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('total_display', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('details', models.TextField(null=True, blank=True)),
                ('assigned', models.ManyToManyField(related_name='sales_saleorder_assigned', null=True, to='core.User', blank=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='identities.Contact', null=True)),
                ('currency', models.ForeignKey(to='finance.Currency')),
                ('opportunity', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='sales.Opportunity', null=True)),
                ('payment', models.ManyToManyField(to='finance.Transaction', null=True, blank=True)),
            ],
            options={
                'ordering': ['-datetime'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='SaleSource',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=512)),
                ('active', models.BooleanField(default=False)),
                ('details', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-active', 'name'),
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='SaleStatus',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=512)),
                ('use_leads', models.BooleanField(default=False)),
                ('use_opportunities', models.BooleanField(default=False)),
                ('use_sales', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('hidden', models.BooleanField(default=False)),
                ('details', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ('hidden', '-active', 'name'),
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('start', models.DateField(default=datetime.datetime.now)),
                ('expiry', models.DateField(null=True, blank=True)),
                ('cycle_period', models.CharField(default=b'month', max_length=32, choices=[(b'daily', b'Daily'), (b'weekly', b'Weekly'), (b'monthly', b'Monthly'), (b'quarterly', b'Quarterly'), (b'yearly', b'Yearly')])),
                ('cycle_end', models.DateField(null=True, blank=True)),
                ('active', models.BooleanField(default=False)),
                ('details', models.CharField(max_length=512, null=True, blank=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='identities.Contact', null=True)),
                ('product', models.ForeignKey(blank=True, to='sales.Product', null=True)),
            ],
            options={
                'ordering': ['expiry'],
            },
            bases=('core.object',),
        ),
        migrations.AddField(
            model_name='saleorder',
            name='source',
            field=models.ForeignKey(to='sales.SaleSource'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='saleorder',
            name='status',
            field=models.ForeignKey(to='sales.SaleStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderedproduct',
            name='order',
            field=models.ForeignKey(to='sales.SaleOrder'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderedproduct',
            name='product',
            field=models.ForeignKey(to='sales.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderedproduct',
            name='subscription',
            field=models.ForeignKey(blank=True, to='sales.Subscription', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderedproduct',
            name='tax',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='finance.Tax', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='opportunity',
            name='products_interested',
            field=models.ManyToManyField(to='sales.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='opportunity',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='sales.SaleSource', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='opportunity',
            name='status',
            field=models.ForeignKey(to='sales.SaleStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lead',
            name='products_interested',
            field=models.ManyToManyField(to='sales.Product', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lead',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='sales.SaleSource', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lead',
            name='status',
            field=models.ForeignKey(to='sales.SaleStatus'),
            preserve_default=True,
        ),
    ]
