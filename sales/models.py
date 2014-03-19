# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Sales module objects.

"""
from django.core.urlresolvers import reverse
from django.db import models

from treeio.core.models import Object, User, ModuleSetting
from treeio.identities.models import Contact
from treeio.finance.models import Transaction, Currency, Tax

from datetime import datetime, timedelta, time
from dateutil.relativedelta import relativedelta
from decimal import Decimal, ROUND_UP
from time import time as ttime


class SaleStatus(Object):
    "Status of the Sale"
    name = models.CharField(max_length=512)
    use_leads = models.BooleanField()
    use_opportunities = models.BooleanField()
    use_sales = models.BooleanField()
    active = models.BooleanField()
    hidden = models.BooleanField()
    details = models.TextField(blank=True, null=True)

    searchable = False

    def __unicode__(self):
        return unicode(self.name)

    def get_absolute_url(self):
        "Returns absolute URL"
        try:
            return reverse('sales_status_view', args=[self.id])
        except Exception:
            return ""

    class Meta:

        "SalesStatus"
        ordering = ('hidden', '-active', 'name')


class Product(Object):
    "Single Product"
    PRODUCT_TYPES = (
        ('service', 'Service'),
        ('good', 'Good'),
        ('subscription', 'Subscription'),
        ('compound', 'Compound'),
    )

    ACTION_CHOICES = (
        ('inactive', 'Mark Inactive'),
        ('notify', 'Notify'),
        ('ignore', 'Ignore'),
    )

    name = models.CharField(max_length=512)
    product_type = models.CharField(max_length=32, default='good',
        choices=PRODUCT_TYPES)
    parent = models.ForeignKey('self', blank=True, null=True,
        related_name='child_set')
    code = models.CharField(max_length=512, blank=True, null=True)
    supplier = models.ForeignKey(Contact, blank=True, null=True,
        on_delete=models.SET_NULL)
    supplier_code = models.IntegerField(blank=True, null=True)
    buy_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    sell_price = models.DecimalField(
        max_digits=20, decimal_places=2, default=0)
    stock_quantity = models.IntegerField(blank=True, null=True)
    active = models.BooleanField()
    runout_action = models.CharField(max_length=32, blank=True, null=True,
        choices=ACTION_CHOICES)
    details = models.TextField(blank=True, null=True)

    access_inherit = ('parent', '*module', '*user')

    def __unicode__(self):
        return unicode(self.name)

    def get_absolute_url(self):
        "Returns absolute URL"
        try:
            return reverse('sales_product_view', args=[self.id])
        except:
            return ""

    class Meta:

        "Product"
        ordering = ['code']


class SaleSource(Object):
    "Source of Sale e.g. Search Engine"
    name = models.CharField(max_length=512)
    active = models.BooleanField(default=False)
    details = models.TextField(blank=True, null=True)

    searchable = False

    def __unicode__(self):
        return unicode(self.name)

    def get_absolute_url(self):
        "Returns absolute URL"
        try:
            return reverse('sales_source_view', args=[self.id])
        except Exception:
            return ""

    class Meta:

        "SaleSource"
        ordering = ('-active', 'name')


class Lead(Object):
    "Lead"
    CONTACT_METHODS = (
        ('email', 'E-Mail'),
        ('phone', 'Phone'),
        ('post', 'Post'),
        ('face', 'Face to Face')
    )

    contact = models.ForeignKey(Contact)
    source = models.ForeignKey(
        SaleSource, blank=True, null=True, on_delete=models.SET_NULL)
    products_interested = models.ManyToManyField(
        Product, blank=True, null=True)
    contact_method = models.CharField(max_length=32, choices=CONTACT_METHODS)
    assigned = models.ManyToManyField(User, related_name='sales_lead_assigned',
        blank=True, null=True)
    status = models.ForeignKey(SaleStatus)
    details = models.TextField(blank=True, null=True)

    access_inherit = ('contact', '*module', '*user')

    def __unicode__(self):
        return unicode(self.contact.name)

    def get_absolute_url(self):
        "Returns absolute URL"
        try:
            return reverse('sales_lead_view', args=[self.id])
        except Exception:
            return ""

    class Meta:

        "Lead"
        ordering = ['contact']


class Opportunity(Object):
    "Opportunity"
    lead = models.ForeignKey(
        Lead, blank=True, null=True, on_delete=models.SET_NULL)
    contact = models.ForeignKey(Contact)
    products_interested = models.ManyToManyField(Product)
    source = models.ForeignKey(
        SaleSource, blank=True, null=True, on_delete=models.SET_NULL)
    expected_date = models.DateField(blank=True, null=True)
    closed_date = models.DateField(blank=True, null=True)
    assigned = models.ManyToManyField(
        User, related_name='sales_opportunity_assigned', blank=True, null=True)
    status = models.ForeignKey(SaleStatus)
    probability = models.DecimalField(
        max_digits=3, decimal_places=0, blank=True, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    amount_currency = models.ForeignKey(Currency)
    amount_display = models.DecimalField(
        max_digits=20, decimal_places=2, default=0)
    details = models.TextField(blank=True, null=True)

    access_inherit = ('lead', 'contact', '*module', '*user')

    def __unicode__(self):
        return unicode(self.contact)

    def get_absolute_url(self):
        "Returns absolute URL"
        try:
            return reverse('sales_opportunity_view', args=[self.id])
        except Exception:
            return ""

    class Meta:

        "Opportunity"
        ordering = ['-expected_date']


class SaleOrder(Object):
    "Sale Order"
    reference = models.CharField(max_length=512, blank=True, null=True)
    datetime = models.DateTimeField(default=datetime.now)
    client = models.ForeignKey(
        Contact, blank=True, null=True, on_delete=models.SET_NULL)
    opportunity = models.ForeignKey(
        Opportunity, blank=True, null=True, on_delete=models.SET_NULL)
    payment = models.ManyToManyField(Transaction, blank=True, null=True)
    source = models.ForeignKey(SaleSource)
    assigned = models.ManyToManyField(
        User, related_name='sales_saleorder_assigned', blank=True, null=True)
    status = models.ForeignKey(SaleStatus)
    currency = models.ForeignKey(Currency)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_display = models.DecimalField(
        max_digits=20, decimal_places=2, default=0)
    details = models.TextField(blank=True, null=True)

    access_inherit = ('opportunity', 'client', '*module', '*user')

    def fulfil(self):
        "Fulfil"
        for p in self.orderedproduct_set.all():
            if not p.fulfilled:
                product = p.product
                product.stock_quantity -= p.quantity
                product.save()
                p.fulfilled = True
                p.save()
            if p.subscription:
                p.subscription.renew()

    def get_next_reference(self):
        try:
            # Very dirty hack, but kinda works for reference (i.e. it doesn't
            # have to be unique)
            next_ref = SaleOrder.objects.all().aggregate(
                models.Max('id'))['id__max'] + 1
        except:
            next_ref = 1
        full_ref = '%.5d/%s' % (next_ref, str(str(ttime() * 10)[8:-2]))
        return full_ref

    def save(self, *args, **kwargs):
        "Automatically set order reference"
        super(SaleOrder, self).save(*args, **kwargs)
        try:
            conf = ModuleSetting.get_for_module(
                'treeio.sales', 'order_fulfil_status')[0]
            fulfil_status = long(conf.value)
            if self.status.id == fulfil_status:
                self.fulfil()
        except Exception:
            pass

    def __unicode__(self):
        return unicode(self.reference)

    def get_absolute_url(self):
        "Returns absolute URL"
        try:
            return reverse('sales_order_view', args=[self.id])
        except Exception:
            return ""

    def get_taxes(self, base=False):
        # TODO: Compound taxes
        taxes = {}
        ops = self.orderedproduct_set.filter(
            trash=False).filter(tax__isnull=False)
        for p in ops:
            if base:
                item_total = p.get_total()
            else:
                item_total = p.get_total_display()
            if p.tax.id in taxes:
                taxes[p.tax.id]['amount'] += (item_total * (p.tax.rate / 100)).quantize(Decimal('.01'), rounding=ROUND_UP)
            else:
                taxes[p.tax.id] = {'name': p.tax.name, 'rate': p.tax.rate,
                                   'amount': (item_total * (p.tax.rate / 100))
                                   .quantize(Decimal('.01'), rounding=ROUND_UP)}
        return taxes

    def get_taxes_total(self):
        taxes = self.get_taxes()
        total = 0
        for tax in taxes.values():
            total += tax['amount']
        return total

    def get_subtotal(self):
        sum = 0
        for p in self.orderedproduct_set.filter(trash=False):
            sum += p.get_total()
        self.total = sum
        return sum

    def get_subtotal_display(self):
        sum = 0
        for p in self.orderedproduct_set.filter(trash=False):
            sum += p.get_total_display()
        self.total_display = sum
        return sum

    def get_total(self):
        sum = 0
        for p in self.orderedproduct_set.filter(trash=False):
            sum += p.get_total()
        sum += self.get_taxes_total()
        self.total = sum
        return sum

    def get_total_display(self):
        sum = 0
        for p in self.orderedproduct_set.filter(trash=False):
            sum += p.get_total_display()
        sum += self.get_taxes_total()
        self.total_display = sum
        return sum

    def update_total(self):
        self.get_total()
        self.get_total_display()
        self.save()

    def get_total_paid(self):
        return Decimal(self.payment.filter(trash=False).aggregate(models.Sum('value_display'))['value_display__sum'] or '0')

    def balance_due(self):
        return self.get_total() - self.get_total_paid()

    class Meta:

        "SaleOrder"
        ordering = ['-datetime']


class Subscription(Object):
    "Subscription"
    CYCLE_PERIODS = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly')
    )

    client = models.ForeignKey(
        Contact, blank=True, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, blank=True, null=True)
    start = models.DateField(default=datetime.now)
    expiry = models.DateField(blank=True, null=True)
    cycle_period = models.CharField(max_length=32, choices=CYCLE_PERIODS,
        default='month')
    cycle_end = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=False)
    details = models.CharField(max_length=512, blank=True, null=True)

    access_inherit = ('client', 'product', '*module', '*user')

    def get_cycle_start(self):
        "Get the cycle start date"
        if not self.cycle_end:
            return None

        cycle_end = self.cycle_end
        # check if we're in the 5 day window before the cycle ends for this
        # subscription
        if self.cycle_period == 'monthly':
            p = relativedelta(months=+1)
        elif self.cycle_period == 'weekly':
            p = timedelta(weeks=1)
        elif self.cycle_period == 'daily':
            p = timedelta(days=1)
        elif self.cycle_period == 'quarterly':
            p = relativedelta(months=+4)
        elif self.cycle_period == 'yearly':
            p = relativedelta(years=1)
        else:
            p = relativedelta(months=+1)

        cycle_start = cycle_end - p
        return cycle_start

    def renew(self):
        "Renew"
        if self.cycle_period == 'monthly':
            p = relativedelta(months=+1)
        elif self.cycle_period == 'daily':
            p = timedelta(days=1)
        elif self.cycle_period == 'weekly':
            p = timedelta(weeks=1)
        elif self.cycle_period == 'quarterly':
            p = relativedelta(months=+4)
        elif self.cycle_period == 'yearly':
            p = relativedelta(years=1)
        else:
            p = relativedelta(months=+1)

        self.cycle_end = datetime.now().date() + p
        self.save()

    def activate(self):
        "Activate"
        if self.active:
            return
        self.renew()
        self.active = True
        self.save()

    def deactivate(self):
        "Deactivate"
        if not self.active:
            return
        self.active = False
        self.save()

    def invoice(self):
        "Create a new sale order for self"
        new_invoice = SaleOrder()
        try:
            conf = ModuleSetting.get_for_module(
                'treeio.sales', 'default_order_status')[0]
            new_invoice.status = long(conf.value)
        except Exception:
            ss = SaleStatus.objects.all()[0]
            new_invoice.status = ss
        so = SaleSource.objects.all()[0]
        new_invoice.source = so
        new_invoice.client = self.client
        new_invoice.reference = "Subscription Invoice " + \
            str(datetime.today().strftime('%Y-%m-%d'))
        new_invoice.save()
        try:
            op = self.orderedproduct_set.filter(
                trash=False).order_by('-date_created')[0]
            opn = OrderedProduct()
            opn.order = new_invoice
            opn.product = self.product
            opn.quantity = op.quantity
            opn.discount = op.discount
            opn.subscription = self
            opn.save()
        except IndexError:
            opn = OrderedProduct()
            opn.order = new_invoice
            opn.product = self.product
            opn.quantity = 1
            opn.subscription = self
            opn.save()
        return new_invoice.reference

    def check_status(self):
        """
        Checks and sets the state of the subscription
        """
        if not self.active:
            return 'Inactive'
        if self.expiry:
            if datetime.now() > datetime.combine(self.expiry, time.min):
                self.deactivate()
                return 'Expired'

        if not self.cycle_end:
            self.renew()

        cycle_end = self.cycle_end
        # check if we're in the 5 day window before the cycle ends for this
        # subscription
        if datetime.now().date() >= cycle_end:
            cycle_start = self.get_cycle_start()
            # if we haven't already invoiced them, invoice them
            grace = 3
            if (datetime.now().date() - cycle_end > timedelta(days=grace)):
                # Subscription has overrun and must be shut down
                return self.deactivate()

            try:
                conf = ModuleSetting.get_for_module(
                    'treeio.sales', 'order_fulfil_status')[0]
                order_fulfil_status = SaleStatus.objects.get(
                    pk=long(conf.value))
            except Exception:
                order_fulfil_status = None

            if self.orderedproduct_set.filter(order__datetime__gte=cycle_start).filter(order__status=order_fulfil_status):
                return 'Paid'
            elif self.orderedproduct_set.filter(order__datetime__gte=cycle_start):
                return 'Invoiced'
            else:
                self.invoice()
                return 'Invoiced'
        else:
            return 'Active'

    def __unicode__(self):
        return unicode(self.product)

    def get_absolute_url(self):
        "Returns absolute URL"
        try:
            return reverse('sales_subscription_view', args=[self.id])
        except Exception:
            return ""

    class Meta:
        "Subscription"
        ordering = ['expiry']


class OrderedProduct(Object):
    "Ordered Product"
    subscription = models.ForeignKey(Subscription, blank=True, null=True)
    product = models.ForeignKey(Product)
    quantity = models.DecimalField(max_digits=30, decimal_places=2, default=1)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax = models.ForeignKey(
        Tax, blank=True, null=True, on_delete=models.SET_NULL)
    rate = models.DecimalField(max_digits=20, decimal_places=2)
    rate_display = models.DecimalField(
        max_digits=20, decimal_places=2, default=0)
    order = models.ForeignKey(SaleOrder)
    description = models.TextField(blank=True, null=True)
    fulfilled = models.BooleanField(default=False)

    access_inherit = ('order', '*module', '*user')

    def __unicode__(self):
        return unicode(self.product)

    def get_absolute_url(self):
        "Returns absolute URL"
        try:
            return reverse('sales_ordered_view', args=[self.id])
        except Exception:
            return ""

    def get_total(self):
        "Returns total sum for this item"
        total = self.rate * self.quantity
        if self.discount:
            total = total - (total * self.discount / 100)
        if total < 0:
            total = Decimal(0)
        return total.quantize(Decimal('.01'), rounding=ROUND_UP)

    def get_total_display(self):
        "Returns total sum for this item in the display currency"
        total = self.rate_display * self.quantity
        if self.discount:
            total = total - (total * self.discount / 100)
        if total < 0:
            total = Decimal(0)
        return total.quantize(Decimal('.01'), rounding=ROUND_UP)

    class Meta:
        ordering = ['product']
