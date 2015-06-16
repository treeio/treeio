# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('identities', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=512)),
                ('balance', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('balance_display', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('details', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=512)),
                ('asset_type', models.CharField(default=b'fixed', max_length=32, choices=[(b'fixed', b'Fixed'), (b'intangible', b'Intangible')])),
                ('initial_value', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('lifetime', models.DecimalField(null=True, max_digits=20, decimal_places=0, blank=True)),
                ('endlife_value', models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)),
                ('depreciation_rate', models.DecimalField(null=True, max_digits=20, decimal_places=5, blank=True)),
                ('depreciation_type', models.CharField(default=b'straight', max_length=32, null=True, blank=True, choices=[(b'straight', b'Straight Line'), (b'reducing', b'Reducing balance')])),
                ('purchase_date', models.DateField(default=datetime.datetime.now, null=True, blank=True)),
                ('current_value', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('details', models.TextField(null=True, blank=True)),
                ('owner', models.ForeignKey(to='identities.Contact')),
            ],
            options={
                'ordering': ['-purchase_date'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=512)),
                ('details', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('code', models.CharField(max_length=3, verbose_name='code')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('symbol', models.CharField(help_text='If no symbol is entered, the 3 letter code will be used.', max_length=1, null=True, verbose_name='symbol', blank=True)),
                ('factor', models.DecimalField(default=1, help_text='Specifies the ratio to the base currency, e.g. 1.324', verbose_name='factor', max_digits=10, decimal_places=4)),
                ('is_active', models.BooleanField(default=True, help_text='The currency will be updated with daily exchange rates.', verbose_name='active')),
                ('is_default', models.BooleanField(default=False, help_text='Make this the default currency.', verbose_name='default')),
            ],
            options={
                'verbose_name': 'currency',
                'verbose_name_plural': 'currencies',
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Equity',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('equity_type', models.CharField(default=b'share', max_length=32, choices=[(b'share', b'Ordinary Share'), (b'preferred', b'Preferred'), (b'warrant', b'Warrant')])),
                ('issue_price', models.DecimalField(max_digits=20, decimal_places=2)),
                ('sell_price', models.DecimalField(max_digits=20, decimal_places=2)),
                ('amount', models.PositiveIntegerField(default=1)),
                ('purchase_date', models.DateField(default=datetime.datetime.now)),
                ('details', models.TextField(null=True, blank=True)),
                ('issuer', models.ForeignKey(related_name='finance_equity_issued', to='identities.Contact')),
                ('owner', models.ForeignKey(related_name='finance_equity_owned', to='identities.Contact')),
            ],
            options={
                'ordering': ['-purchase_date'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Liability',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=512)),
                ('due_date', models.DateField(null=True, blank=True)),
                ('value', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('value_display', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('details', models.TextField(blank=True)),
                ('account', models.ForeignKey(to='finance.Account')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='finance.Category', null=True)),
                ('source', models.ForeignKey(related_name='finance_liability_source', to='identities.Contact')),
                ('target', models.ForeignKey(related_name='finance_liability_target', to='identities.Contact')),
                ('value_currency', models.ForeignKey(to='finance.Currency')),
            ],
            options={
                'ordering': ['-due_date'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=512)),
                ('rate', models.DecimalField(max_digits=4, decimal_places=2)),
                ('compound', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=512)),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('value', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('value_display', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('details', models.TextField(blank=True)),
                ('account', models.ForeignKey(to='finance.Account')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='finance.Category', null=True)),
                ('liability', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='finance.Liability', null=True)),
                ('source', models.ForeignKey(related_name='finance_transaction_source', to='identities.Contact')),
                ('target', models.ForeignKey(related_name='finance_transaction_target', to='identities.Contact')),
                ('value_currency', models.ForeignKey(to='finance.Currency')),
            ],
            options={
                'ordering': ['-datetime'],
            },
            bases=('core.object',),
        ),
        migrations.AddField(
            model_name='account',
            name='balance_currency',
            field=models.ForeignKey(to='finance.Currency'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='owner',
            field=models.ForeignKey(to='identities.Contact'),
            preserve_default=True,
        ),
    ]
