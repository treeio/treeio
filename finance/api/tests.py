# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- coding: utf-8 -*-

import json
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, Perspective, ModuleSetting, Object
from treeio.finance.models import Transaction, Liability, Category, Account, Equity, Asset, Currency, Tax
from treeio.identities.models import Contact, ContactType


class FinanceAPITest(TestCase):

    "Finance api tests"
    username = "api_test"
    password = "api_password"
    prepared = False
    authentication_headers = {"CONTENT_TYPE": "application/json",
                              "HTTP_AUTHORIZATION": "Basic YXBpX3Rlc3Q6YXBpX3Bhc3N3b3Jk"}
    content_type = 'application/json'

    def setUp(self):
        "Initial Setup"
        if not self.prepared:
            # Clean up first
            Object.objects.all().delete()
            User.objects.all().delete()

            # Create objects
            try:
                self.group = Group.objects.get(name='test')
            except Group.DoesNotExist:
                Group.objects.all().delete()
                self.group = Group(name='test')
                self.group.save()

            try:
                self.user = DjangoUser.objects.get(username=self.username)
                self.user.set_password(self.password)
                try:
                    self.profile = self.user.get_profile()
                except Exception:
                    User.objects.all().delete()
                    self.user = DjangoUser(username=self.username, password='')
                    self.user.set_password(self.password)
                    self.user.save()
            except DjangoUser.DoesNotExist:
                User.objects.all().delete()
                self.user = DjangoUser(username=self.username, password='')
                self.user.set_password(self.password)
                self.user.save()

            try:
                perspective = Perspective.objects.get(name='default')
            except Perspective.DoesNotExist:
                Perspective.objects.all().delete()
                perspective = Perspective(name='default')
                perspective.set_default_user()
                perspective.save()
            ModuleSetting.set('default_perspective', perspective.id)

            self.contact_type = ContactType(name='test')
            self.contact_type.set_default_user()
            self.contact_type.save()

            self.contact = Contact(name='test', contact_type=self.contact_type)
            self.contact.set_default_user()
            self.contact.save()

            self.category = Category(name='test')
            self.category.set_default_user()
            self.category.save()

            self.equity = Equity(
                issue_price=10, sell_price=10, issuer=self.contact, owner=self.contact)
            self.equity.set_default_user()
            self.equity.save()

            self.asset = Asset(name='test', owner=self.contact)
            self.asset.set_default_user()
            self.asset.save()

            self.tax = Tax(name='test', rate=10)
            self.tax.set_default_user()
            self.tax.save()

            self.currency = Currency(code="GBP",
                                     name="Pounds",
                                     symbol="L",
                                     is_default=True)
            self.currency.set_default_user()
            self.currency.save()

            self.account = Account(
                name='test', owner=self.contact, balance_currency=self.currency)
            self.account.set_default_user()
            self.account.save()

            self.liability = Liability(name='test',
                                       source=self.contact,
                                       target=self.contact,
                                       account=self.account,
                                       value=10,
                                       value_currency=self.currency)
            self.liability.set_default_user()
            self.liability.save()

            self.transaction = Transaction(name='test', account=self.account, source=self.contact,
                                           target=self.contact, value=10, value_currency=self.currency)
            self.transaction.set_default_user()
            self.transaction.save()

            self.client = Client()

            self.prepared = True

    def test_unauthenticated_access(self):
        "Test index page at /api/finance/currencies"
        response = self.client.get('/api/finance/currencies')
        # Redirects as unauthenticated
        self.assertEquals(response.status_code, 401)

    def test_get_currencies_list(self):
        """ Test index page api/finance/currencies """
        response = self.client.get(
            path=reverse('api_finance_currencies'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_currency(self):
        response = self.client.get(path=reverse('api_finance_currencies', kwargs={
                                   'object_ptr': self.currency.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_currency(self):
        updates = {"code": "RUB", "name": "api RUB",
                   "factor": "10.00", "is_active": True}
        response = self.client.put(path=reverse('api_finance_currencies', kwargs={'object_ptr': self.currency.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['code'], updates['code'])
        self.assertEquals(data['name'], updates['name'])
        self.assertEquals(data['factor'], updates['factor'])
        self.assertEquals(data['is_active'], updates['is_active'])

    def test_get_taxes_list(self):
        """ Test index page api/finance/taxes """
        response = self.client.get(
            path=reverse('api_finance_taxes'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_tax(self):
        response = self.client.get(path=reverse(
            'api_finance_taxes', kwargs={'object_ptr': self.tax.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_tax(self):
        updates = {"name": "API TEST TAX", "rate": "20.00", "compound": False}
        response = self.client.put(path=reverse('api_finance_taxes', kwargs={'object_ptr': self.tax.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], updates['name'])
        self.assertEquals(data['rate'], updates['rate'])
        self.assertEquals(data['compound'], updates['compound'])

    def test_get_categories_list(self):
        """ Test index page api/finance/categories """
        response = self.client.get(
            path=reverse('api_finance_categories'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_category(self):
        response = self.client.get(path=reverse('api_finance_categories', kwargs={
                                   'object_ptr': self.category.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_category(self):
        updates = {"name": "Api category", "details": "api details"}
        response = self.client.put(path=reverse('api_finance_categories', kwargs={'object_ptr': self.category.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], updates['name'])
        self.assertEquals(data['details'], updates['details'])

    def test_get_assets_list(self):
        """ Test index page api/finance/assets """
        response = self.client.get(
            path=reverse('api_finance_assets'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_asset(self):
        response = self.client.get(path=reverse('api_finance_assets', kwargs={
                                   'object_ptr': self.asset.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_asset(self):
        updates = {"current_value": "20.0", "owner": self.contact.id, "asset_type": "fixed", "name": "Api name",
                   "initial_value": '40.0'}
        response = self.client.put(path=reverse('api_finance_assets', kwargs={'object_ptr': self.asset.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        print response.content
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], updates['name'])
        self.assertEquals(data['owner']['id'], updates['owner'])
        self.assertEquals(data['asset_type'], updates['asset_type'])
        self.assertEquals(data['initial_value'], updates['initial_value'])
        self.assertEquals(data['current_value'], updates['current_value'])

    def test_get_accounts_list(self):
        """ Test index page api/finance/accounts """
        response = self.client.get(
            path=reverse('api_finance_accounts'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_account(self):
        response = self.client.get(path=reverse('api_finance_accounts', kwargs={
                                   'object_ptr': self.account.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_account(self):
        updates = {"owner": self.user.id, "balance_display": 40.0,
                   "name": "api test name", "balance_currency": self.currency.id}
        response = self.client.put(path=reverse('api_finance_accounts', kwargs={'object_ptr': self.account.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], updates['name'])
        self.assertEquals(data['owner']['id'], updates['owner'])
        self.assertEquals(data['balance_display'], updates['balance_display'])
        self.assertEquals(
            data['balance_currency']['id'], updates['balance_currency'])

    def test_get_equities_list(self):
        """ Test index page api/finance/equities"""
        response = self.client.get(
            path=reverse('api_finance_equities'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_equity(self):
        response = self.client.get(path=reverse('api_finance_equities', kwargs={
                                   'object_ptr': self.equity.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_account_2(self):
        updates = {"issue_price": "100.0", "equity_type": "warrant", "sell_price": "50.0", "amount": 100,
                   "purchase_date": "2011-06-06", "owner": self.contact.id, "issuer": self.contact.id}
        response = self.client.put(path=reverse('api_finance_equities', kwargs={'object_ptr': self.equity.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['issue_price'], updates['issue_price'])
        self.assertEquals(data['equity_type'], updates['equity_type'])
        self.assertEquals(data['sell_price'], updates['sell_price'])
        self.assertEquals(data['amount'], updates['amount'])
        self.assertEquals(data['purchase_date'], updates['purchase_date'])
        self.assertEquals(data['owner']['id'], updates['owner'])
        self.assertEquals(data['issuer']['id'], updates['issuer'])
        self.assertEquals(data['issuer']['id'], updates['issuer'])

    def test_get_liabilities_list(self):
        """ Test index page api/finance/liabilities"""
        response = self.client.get(
            path=reverse('api_finance_liabilities'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_liability(self):
        response = self.client.get(path=reverse('api_finance_liabilities', kwargs={
                                   'object_ptr': self.liability.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_liability(self):
        updates = {"account": self.account.id, "target": self.contact.id, "value_display": "20.0",
                   "name": "api test name", "value_currency": self.currency.id}
        response = self.client.put(path=reverse('api_finance_liabilities', kwargs={'object_ptr': self.liability.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], updates['name'])
        self.assertEquals(data['target']['id'], updates['target'])
        self.assertEquals(data['account']['id'], updates['account'])
        self.assertEquals(data['value_display'], updates['value_display'])
        self.assertEquals(
            data['value_currency']['id'], updates['value_currency'])

    def test_get_transactions_list(self):
        """ Test index page api/finance/transactions"""
        response = self.client.get(
            path=reverse('api_finance_transactions'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_transaction(self):
        response = self.client.get(path=reverse('api_finance_transactions', kwargs={
                                   'object_ptr': self.transaction.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_transaction(self):
        updates = {"value_display": "1000.0", "account": self.account.id, "name": "api test name", "value_currency": self.currency.id,
                   "datetime": "2011-03-21 11:04:42", "target": self.contact.id, "account": self.account.id, "source": self.contact.id}
        response = self.client.put(path=reverse('api_finance_transactions', kwargs={'object_ptr': self.transaction.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        print response.content
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], updates['name'])
        self.assertEquals(data['value_display'], updates['value_display'])
        self.assertEquals(data['account']['id'], updates['account'])
        self.assertEquals(
            data['value_currency']['id'], updates['value_currency'])
        self.assertEquals(data['datetime'], updates['datetime'])
        self.assertEquals(data['target']['id'], updates['target'])
        self.assertEquals(data['account']['id'], updates['account'])
        self.assertEquals(data['source']['id'], updates['source'])
