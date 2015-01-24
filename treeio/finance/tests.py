# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Finance: test suites
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, Perspective, ModuleSetting, Object
from treeio.finance.models import Transaction, Liability, Category, Account, Equity, Asset, Currency, Tax
from treeio.identities.models import Contact, ContactType


class FinanceModelsTest(TestCase):

    "Finance models tests"

    def test_model_category(self):
        "Test category model"
        obj = Category(name='test')
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_tax(self):
        "Test tax model"
        obj = Tax(name='test', rate=10)
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_equity(self):
        "Test equity model"
        contact_type = ContactType(name='test')
        contact_type.save()

        contact = Contact(name='test', contact_type=contact_type)
        contact.save()

        obj = Equity(
            issue_price=10, sell_price=10, issuer=contact, owner=contact)
        obj.save()
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_asset(self):
        "Test asset model"
        contact_type = ContactType(name='test')
        contact_type.save()

        contact = Contact(name='test', contact_type=contact_type)
        contact.save()

        obj = Asset(name='test', owner=contact)
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_liability(self):
        "Test liability model"
        contact_type = ContactType(name='test')
        contact_type.save()

        contact = Contact(name='test', contact_type=contact_type)
        contact.save()

        currency = Currency(code="GBP",
                            name="Pounds",
                            symbol="L",
                            is_default=True)
        currency.save()

        account = Account(
            name='test', owner=contact, balance_currency=currency)
        account.save()

        obj = Liability(name='test',
                        source=contact,
                        target=contact,
                        account=account,
                        value=10,
                        value_currency=currency)
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_account(self):
        "Test account model"
        contact_type = ContactType(name='test')
        contact_type.save()

        contact = Contact(name='test', contact_type=contact_type)
        contact.save()

        currency = Currency(code="GBP",
                            name="Pounds",
                            symbol="L",
                            is_default=True)
        currency.save()

        obj = Account(name='test', owner=contact,
                      balance_currency=currency)
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_transaction(self):
        "Test transaction model"
        contact_type = ContactType(name='test')
        contact_type.save()

        contact = Contact(name='test', contact_type=contact_type)
        contact.save()

        currency = Currency(code="GBP",
                            name="Pounds",
                            symbol="L",
                            is_default=True)
        currency.save()

        account = Account(
            name='test', owner=contact, balance_currency=currency)
        account.save()

        obj = Transaction(name='test',
                          account=account,
                          source=contact,
                          target=contact,
                          value=10,
                          value_currency=currency)
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()


class FinanceViewsTest(TestCase):

    "Finance functional tests for views"

    username = "test"
    password = "password"
    prepared = False

    def setUp(self):
        "Initial Setup"
        if not self.prepared:
            # Clean up first
            Object.objects.all().delete()
            User.objects.all().delete()

            # Create objects
            self.group, created = Group.objects.get_or_create(name='test')
            duser, created = DjangoUser.objects.get_or_create(
                username=self.username)
            duser.set_password(self.password)
            duser.save()
            self.user, created = User.objects.get_or_create(user=duser)
            self.user.save()
            perspective, created = Perspective.objects.get_or_create(
                name='default')
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

    ######################################
    # Testing views when user is logged in
    ######################################
    def test_finance_login(self):
        "Test index page with login at /finance/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance'))
        self.assertEquals(response.status_code, 200)

    def test_finance_index_login(self):
        "Test index page with login at /finance/index/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance_index_transactions'))
        self.assertEquals(response.status_code, 200)

    def test_finance_income(self):
        "Test index page with login at /finance/income/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance_income_view'))
        self.assertEquals(response.status_code, 200)

    def test_finance_balance(self):
        "Test index page with login at /finance/balance/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance_balance_sheet'))
        self.assertEquals(response.status_code, 200)

    # Account
    def test_finance_accounts_index(self):
        "Test index page with login at /finance/accounts/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance_index_accounts'))
        self.assertEquals(response.status_code, 200)

    def test_finance_account_add(self):
        "Test index page with login at /finance/account/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance_account_add'))
        self.assertEquals(response.status_code, 200)

    def test_finance_account_edit(self):
        "Test index page with login at /finance/account/edit/<account_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_account_edit', args=[self.account.id]))
        self.assertEquals(response.status_code, 200)

    def test_finance_account_view(self):
        "Test index page with login at /finance/account/view/<account_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_account_view', args=[self.account.id]))
        self.assertEquals(response.status_code, 200)

    def test_finance_account_delete(self):
        "Test index page with login at /finance/account/delete/<account_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_account_delete', args=[self.account.id]))
        self.assertEquals(response.status_code, 200)

    # Asset
    def test_finance_assets_index(self):
        "Test index page with login at /finance/assets/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance_index_assets'))
        self.assertEquals(response.status_code, 200)

    def test_finance_asset_add(self):
        "Test index page with login at /finance/asset/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance_asset_add'))
        self.assertEquals(response.status_code, 200)

    def test_finance_asset_edit(self):
        "Test index page with login at /finance/asset/edit/<asset_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_asset_edit', args=[self.asset.id]))
        self.assertEquals(response.status_code, 200)

    def test_finance_asset_view(self):
        "Test index page with login at /finance/asset/view/<asset_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_asset_view', args=[self.asset.id]))
        self.assertEquals(response.status_code, 200)

    def test_finance_asset_delete(self):
        "Test index page with login at /finance/asset/delete/<asset_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_asset_delete', args=[self.asset.id]))
        self.assertEquals(response.status_code, 200)

    # Equity
    def test_finance_equity_index(self):
        "Test index page with login at /finance/equity/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance_index_equities'))
        self.assertEquals(response.status_code, 200)

    def test_finance_equity_add(self):
        "Test index page with login at /finance/equity/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance_equity_add'))
        self.assertEquals(response.status_code, 200)

    def test_finance_equity_edit(self):
        "Test index page with login at /finance/equity/edit/<equity_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_equity_edit', args=[self.equity.id]))
        self.assertEquals(response.status_code, 200)

    def test_finance_equity_view(self):
        "Test index page with login at /finance/equity/view/<equity_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_equity_view', args=[self.equity.id]))
        self.assertEquals(response.status_code, 200)

    def test_finance_equity_delete(self):
        "Test index page with login at /finance/equity/delete/<equity_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_equity_delete', args=[self.equity.id]))
        self.assertEquals(response.status_code, 200)

    # Transaction
    def test_finance_transactions_index(self):
        "Test index page with login at /finance/transaction/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance_index_transactions'))
        self.assertEquals(response.status_code, 200)

    def test_finance_transaction_add(self):
        "Test index page with login at /finance/transaction/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance_transaction_add'))
        self.assertEquals(response.status_code, 200)

    def test_finance_transaction_add_liability(self):
        "Test index page with login at /finance/transaction/add/liability/(?P<liability_id>\d+)"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_transaction_add', args=[self.liability.id]))
        self.assertEquals(response.status_code, 200)

    def test_finance_transaction_edit(self):
        "Test index page with login at /finance/transaction/edit/<transaction_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_transaction_edit', args=[self.transaction.id]))
        self.assertEquals(response.status_code, 200)

    def test_finance_transaction_view(self):
        "Test index page with login at /finance/transaction/view/<transaction_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_transaction_view', args=[self.transaction.id]))
        self.assertEquals(response.status_code, 200)

    def test_finance_transaction_delete(self):
        "Test index page with login at /finance/transaction/delete/<transaction_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_transaction_delete', args=[self.transaction.id]))
        self.assertEquals(response.status_code, 200)

    # Liability
    def test_finance_liability_index(self):
        "Test index page with login at /finance/liability/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance_index_liabilities'))
        self.assertEquals(response.status_code, 200)

    def test_finance_liability_add(self):
        "Test index page with login at /finance/liability/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance_liability_add'))
        self.assertEquals(response.status_code, 200)

    def test_finance_liability_edit(self):
        "Test index page with login at /finance/liability/edit/<liability_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_liability_edit', args=[self.liability.id]))
        self.assertEquals(response.status_code, 200)

    def test_finance_liability_view(self):
        "Test index page with login at /finance/liability/view/<liability_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_liability_view', args=[self.liability.id]))
        self.assertEquals(response.status_code, 200)

    def test_finance_liability_delete(self):
        "Test index page with login at /finance/liability/delete/<liability_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_liability_delete', args=[self.liability.id]))
        self.assertEquals(response.status_code, 200)

     # Receivables
    def test_finance_receivables_index(self):
        "Test index page with login at /finance/receivables/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance_index_receivables'))
        self.assertEquals(response.status_code, 200)

    def test_finance_receivable_add(self):
        "Test index page with login at /finance/receivable/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance_receivable_add'))
        self.assertEquals(response.status_code, 200)

    def test_finance_receivable_edit(self):
        "Test index page with login at /finance/receivable/edit/<receivable_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_receivable_edit', args=[self.liability.id]))
        self.assertEquals(response.status_code, 200)

    def test_finance_receivable_view(self):
        "Test index page with login at /finance/receivable/view/<receivable_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_receivable_view', args=[self.liability.id]))
        self.assertEquals(response.status_code, 200)

    def test_finance_receivable_delete(self):
        "Test index page with login at /finance/liability/delete/<receivable_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_receivable_delete', args=[self.liability.id]))
        self.assertEquals(response.status_code, 200)

     # Category
    def test_finance_category_add(self):
        "Test index page with login at /finance/category/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance_category_add'))
        self.assertEquals(response.status_code, 200)

    def test_finance_category_edit(self):
        "Test index page with login at /finance/category/edit/<category_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_category_edit', args=[self.category.id]))
        self.assertEquals(response.status_code, 200)

    def test_finance_category_view(self):
        "Test index page with login at /finance/category/view/<category_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_category_view', args=[self.category.id]))
        self.assertEquals(response.status_code, 200)

    def test_finance_category_delete(self):
        "Test index page with login at /finance/category/delete/<category_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_category_delete', args=[self.category.id]))
        self.assertEquals(response.status_code, 200)

     # Currency
    def test_finance_currency_add(self):
        "Test index page with login at /finance/currency/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance_currency_add'))
        self.assertEquals(response.status_code, 200)

    def test_finance_currency_edit(self):
        "Test index page with login at /finance/currency/edit/<currency_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_currency_edit', args=[self.currency.id]))
        self.assertEquals(response.status_code, 200)

    def test_finance_currency_view(self):
        "Test index page with login at /finance/currency/view/<currency_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_currency_view', args=[self.currency.id]))
        self.assertEquals(response.status_code, 200)

    def test_finance_currency_delete(self):
        "Test index page with login at /finance/currency/delete/<currency_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_currency_delete', args=[self.currency.id]))
        self.assertEquals(response.status_code, 200)

     # Taxes
    def test_finance_tax_add(self):
        "Test index page with login at /finance/tax/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance_tax_add'))
        self.assertEquals(response.status_code, 200)

    def test_finance_tax_edit(self):
        "Test index page with login at /finance/tax/edit/<tax_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_tax_edit', args=[self.tax.id]))
        self.assertEquals(response.status_code, 200)

    def test_finance_tax_view(self):
        "Test index page with login at /finance/tax/view/<tax_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_tax_view', args=[self.tax.id]))
        self.assertEquals(response.status_code, 200)

    def test_finance_tax_delete(self):
        "Test index page with login at /finance/tax/delete/<tax_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('finance_tax_delete', args=[self.tax.id]))
        self.assertEquals(response.status_code, 200)

    # Settings
    def test_finance_settings_view(self):
        "Test index page with login at /finance/settings/view/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance_settings_view'))
        self.assertEquals(response.status_code, 200)

    def test_finance_settings_edit(self):
        "Test index page with login at /finance/settings/edit/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('finance_settings_edit'))
        self.assertEquals(response.status_code, 200)

    ######################################
    # Testing views when user is not logged in
    ######################################
    def test_index(self):
        "Test index page at /finance/"
        response = self.client.get('/finance/')
        # Redirects as unauthenticated
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_index_out(self):
        "Testing /finance/index/"
        response = self.client.get(reverse('finance_index_transactions'))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_income_out(self):
        "Testing /finance/income/"
        response = self.client.get(reverse('finance_income_view'))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_balance_out(self):
        "Testing /finance/balance/"
        response = self.client.get(reverse('finance_balance_sheet'))
        self.assertRedirects(response, reverse('user_login'))

    # Account
    def test_finance_accounts_index_out(self):
        "Testing /finance/accounts/"
        response = self.client.get(reverse('finance_index_accounts'))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_account_add_out(self):
        "Testing /finance/account/add/"
        response = self.client.get(reverse('finance_account_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_account_edit_out(self):
        "Testing /finance/account/edit/<account_id>"
        response = self.client.get(
            reverse('finance_account_edit', args=[self.account.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_account_view_out(self):
        "Testing /finance/account/view/<account_id>"
        response = self.client.get(
            reverse('finance_account_view', args=[self.account.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_account_delete_out(self):
        "Testing /finance/account/delete/<account_id>"
        response = self.client.get(
            reverse('finance_account_delete', args=[self.account.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Asset
    def test_finance_assets_index_out(self):
        "Testing /finance/assets/"
        response = self.client.get(reverse('finance_index_assets'))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_asset_add_out(self):
        "Testing /finance/asset/add/"
        response = self.client.get(reverse('finance_asset_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_asset_edit_out(self):
        "Testing /finance/asset/edit/<asset_id>"
        response = self.client.get(
            reverse('finance_asset_edit', args=[self.asset.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_asset_view_out(self):
        "Testing /finance/asset/view/<asset_id>"
        response = self.client.get(
            reverse('finance_asset_view', args=[self.asset.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_asset_delete_out(self):
        "Testing /finance/asset/delete/<asset_id>"
        response = self.client.get(
            reverse('finance_asset_delete', args=[self.asset.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Equity
    def test_finance_equity_index_out(self):
        "Testing /finance/equity/"
        response = self.client.get(reverse('finance_index_equities'))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_equity_add_out(self):
        "Testing /finance/equity/add/"
        response = self.client.get(reverse('finance_equity_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_equity_edit_out(self):
        "Tesing /finance/equity/edit/<equity_id>"
        response = self.client.get(
            reverse('finance_equity_edit', args=[self.equity.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_equity_view_out(self):
        "Testing /finance/equity/view/<equity_id>"
        response = self.client.get(
            reverse('finance_equity_view', args=[self.equity.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_equity_delete_out(self):
        "Testing /finance/equity/delete/<equity_id>"
        response = self.client.get(
            reverse('finance_equity_delete', args=[self.equity.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Transaction
    def test_finance_transactions_index_out(self):
        "Testing /finance/transaction/"
        response = self.client.get(reverse('finance_index_transactions'))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_transaction_add_out(self):
        "Testing /finance/transaction/add/"
        response = self.client.get(reverse('finance_transaction_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_transaction_add_liability_out(self):
        "Testing /finance/transaction/add/liability/(?P<liability_id>\d+)"
        response = self.client.get(
            reverse('finance_transaction_add', args=[self.liability.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_transaction_edit_out(self):
        "Testing /finance/transaction/edit/<transaction_id>"
        response = self.client.get(
            reverse('finance_transaction_edit', args=[self.transaction.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_transaction_view_out(self):
        "Testing /finance/transaction/view/<transaction_id>"
        response = self.client.get(
            reverse('finance_transaction_view', args=[self.transaction.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_transaction_delete_out(self):
        "Testing /finance/transaction/delete/<transaction_id>"
        response = self.client.get(
            reverse('finance_transaction_delete', args=[self.transaction.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Liability
    def test_finance_liability_index_out(self):
        "Testing /finance/liability/"
        response = self.client.get(reverse('finance_index_liabilities'))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_liability_add_out(self):
        "Testing /finance/liability/add/"
        response = self.client.get(reverse('finance_liability_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_liability_edit_out(self):
        "Testing /finance/liability/edit/<liability_id>"
        response = self.client.get(
            reverse('finance_liability_edit', args=[self.liability.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_liability_view_out(self):
        "Testing /finance/liability/view/<liability_id>"
        response = self.client.get(
            reverse('finance_liability_view', args=[self.liability.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_liability_delete_out(self):
        "Testing /finance/liability/delete/<liability_id>"
        response = self.client.get(
            reverse('finance_liability_delete', args=[self.liability.id]))
        self.assertRedirects(response, reverse('user_login'))

     # Receivables
    def test_finance_receivables_index_out(self):
        "Testing /finance/receivables/"
        response = self.client.get(reverse('finance_index_receivables'))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_receivable_add_out(self):
        "Testing /finance/receivable/add/"
        response = self.client.get(reverse('finance_receivable_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_receivable_edit_out(self):
        "Testing /finance/receivable/edit/<receivable_id>"
        response = self.client.get(
            reverse('finance_receivable_edit', args=[self.liability.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_receivable_view_out(self):
        "Testing /finance/receivable/view/<receivable_id>"
        response = self.client.get(
            reverse('finance_receivable_view', args=[self.liability.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_receivable_delete_out(self):
        "Testing /finance/liability/delete/<receivable_id>"
        response = self.client.get(
            reverse('finance_receivable_delete', args=[self.liability.id]))
        self.assertRedirects(response, reverse('user_login'))

     # Category
    def test_finance_category_add_out(self):
        "Testing /finance/category/add/"
        response = self.client.get(reverse('finance_category_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_category_edit_out(self):
        "Testing /finance/category/edit/<category_id>"
        response = self.client.get(
            reverse('finance_category_edit', args=[self.category.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_category_view_out(self):
        "Testing /finance/category/view/<category_id>"
        response = self.client.get(
            reverse('finance_category_view', args=[self.category.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_category_delete_out(self):
        "Testing /finance/category/delete/<category_id>"
        response = self.client.get(
            reverse('finance_category_delete', args=[self.category.id]))
        self.assertRedirects(response, reverse('user_login'))

     # Currency
    def test_finance_currency_add_out(self):
        "Testing /finance/currency/add/"
        response = self.client.get(reverse('finance_currency_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_currency_edit_out(self):
        "Testing /finance/currency/edit/<currency_id>"
        response = self.client.get(
            reverse('finance_currency_edit', args=[self.currency.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_currency_view_out(self):
        "Testing /finance/currency/view/<currency_id>"
        response = self.client.get(
            reverse('finance_currency_view', args=[self.currency.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_currency_delete_out(self):
        "Testing /finance/currency/delete/<currency_id>"
        response = self.client.get(
            reverse('finance_currency_delete', args=[self.currency.id]))
        self.assertRedirects(response, reverse('user_login'))

     # Taxes
    def test_finance_tax_add_out(self):
        "Testing /finance/tax/add/"
        response = self.client.get(reverse('finance_tax_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_tax_edit_out(self):
        "Testing /finance/tax/edit/<tax_id>"
        response = self.client.get(
            reverse('finance_tax_edit', args=[self.tax.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_tax_view_out(self):
        "Testing /finance/tax/view/<tax_id>"
        response = self.client.get(
            reverse('finance_tax_view', args=[self.tax.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_tax_delete_out(self):
        "Testing /finance/tax/delete/<tax_id>"
        response = self.client.get(
            reverse('finance_tax_delete', args=[self.tax.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Settings
    def test_finance_settings_view_out(self):
        "Testing /finance/settings/view/"
        response = self.client.get(reverse('finance_settings_view'))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_settings_edit_out(self):
        "Testing /finance/settings/edit/"
        response = self.client.get(reverse('finance_settings_edit'))
        self.assertRedirects(response, reverse('user_login'))
