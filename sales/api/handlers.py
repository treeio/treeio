# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- coding: utf-8 -*-

from __future__ import absolute_import, with_statement

__all__ = ['SaleCommonHandler',
           'SaleStatusHandler',
           'ProductHandler',
           'SaleSourceHandler',
           'LeadHandler',
           'OpportunityHandler',
           'SaleOrderHandler',
           'SubscriptionHandler',
           'OrderedProductHandler',
           ]

from treeio.core.api.utils import rc
from treeio.core.api.handlers import ObjectHandler, getOrNone
from treeio.finance.helpers import convert
from treeio.sales.models import SaleStatus, Product, SaleSource, Lead, Opportunity, SaleOrder, Subscription, OrderedProduct
from treeio.sales.forms import OrderForm, ProductForm, SaleStatusForm, LeadForm, OpportunityForm, \
    OrderedProductForm, SubscriptionForm, SaleSourceForm


class SaleCommonHandler(ObjectHandler):

    def check_create_permission(self, request, mode):
        return request.user.get_profile().is_admin('treeio.sales')

    def check_instance_permission(self, request, inst, mode):
        return request.user.get_profile().has_permission(inst, mode=mode) \
            or request.user.get_profile().is_admin('treeio.sales')


class SaleStatusHandler(SaleCommonHandler):

    "Entrypoint for SaleStatus model."

    model = SaleStatus
    form = SaleStatusForm

    @staticmethod
    def resource_uri():
        return ('api_sales_status', ['id'])


class ProductHandler(SaleCommonHandler):

    "Entrypoint for Product model."

    model = Product
    form = ProductForm

    @staticmethod
    def resource_uri():
        return ('api_sales_products', ['id'])

    def flatten_dict(self, request):
        dct = super(ProductHandler, self).flatten_dict(request)
        dct['parent'] = None
        return dct


class SaleSourceHandler(SaleCommonHandler):

    "Entrypoint for SaleSource model."

    model = SaleSource
    form = SaleSourceForm

    @staticmethod
    def resource_uri():
        return ('api_sales_sources', ['id'])


class LeadHandler(SaleCommonHandler):

    "Entrypoint for Lead model."

    model = Lead
    form = LeadForm
    fields = ('id',) + LeadForm._meta.fields

    @staticmethod
    def resource_uri():
        return ('api_sales_leads', ['id'])


class OpportunityHandler(SaleCommonHandler):

    "Entrypoint for Opportunity model."

    model = Opportunity
    form = OpportunityForm
    fields = ('id',) + OpportunityForm._meta.fields

    @staticmethod
    def resource_uri():
        return ('api_sales_opportunities', ['id'])

    def flatten_dict(self, request):
        dct = super(OpportunityHandler, self).flatten_dict(request)
        if request.method.lower() == 'post' and 'lead' in request.data:
            dct['lead'] = getOrNone(Lead, request.data['lead'])
        else:
            dct['lead'] = None
        return dct

    def create(self, request, *args, **kwargs):
        if request.data is None:
            return rc.BAD_REQUEST

        if not self.check_create_permission(request, "x"):
            return rc.FORBIDDEN

        attrs = self.flatten_dict(request)

        form = self.form(**attrs)
        if form.is_valid():
            opportunity = form.save(commit=False)
            convert(opportunity, 'amount')
            opportunity.set_user_from_request(request)
            return opportunity
        else:
            self.status = 400
            return form.errors

    def update(self, request, *args, **kwargs):
        pkfield = kwargs.get(self.model._meta.pk.name) or request.data.get(
            self.model._meta.pk.name)

        if not pkfield or request.data is None:
            return rc.BAD_REQUEST

        try:
            obj = self.model.objects.get(pk=pkfield)
        except self.model.ObjectDoesNotExist:
            return rc.NOT_FOUND

        if not self.check_instance_permission(request, obj, "w"):
            return rc.FORBIDDEN

        attrs = self.flatten_dict(request)

        form = self.form(instance=obj, **attrs)
        if form.is_valid():
            opportunity = form.save(commit=False)
            convert(opportunity, 'amount')
            return opportunity
        else:
            self.status = 400
            return form.errors


class SaleOrderHandler(SaleCommonHandler):

    "Entrypoint for SaleOrder model."

    model = SaleOrder
    form = OrderForm
    fields = ('id', 'payment', 'total', 'total_display') + \
        OrderForm._meta.fields

    @staticmethod
    def resource_uri():
        return ('api_sales_orders', ['id'])

    def flatten_dict(self, request):
        dct = super(SaleOrderHandler, self).flatten_dict(request)
        if request.method.lower() == 'post':
            if 'lead' in request.data:
                dct['lead'] = getOrNone(Lead, request.data['lead'])
            if 'opportunity' in request.data:
                dct['opportunity'] = getOrNone(
                    Opportunity, request.data['opportunity'])
        else:
            dct['lead'] = None
            dct['opportunity'] = None
        return dct


class SubscriptionHandler(SaleCommonHandler):

    "Entrypoint for Subscription model."

    model = Subscription
    form = SubscriptionForm

    @staticmethod
    def resource_uri():
        return ('api_sales_subscriptions', ['id'])

    def create(self, request, *args, **kwargs):
        if request.data is None:
            return rc.BAD_REQUEST

        if not self.check_create_permission(request, "x"):
            return rc.FORBIDDEN

        order = getOrNone(
            SaleOrder, pk=request.data['order']) if 'order' in request.data else None
        product = getOrNone(
            OrderedProduct, pk=request.data['product']) if 'product' in request.data else None
        productset = getOrNone(
            Product, pk=request.data['productset']) if 'productset' in request.data else None
        subscription = Subscription()
        if order:
            subscription.client = order.client
        if product:
            subscription.product = product.product
        if productset:
            subscription.product = productset
        form = SubscriptionForm(
            request.user.get_profile(), request.data, instance=subscription)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.renew()
            subscription.save()
            subscription.set_user_from_request(request)
            if product:
                product.subscription = subscription
                product.save()
            return subscription
        else:
            self.status = 400
            return form.errors


class OrderedProductHandler(SaleCommonHandler):

    "Entrypoint for OrderedProduct model."

    model = OrderedProduct
    form = OrderedProductForm

    @staticmethod
    def resource_uri():
        return ('api_sales_ordered_products', ['id'])

    def create(self, request, object_ptr, *args, **kwargs):
        if request.data is None:
            return rc.BAD_REQUEST

        order = getOrNone(SaleOrder, pk=object_ptr)
        if not order:
            return rc.NOT_FOUND

        if not request.user.get_profile().has_permission(order, mode='x'):
            return rc.FORBIDDEN

        ordered_product = OrderedProduct()
        ordered_product.order = order
        form = OrderedProductForm(
            request.user.get_profile(), order, request.data, instance=ordered_product)
        if form.is_valid():
            ordered_product = form.save(commit=False)
            convert(
                ordered_product, 'rate', currency=ordered_product.order.currency)
            ordered_product.set_user_from_request(request)
            ordered_product.order.update_total()
            return ordered_product
        else:
            self.status = 400
            return form.errors

    def update(self, request, object_ptr, *args, **kwargs):
        if request.data is None:
            return rc.BAD_REQUEST

        ordered_product = getOrNone(OrderedProduct, pk=object_ptr)
        if not request.user.get_profile().has_permission(ordered_product, mode='w'):
            return rc.FORBIDDEN

        order = ordered_product.order
        form = OrderedProductForm(
            request.user.get_profile(), order, request.data, instance=ordered_product)
        if form.is_valid():
            ordered_product = form.save(commit=False)
            convert(
                ordered_product, 'rate', currency=ordered_product.order.currency)
            ordered_product.order.update_total()
            return ordered_product
        else:
            self.status = 400
            return form.errors

    def delete_instance(self, request, ordered_product):
        if 'trash' in request.REQUEST:
            ordered_product.trash = True
            ordered_product.save()
        else:
            ordered_product.delete()
        ordered_product.order.update_total()
        return ordered_product if ordered_product.pk else rc.DELETED
