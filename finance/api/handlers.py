# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- coding: utf-8 -*-

from __future__ import absolute_import, with_statement

__all__ = ['CurrencyHandler',
           'TaxHandler',
           'CategoryHandler',
           'AssetHandler',
           'AccountHandler',
           'EquityHandler',
           'LiabilityHandler',
           'TransactionHandler',
           ]

from django.core.exceptions import ObjectDoesNotExist

from treeio.core.api.utils import rc
from treeio.sales.models import SaleOrder
from treeio.finance.helpers import convert
from treeio.sales.forms import dict_currencies
from treeio.core.api.handlers import ObjectHandler
from treeio.finance.models import Currency, Tax, Category, Asset, Account, Equity, Liability, Transaction
from treeio.finance.forms import TransactionForm, LiabilityForm, AccountForm, EquityForm, AssetForm, \
    CategoryForm, CurrencyForm, TaxForm


class FinanceCommonHandler(ObjectHandler):

    def check_create_permission(self, request, mode):
        return True  # request.user.get_profile().is_admin('treeio.finance')

    def check_instance_permission(self, request, inst, mode):
        return request.user.get_profile().has_permission(inst, mode=mode) \
            or request.user.get_profile().is_admin('treeio.finance')


class CurrencyHandler(ObjectHandler):

    """ Process Currency objects"""

    model = Currency
    form = CurrencyForm

    @staticmethod
    def resource_uri():
        return ('api_finance_currencies', ['id'])

    def create(self, request, *args, **kwargs):
        if request.data is None:
            return rc.BAD_REQUEST

        if not self.check_create_permission(request, "x"):
            return rc.FORBIDDEN

        currency = Currency()
        form = CurrencyForm(
            request.user.get_profile(), request.data, instance=currency)
        if form.is_valid():
            currency = form.save(commit=False)
            cname = dict_currencies[currency.code]
            currency.name = cname[cname.index(' ') + 2:]
            # currency.factor = 1.0 #Get currency conversion here
            currency.save()
            currency.set_user_from_request(request)
            return currency
        else:
            self.status = 400
            return form.errors


class TaxHandler(FinanceCommonHandler):
    model = Tax
    form = TaxForm

    @staticmethod
    def resource_uri():
        return ('api_finance_taxes', ['id'])


class CategoryHandler(FinanceCommonHandler):
    model = Category
    form = CategoryForm

    @staticmethod
    def resource_uri():
        return ('api_finance_categories', ['id'])


class AssetHandler(FinanceCommonHandler):
    model = Asset
    form = AssetForm

    @staticmethod
    def resource_uri():
        return ('api_finance_assets', ['id'])


class AccountHandler(FinanceCommonHandler):
    model = Account
    form = AccountForm

    @staticmethod
    def resource_uri():
        return ('api_finance_accounts', ['id'])

    def create(self, request, *args, **kwargs):
        if request.data is None:
            return rc.BAD_REQUEST

        if not self.check_create_permission(request, "x"):
            return rc.FORBIDDEN

        account = Account()
        form = AccountForm(
            request.user.get_profile(), request.data, instance=account)
        if form.is_valid():
            account = form.save(commit=False)
            convert(account, 'balance')
            account.set_user_from_request(request)
            return account
        else:
            self.status = 400
            return form.errors


class EquityHandler(FinanceCommonHandler):
    model = Equity
    form = EquityForm

    @staticmethod
    def resource_uri():
        return ('api_finance_equities', ['id'])


class LiabilityHandler(FinanceCommonHandler):
    model = Liability
    form = LiabilityForm

    @staticmethod
    def resource_uri():
        return ('api_finance_liabilities', ['id'])

    def create(self, request, *args, **kwargs):
        if request.data is None:
            return rc.BAD_REQUEST

        # if not self.check_create_permission(request, "x"):
        #    return rc.FORBIDDEN

        liability = self.model()
        form = self.form(
            request.user.get_profile(), request.data, instance=liability)
        if form.is_valid():
            liability = form.save(commit=False)
            liability.source = liability.account.owner
            convert(liability, 'value')
            liability.set_user_from_request(request)
            return liability
        else:
            self.status = 400
            return form.errors


class TransactionHandler(FinanceCommonHandler):
    model = Transaction
    form = TransactionForm

    @staticmethod
    def resource_uri():
        return ('api_finance_transactions', ['id'])

    def create(self, request, *args, **kwargs):
        if request.data is None:
            return rc.BAD_REQUEST

        # if not self.check_create_permission(request, "x"):
        #    return rc.FORBIDDEN

        transaction = self.model()
        form = self.form(
            request.user.get_profile(), None, None, request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save(commit=False)
            convert(transaction, 'value')
            transaction.set_user_from_request(request)
            if request.data.has_key("order"):
                try:
                    order = SaleOrder.objects.get(pk=request.data['order'])
                    order.payment.add(transaction)
                    order.save()
                except:
                    pass
            return transaction
        else:
            self.status = 400
            return form.errors

    def update(self, request, *args, **kwargs):

        pkfield = kwargs.get(self.model._meta.pk.name) or request.data.get(
            self.model._meta.pk.name)

        if not pkfield:
            return rc.BAD_REQUEST

        try:
            obj = self.model.objects.get(pk=pkfield)
        except ObjectDoesNotExist:
            return rc.NOT_FOUND

        form = self.form(
            request.user.get_profile(), None, None, request.data, instance=obj)
        if form.is_valid():
            transaction = form.save(commit=False)
            convert(transaction, 'value')
            return transaction
        else:
            self.status = 400
            return form.errors
