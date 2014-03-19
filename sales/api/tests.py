# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- codeing: utf-8 -*-

import json
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, Perspective, ModuleSetting, Object
from treeio.identities.models import Contact, ContactType
from treeio.sales.models import SaleOrder, Product, OrderedProduct, Subscription, \
    SaleStatus, SaleSource, Lead, Opportunity
from treeio.finance.models import Currency


class SalesAPITest(TestCase):

    "Sales functional tests for views"

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

            self.contact_type = ContactType()
            self.contact_type.slug = 'machine'
            self.contact_type.name = 'machine'
            self.contact_type.save()

            self.contact = Contact()
            self.contact.contact_type = self.contact_type
            self.contact.set_default_user()
            self.contact.save()
            self.assertNotEquals(self.contact.id, None)

            self.status = SaleStatus()
            self.status.active = True
            self.status.use_sales = True
            self.status.use_leads = True
            self.status.use_opportunities = True
            self.status.set_default_user()
            self.status.save()
            self.assertNotEquals(self.status.id, None)

            self.currency = Currency(code="GBP",
                                     name="Pounds",
                                     symbol="L",
                                     is_default=True)
            self.currency.save()

            self.source = SaleSource()
            self.source.active = True
            self.source.save()
            self.source.set_user(self.user)
            self.assertNotEquals(self.source.id, None)

            self.product = Product(name="Test")
            self.product.product_type = 'service'
            self.product.active = True
            self.product.sell_price = 10
            self.product.buy_price = 100
            self.product.set_default_user()
            self.product.save()
            self.assertNotEquals(self.product.id, None)

            self.subscription = Subscription()
            self.subscription.client = self.contact
            self.subscription.set_default_user()
            self.subscription.save()
            self.assertNotEquals(self.subscription.id, None)

            self.lead = Lead()
            self.lead.contact_method = 'email'
            self.lead.status = self.status
            self.lead.contact = self.contact
            self.lead.set_default_user()
            self.lead.save()
            self.assertNotEquals(self.lead.id, None)

            self.opportunity = Opportunity()
            self.opportunity.lead = self.lead
            self.opportunity.contact = self.contact
            self.opportunity.status = self.status
            self.opportunity.amount = 100
            self.opportunity.amount_currency = self.currency
            self.opportunity.amount_display = 120
            self.opportunity.set_default_user()
            self.opportunity.save()
            self.assertNotEquals(self.opportunity.id, None)

            self.order = SaleOrder(reference="Test")
            self.order.opportunity = self.opportunity
            self.order.status = self.status
            self.order.source = self.source
            self.order.currency = self.currency
            self.order.total = 0
            self.order.total_display = 0
            self.order.set_default_user()
            self.order.save()
            self.assertNotEquals(self.order.id, None)

            self.ordered_product = OrderedProduct()
            self.ordered_product.product = self.product
            self.ordered_product.order = self.order
            self.ordered_product.rate = 0
            self.ordered_product.subscription = self.subscription
            self.ordered_product.set_default_user()
            self.ordered_product.save()

            self.assertNotEquals(self.ordered_product.id, None)

            self.client = Client()

            self.prepared = True

    def test_unauthenticated_access(self):
        "Test index page at /sales/statuses"
        response = self.client.get('/api/sales/statuses')
        # Redirects as unauthenticated
        self.assertEquals(response.status_code, 401)

    def test_get_statuses_list(self):
        """ Test index page api/sales/status """
        response = self.client.get(
            path=reverse('api_sales_status'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_status(self):
        response = self.client.get(path=reverse('api_sales_status', kwargs={
                                   'object_ptr': self.status.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_status(self):
        updates = {"name": "Close_API", "active": True, "details": "api test details",
                   "use_leads": True, "use_opportunities": True, "hidden": False}
        response = self.client.put(path=reverse('api_sales_status', kwargs={'object_ptr': self.status.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], updates['name'])
        self.assertEquals(data['active'], updates['active'])
        self.assertEquals(data['details'], updates['details'])
        self.assertEquals(data['use_leads'], updates['use_leads'])
        self.assertEquals(
            data['use_opportunities'], updates['use_opportunities'])
        self.assertEquals(data['hidden'], updates['hidden'])

    def test_get_products_list(self):
        """ Test index page api/sales/products """
        response = self.client.get(
            path=reverse('api_sales_products'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_product(self):
        response = self.client.get(path=reverse('api_sales_products', kwargs={
                                   'object_ptr': self.product.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_product(self):
        updates = {"name": "API product", "parent": None, "product_type": "service", "code": "api_test_code",
                   "buy_price": '100.05', "sell_price": '10.5', "active": True, "runout_action": "ignore", "details": "api details"}
        response = self.client.put(path=reverse('api_sales_products', kwargs={'object_ptr': self.product.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], updates['name'])
        self.assertEquals(data['product_type'], updates['product_type'])
        self.assertEquals(data['code'], updates['code'])
        self.assertEquals(data['buy_price'], updates['buy_price'])
        self.assertEquals(data['sell_price'], updates['sell_price'])
        self.assertEquals(data['active'], updates['active'])
        self.assertEquals(data['runout_action'], updates['runout_action'])
        self.assertEquals(data['details'], updates['details'])

    def test_get_sources_list(self):
        """ Test index page api/sales/sources """
        response = self.client.get(
            path=reverse('api_sales_sources'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_source(self):
        response = self.client.get(path=reverse('api_sales_sources', kwargs={
                                   'object_ptr': self.source.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_source(self):
        updates = {
            "name": "Api source", "active": True, "details": "api details"}
        response = self.client.put(path=reverse('api_sales_sources', kwargs={'object_ptr': self.source.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], updates['name'])
        self.assertEquals(data['active'], updates['active'])
        self.assertEquals(data['details'], updates['details'])
#

    def test_get_leads_list(self):
        """ Test index page api/sales/leads """
        response = self.client.get(
            path=reverse('api_sales_leads'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_lead(self):
        response = self.client.get(path=reverse(
            'api_sales_leads', kwargs={'object_ptr': self.lead.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_lead(self):
        updates = {"status": self.status.id, "contact_method": "email", "contact": self.contact.id,
                   "products_interested": [self.product.id], "source": self.source.id, 'details': 'Api details'}
        response = self.client.put(path=reverse('api_sales_leads', kwargs={'object_ptr': self.lead.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['status']['id'], updates['status'])
        self.assertEquals(data['contact_method'], updates['contact_method'])
        self.assertEquals(data['contact']['id'], updates['contact'])
        for i, product in enumerate(data['products_interested']):
            self.assertEquals(product['id'], updates['products_interested'][i])
        self.assertEquals(data['source']['id'], updates['source'])
        self.assertEquals(data['details'], updates['details'])

    def test_get_opportunities_list(self):
        """ Test index page api/sales/opportunities """
        response = self.client.get(
            path=reverse('api_sales_opportunities'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_opportunity(self):
        response = self.client.get(path=reverse('api_sales_opportunities', kwargs={
                                   'object_ptr': self.opportunity.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_opportunity(self):
        updates = {"status": self.status.id, "products_interested": [self.product.id], "contact": self.contact.id,
                   "amount_display": 3000.56, "amount_currency": self.currency.id, "details": "API DETAILS"}
        response = self.client.put(path=reverse('api_sales_opportunities', kwargs={'object_ptr': self.opportunity.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['status']['id'], updates['status'])
        self.assertEquals(data['contact']['id'], updates['contact'])
        for i, product in enumerate(data['products_interested']):
            self.assertEquals(product['id'], updates['products_interested'][i])
        self.assertEquals(
            data['amount_currency']['id'], updates['amount_currency'])
        self.assertEquals(data['details'], updates['details'])

    def test_get_orders_list(self):
        """ Test index page api/sales/orders """
        response = self.client.get(
            path=reverse('api_sales_orders'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_order(self):
        response = self.client.get(path=reverse(
            'api_sales_orders', kwargs={'object_ptr': self.order.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_order(self):
        updates = {"datetime": "2011-04-11 12:01:15", "status": self.status.id,
                   "source": self.source.id, "details": "api details"}
        response = self.client.put(path=reverse('api_sales_orders', kwargs={'object_ptr': self.order.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)

        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data['status']['id'], updates['status'])
        self.assertEquals(data['source']['id'], updates['source'])
        self.assertEquals(data['details'], updates['details'])

    def test_get_subscriptions_list(self):
        """ Test index page api/sales/subscriptions"""
        response = self.client.get(
            path=reverse('api_sales_subscriptions'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_subscription(self):
        response = self.client.get(path=reverse('api_sales_subscriptions', kwargs={
                                   'object_ptr': self.subscription.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_subscription(self):
        updates = {"product": self.product.id, "start": "2011-06-30",
                   "cycle_period": "daily", "active": True, "details": "api details"}
        response = self.client.put(path=reverse('api_sales_subscriptions', kwargs={'object_ptr': self.subscription.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['product']['id'], updates['product'])
        self.assertEquals(data['cycle_period'], updates['cycle_period'])
        self.assertEquals(data['active'], updates['active'])
        self.assertEquals(data['details'], updates['details'])

    def test_get_ordered_product(self):
        response = self.client.get(path=reverse('api_sales_ordered_products', kwargs={
                                   'object_ptr': self.ordered_product.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_ordered_product(self):
        updates = {
            "discount": '10.0', "product": self.product.id, "quantity": '10'}
        response = self.client.put(path=reverse('api_sales_ordered_products', kwargs={'object_ptr': self.ordered_product.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['product']['id'], updates['product'])
        self.assertEquals(data['discount'], updates['discount'])
        self.assertEquals(data['quantity'], updates['quantity'])
