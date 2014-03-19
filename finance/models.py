# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Finance module objects
"""

from django.db import models
from treeio.core.models import Object
from treeio.identities.models import Contact
from datetime import datetime
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
import math
from decimal import Decimal, ROUND_UP


class Currency(Object):

    "Currency Object"

    code = models.CharField(_('code'), max_length=3)
    name = models.CharField(_('name'), max_length=255)
    symbol = models.CharField(_('symbol'), max_length=1, blank=True, null=True,
                              help_text=_('If no symbol is entered, the 3 letter code will be used.'))
    factor = models.DecimalField(_('factor'), max_digits=10, decimal_places=4,
                                 help_text=_(
                                     'Specifies the ratio to the base currency, e.g. 1.324'),
                                 default=1)
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('The currency will be updated with daily exchange rates.'))
    is_default = models.BooleanField(_('default'), default=False,
                                     help_text=_('Make this the default currency.'))

    class Meta:
        verbose_name = _('currency')
        verbose_name_plural = _('currencies')

    def __unicode__(self):
        # return self.code
        if self.symbol:
            return "%s    %s" % (self.symbol, self.name)
        else:
            return "%s  %s" % (self.code, self.name)

    def save(self, **kwargs):
        try:
            default_currency = Currency.objects.get(is_default=True)
            if self.is_default and not self == default_currency:
                default_currency.is_default = False
                default_currency.save()
        except:
            pass
        super(Currency, self).save(**kwargs)


class Tax(Object):

    """ Tax model """
    name = models.CharField(max_length=512)
    rate = models.DecimalField(max_digits=4, decimal_places=2)
    compound = models.BooleanField(default=False)

    def __unicode__(self):
        # return self in unicode
        return unicode(self.name)


class Category(Object):

    """ Category model """
    name = models.CharField(max_length=512)
    details = models.TextField(blank=True, null=True)

    revenue = 0
    expense = 0

    def __unicode__(self):
        return unicode(self.name)


class Asset(Object):

    """ Asset model """
    name = models.CharField(max_length=512)
    asset_type = models.CharField(max_length=32,
                                  choices=(
                                      ('fixed', 'Fixed'), ('intangible', 'Intangible')),
                                  default='fixed')
    initial_value = models.DecimalField(
        max_digits=20, decimal_places=2, default=0)
    lifetime = models.DecimalField(
        max_digits=20, decimal_places=0, blank=True, null=True)
    endlife_value = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True)
    depreciation_rate = models.DecimalField(
        max_digits=20, decimal_places=5, blank=True, null=True)
    depreciation_type = models.CharField(max_length=32, blank=True, null=True,
                                         choices=(('straight', 'Straight Line'),
                                                  ('reducing', 'Reducing balance')),
                                         default='straight')
    purchase_date = models.DateField(
        blank=True, null=True, default=datetime.now)
    current_value = models.DecimalField(
        max_digits=20, decimal_places=2, default=0)
    owner = models.ForeignKey(Contact)
    details = models.TextField(blank=True, null=True)

    class Meta:

        "Event"
        ordering = ['-purchase_date']

    def check_depreciate(self):
        "Check Depreciate"
        if (self.purchase_date and self.endlife_value is not None and self.initial_value and self.lifetime):
            return True
        else:
            return False

    def get_depreciation(self):
        "Get Depreciation"
        if self.check_depreciate():  # Edited by Renat

            self.set_rate()

            from_purchase = datetime.date(datetime.now()) - self.purchase_date
            days_from_purchase = from_purchase.days

            if days_from_purchase >= (self.lifetime * 365):
                return (self.initial_value - self.endlife_value).quantize(Decimal('.01'), rounding=ROUND_UP)

            straight = Decimal(((self.initial_value -
                                 self.endlife_value) / ((self.lifetime * 365)) *
                                days_from_purchase)).quantize(Decimal('.01'), rounding=ROUND_UP)

            if self.depreciation_type == 'reducing':
                i = self.initial_value
                daily_depreciation_rate = Decimal(str(1 - math.pow((self.endlife_value / self.initial_value),
                                                                   (1 / (self.lifetime * 365)))))
                for g in range(1, days_from_purchase):
                    i -= (i * daily_depreciation_rate)
                reducing = round(self.initial_value - i, 2)
                if reducing > straight:
                    return reducing.quantize(Decimal('.01'), rounding=ROUND_UP)
                else:
                    return straight.quantize(Decimal('.01'), rounding=ROUND_UP)

            elif self.depreciation_type == 'straight':
                return straight.quantize(Decimal('.01'), rounding=ROUND_UP)

            else:
                return Decimal('0.00')
        else:
            return Decimal('0.00')

    def set_rate(self):
        "Set Rate"
        if self.depreciation_type == 'straight':
            if self.lifetime:
                self.depreciation_rate = (100 /
                                          self.lifetime).quantize(Decimal('00.01'), rounding=ROUND_UP)

        elif self.depreciation_type == 'reducing':
            if not self.check_depreciate():
                return Decimal('0.00')
            self.depreciation_rate = Decimal(str(100 / (1 -
                                                        math.pow((self.endlife_value / self.initial_value),
                                                                 (1 / self.lifetime))))).quantize(Decimal('00.01'), rounding=ROUND_UP)
        else:
            return Decimal('0.00')
        if self.depreciation_rate == Decimal('100.00'):
            self.depreciation_rate = Decimal('99.99')

        self.save()
        return self

    def set_current_value(self):
        "Set current value"
        if not self.check_depreciate():
            return self.initial_value

        self.current_value = self.initial_value - self.get_depreciation()
        self.save()

        return self.current_value

    def __unicode__(self):
        return unicode(self.name)

    def get_absolute_url(self):
        "Returns absolute URL"
        try:
            return reverse('finance_asset_view', args=[self.id])
        except Exception:
            return ""


class Account(Object):

    """ Account model """
    name = models.CharField(max_length=512)
    owner = models.ForeignKey(Contact)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    balance_currency = models.ForeignKey(Currency)
    balance_display = models.DecimalField(
        max_digits=20, decimal_places=2, default=0)
    details = models.TextField(blank=True, null=True)

    class Meta:

        "Event"
        ordering = ['name']

    def get_balance(self):
        "Returns balance"
        bal = self.balance
        transactions = Transaction.objects.filter(account=self.id)
        for transaction in transactions:
            bal += transaction.get_relative_value()
        return bal

    def __unicode__(self):
        return unicode(self.name)

    def get_absolute_url(self):
        "Returns absolute URL"
        try:
            return reverse('finance_account_view', args=[self.id])
        except Exception:
            return ""


class Equity(Object):

    """ Equity model """
    equity_type = models.CharField(max_length=32,
                                   choices=(('share', 'Ordinary Share'), ('preferred', 'Preferred'),
                                            ('warrant', 'Warrant')),
                                   default='share')
    issue_price = models.DecimalField(max_digits=20, decimal_places=2)
    sell_price = models.DecimalField(max_digits=20, decimal_places=2)
    issuer = models.ForeignKey(Contact, related_name='finance_equity_issued')
    owner = models.ForeignKey(Contact, related_name='finance_equity_owned')
    amount = models.PositiveIntegerField(default=1)
    purchase_date = models.DateField(default=datetime.now)
    details = models.TextField(blank=True, null=True)

    class Meta:

        "Event"
        ordering = ['-purchase_date']

    def __unicode__(self):
        return unicode(unicode(self.issuer) + " (" + unicode(self.equity_type) + ")")

    def get_absolute_url(self):
        "Returns absolute URL"
        try:
            return reverse('finance_equity_view', args=[self.id])
        except Exception:
            return ""


class Liability(Object):

    """ Liability model, used for both Liabilities and Receivables """
    name = models.CharField(max_length=512)
    source = models.ForeignKey(
        Contact, related_name='finance_liability_source')
    target = models.ForeignKey(
        Contact, related_name='finance_liability_target')
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.SET_NULL)
    account = models.ForeignKey(Account)
    due_date = models.DateField(blank=True, null=True)
    value = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    value_currency = models.ForeignKey(Currency)
    value_display = models.DecimalField(
        default=0, max_digits=20, decimal_places=2)
    details = models.TextField(blank=True)

    class Meta:

        "Event"
        ordering = ['-due_date']

    def __unicode__(self):
        return unicode(self.name)

    def get_absolute_url(self):
        "Returns absolute URL"
        try:
            return reverse('finance_liability_view', args=[self.id])
        except Exception:
            return ""

    def is_receivable(self):
        "Returns True if self is receivable relative to self.account"
        return self.account.owner == self.target


class Transaction(Object):

    """ Transaction model """
    name = models.CharField(max_length=512)
    source = models.ForeignKey(
        Contact, related_name='finance_transaction_source')
    target = models.ForeignKey(
        Contact, related_name='finance_transaction_target')
    liability = models.ForeignKey(
        Liability, blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.SET_NULL)
    account = models.ForeignKey(Account)
    datetime = models.DateTimeField(default=datetime.now)
    value = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    value_currency = models.ForeignKey(Currency)
    value_display = models.DecimalField(
        default=0, max_digits=20, decimal_places=2)
    details = models.TextField(blank=True)

    class Meta:

        "Event"
        ordering = ['-datetime']

    def __unicode__(self):
        return unicode(self.name)

    def get_relative_value(self):
        "Get Relative Value"
        if self.trash:
            return 0
        elif self.account.owner_id == self.source_id:
            return -abs(self.value)
        elif self.account.owner_id == self.target_id:
            return abs(self.value)
        else:
            return 0

    def get_absolute_url(self):
        "Returns absolute URL"
        try:
            return reverse('finance_transaction_view', args=[self.id])
        except Exception:
            return ""
