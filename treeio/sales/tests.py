# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Sales: test suites
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, Perspective, ModuleSetting
from treeio.identities.models import Contact, ContactType
from treeio.sales.models import SaleOrder, Product, OrderedProduct, Subscription, \
    SaleStatus, SaleSource, Lead, Opportunity
from treeio.finance.models import Currency


class SalesViewsTest(TestCase):

    "Sales functional tests for views"

    username = "test"
    password = "password"
    prepared = False

    def setUp(self):
        "Initial Setup"

        if not self.prepared:
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
            self.status.set_default_user()
            self.status.save()
            self.assertNotEquals(self.status.id, None)

            self.currency = Currency(code="GBP",
                                     name="Pounds",
                                     symbol="L",
                                     is_default=True)
            self.currency.save()

            self.source = SaleSource()
            self.source.set_default_user()
            self.source.save()
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

    ######################################
    # Testing views when user is logged in
    ######################################
    def test_index(self):
        "Test page with login at /sales/index"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('sales_index'))
        self.assertEquals(response.status_code, 200)

    def test_index_open(self):
        "Test page with login at /sales/open"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('sales_index_open'))
        self.assertEquals(response.status_code, 200)

    def test_index_assigned(self):
        "Test page with login at /sales/index/assigned"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('sales_index_assigned'))
        self.assertEquals(response.status_code, 200)

    # Orders
    def test_order_add(self):
        "Test page with login at /sales/order/add"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('sales_order_add'))
        self.assertEquals(response.status_code, 200)

    def test_order_add_lead(self):
        "Test page with login at /sales/order/add/lead/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_order_add_with_lead', args=[self.lead.id]))
        self.assertEquals(response.status_code, 200)

    def test_order_add_opportunity(self):
        "Test page with login at /sales/order/add/opportunity/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_order_add_with_opportunity', args=[self.opportunity.id]))
        self.assertEquals(response.status_code, 200)

    def test_order_edit(self):
        "Test page with login at /sales/order/edit/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_order_edit', args=[self.order.id]))
        self.assertEquals(response.status_code, 200)

    def test_order_view(self):
        "Test page with login at /sales/order/view/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_order_view', args=[self.order.id]))
        self.assertEquals(response.status_code, 200)

    def test_order_delete(self):
        "Test page with login at /sales/order/delete/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_order_delete', args=[self.order.id]))
        self.assertEquals(response.status_code, 200)

    def test_order_invoice_view(self):
        "Test page with login at /sales/order/invoice/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_order_invoice_view', args=[self.order.id]))
        self.assertEquals(response.status_code, 200)

    # Products
    def test_product_index(self):
        "Test page with login at /sales/product/index"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('sales_product_index'))
        self.assertEquals(response.status_code, 200)

    def test_product_add(self):
        "Test page with login at /sales/product/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('sales_product_add'))
        self.assertEquals(response.status_code, 200)

    def test_product_add_parent(self):
        "Test page with login at /sales/product/add"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_product_add', args=[self.product.id]))
        self.assertEquals(response.status_code, 200)

    def test_product_edit(self):
        "Test page with login at /sales/product/edit/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_product_edit', args=[self.product.id]))
        self.assertEquals(response.status_code, 200)

    def test_product_view(self):
        "Test page with login at /sales/product/view/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_product_view', args=[self.product.id]))
        self.assertEquals(response.status_code, 200)

    def test_product_delete(self):
        "Test page with login at /sales/product/delete/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_product_delete', args=[self.product.id]))
        self.assertEquals(response.status_code, 200)

    # Settings
    def test_settings_view(self):
        "Test page with login at /sales/settings/view"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('sales_settings_view'))
        self.assertEquals(response.status_code, 200)

    def test_settings_edit(self):
        "Test page with login at /sales/settings/edit"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('sales_settings_edit'))
        self.assertEquals(response.status_code, 200)

    # Statuses
    def test_status_add(self):
        "Test page with login at /sales/status/add"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('sales_status_add'))
        self.assertEquals(response.status_code, 200)

    def test_status_edit(self):
        "Test page with login at /sales/status/edit/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_status_edit', args=[self.status.id]))
        self.assertEquals(response.status_code, 200)

    def test_status_view(self):
        "Test page with login at /sales/status/view/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_status_view', args=[self.status.id]))
        self.assertEquals(response.status_code, 200)

    def test_status_delete(self):
        "Test page with login at /sales/status/delete/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_status_delete', args=[self.status.id]))
        self.assertEquals(response.status_code, 200)

    # Subscriptions
    def test_subscription_add(self):
        "Test page with login at /sales/subscription/add"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('sales_subscription_add'))
        self.assertEquals(response.status_code, 200)

    def test_subscription_add_product(self):
        "Test page with login at /sales/subscription/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_subscription_add_with_product', args=[self.product.id]))
        self.assertEquals(response.status_code, 200)

    def test_subscription_edit(self):
        "Test page with login at /sales/subscription/edit/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_subscription_edit', args=[self.subscription.id]))
        self.assertEquals(response.status_code, 200)

    def test_subscription_view(self):
        "Test page with login at /sales/subscription/view/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_subscription_view', args=[self.subscription.id]))
        self.assertEquals(response.status_code, 200)

    def test_subscription_delete(self):
        "Test page with login at /sales/subscription/delete/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_subscription_delete', args=[self.subscription.id]))
        self.assertEquals(response.status_code, 200)

    # Ordered Products
    def test_ordered_product_add(self):
        "Test page with login at /sales/ordered_product/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_ordered_product_add', args=[self.order.id]))
        self.assertEquals(response.status_code, 200)

    def test_ordered_product_edit(self):
        "Test page with login at /sales/ordered_product/edit/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_ordered_product_edit', args=[self.ordered_product.id]))
        self.assertEquals(response.status_code, 200)

    def test_ordered_product_view(self):
        "Test page with login at /sales/ordered_product/view/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_ordered_product_view', args=[self.ordered_product.id]))
        self.assertEquals(response.status_code, 200)

    def test_ordered_product_delete(self):
        "Test page with login at /sales/ordered_product/delete/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_ordered_product_delete', args=[self.ordered_product.id]))
        self.assertEquals(response.status_code, 200)

    # Sources
    def test_source_add(self):
        "Test page with login at /sales/source/add"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('sales_source_add'))
        self.assertEquals(response.status_code, 200)

    def test_source_edit(self):
        "Test page with login at /sales/source/edit/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_source_edit', args=[self.source.id]))
        self.assertEquals(response.status_code, 200)

    def test_source_view(self):
        "Test page with login at /sales/source/view/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_source_view', args=[self.source.id]))
        self.assertEquals(response.status_code, 200)

    def test_source_delete(self):
        "Test page with login at /sales/source/delete/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_source_delete', args=[self.source.id]))
        self.assertEquals(response.status_code, 200)

    # Leads
    def test_lead_index(self):
        "Test page with login at /sales/lead/index"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('sales_lead_index'))
        self.assertEquals(response.status_code, 200)

    def test_lead_index_assigned(self):
        "Test page with login at /sales/lead/index/assigned"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('sales_lead_index_assigned'))
        self.assertEquals(response.status_code, 200)

    def test_lead_add(self):
        "Test page with login at /sales/lead/add"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('sales_lead_add'))
        self.assertEquals(response.status_code, 200)

    def test_lead_edit(self):
        "Test page with login at /sales/lead/edit/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_lead_edit', args=[self.lead.id]))
        self.assertEquals(response.status_code, 200)

    def test_lead_view(self):
        "Test page with login at /sales/lead/view/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_lead_view', args=[self.lead.id]))
        self.assertEquals(response.status_code, 200)

    def test_lead_delete(self):
        "Test page with login at /sales/lead/delete/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_lead_delete', args=[self.lead.id]))
        self.assertEquals(response.status_code, 200)

    # Opportunities
    def test_opportunity_index(self):
        "Test page with login at /sales/opportunity/index"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('sales_opportunity_index'))
        self.assertEquals(response.status_code, 200)

    def test_opportunity_index_assigned(self):
        "Test page with login at /sales/opportunity/index/assigned"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('sales_opportunity_index_assigned'))
        self.assertEquals(response.status_code, 200)

    def test_opportunity_add(self):
        "Test page with login at /sales/opportunity/add"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('sales_opportunity_add'))
        self.assertEquals(response.status_code, 200)

    def test_opportunity_add_lead(self):
        "Test page with login at /sales/opportunity/add/lead/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_opportunity_add_with_lead', args=[self.lead.id]))
        self.assertEquals(response.status_code, 200)

    def test_opportunity_edit(self):
        "Test page with login at /sales/opportunity/edit/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_opportunity_edit', args=[self.opportunity.id]))
        self.assertEquals(response.status_code, 200)

    def test_opportunity_view(self):
        "Test page with login at /sales/opportunity/view/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_opportunity_view', args=[self.opportunity.id]))
        self.assertEquals(response.status_code, 200)

    def test_opportunity_delete(self):
        "Test page with login at /sales/opportunity/delete/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('sales_opportunity_delete', args=[self.opportunity.id]))
        self.assertEquals(response.status_code, 200)

    ######################################
    # Testing views when user is not logged in
    ######################################
    def test_index_anonymous(self):
        "Test index page at /sales/"
        response = self.client.get('/sales/')
        # Redirects as unauthenticated
        self.assertRedirects(response, reverse('user_login'))

    def test_index_open_out(self):
        "Testing /sales/open"
        response = self.client.get(reverse('sales_index_open'))
        self.assertRedirects(response, reverse('user_login'))

    def test_index_assigned_out(self):
        "Testing /sales/index/assigned"
        response = self.client.get(reverse('sales_index_assigned'))
        self.assertRedirects(response, reverse('user_login'))

    # Orders
    def test_order_add_out(self):
        "Testing /sales/order/add"
        response = self.client.get(reverse('sales_order_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_order_add_lead_out(self):
        "Testing /sales/order/add/lead/"
        response = self.client.get(
            reverse('sales_order_add_with_lead', args=[self.lead.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_order_add_opportunity_out(self):
        "Testing /sales/order/add/opportunity/"
        response = self.client.get(
            reverse('sales_order_add_with_opportunity', args=[self.opportunity.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_order_edit_out(self):
        "Testing /sales/order/edit/"
        response = self.client.get(
            reverse('sales_order_edit', args=[self.order.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_order_view_out(self):
        "Testing /sales/order/view/"
        response = self.client.get(
            reverse('sales_order_view', args=[self.order.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_order_delete_out(self):
        "Testing /sales/order/delete/"
        response = self.client.get(
            reverse('sales_order_delete', args=[self.order.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_order_invoice_view_out(self):
        "Testing /sales/order/invoice/"
        response = self.client.get(
            reverse('sales_order_invoice_view', args=[self.order.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Products
    def test_product_index_out(self):
        "Testing /sales/product/index"
        response = self.client.get(reverse('sales_product_index'))
        self.assertRedirects(response, reverse('user_login'))

    def test_product_add_out(self):
        "Testing /sales/product/add/"
        response = self.client.get(reverse('sales_product_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_product_add_parent_out(self):
        "Testing /sales/product/add"
        response = self.client.get(
            reverse('sales_product_add', args=[self.product.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_product_edit_out(self):
        "Testing /sales/product/edit/"
        response = self.client.get(
            reverse('sales_product_edit', args=[self.product.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_product_view_out(self):
        "Testing /sales/product/view/"
        response = self.client.get(
            reverse('sales_product_view', args=[self.product.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_product_delete_out(self):
        "Testing /sales/product/delete/"
        response = self.client.get(
            reverse('sales_product_delete', args=[self.product.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Settings
    def test_settings_view_out(self):
        "Testing /sales/settings/view"
        response = self.client.get(reverse('sales_settings_view'))
        self.assertRedirects(response, reverse('user_login'))

    def test_settings_edit_out(self):
        "Testing /sales/settings/edit"
        response = self.client.get(reverse('sales_settings_edit'))
        self.assertRedirects(response, reverse('user_login'))

    # Statuses
    def test_status_add_out(self):
        "Testing /sales/status/add"
        response = self.client.get(reverse('sales_status_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_status_edit_out(self):
        "Testing /sales/status/edit/"
        response = self.client.get(
            reverse('sales_status_edit', args=[self.status.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_status_view_out(self):
        "Testing /sales/status/view/"
        response = self.client.get(
            reverse('sales_status_view', args=[self.status.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_status_delete_out(self):
        "Testing /sales/status/delete/"
        response = self.client.get(
            reverse('sales_status_delete', args=[self.status.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Subscriptions
    def test_subscription_add_out(self):
        "Testing /sales/subscription/add"
        response = self.client.get(reverse('sales_subscription_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_subscription_add_product_out(self):
        "Testing /sales/subscription/add/"
        response = self.client.get(
            reverse('sales_subscription_add_with_product', args=[self.product.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_subscription_edit_out(self):
        "Testing /sales/subscription/edit/"
        response = self.client.get(
            reverse('sales_subscription_edit', args=[self.subscription.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_subscription_view_out(self):
        "Testing /sales/subscription/view/"
        response = self.client.get(
            reverse('sales_subscription_view', args=[self.subscription.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_subscription_delete_out(self):
        "Testing /sales/subscription/delete/"
        response = self.client.get(
            reverse('sales_subscription_delete', args=[self.subscription.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Ordered Products
    def test_ordered_product_add_out(self):
        "Testing /sales/ordered_product/add/"
        response = self.client.get(
            reverse('sales_ordered_product_add', args=[self.order.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_ordered_product_edit_out(self):
        "Testing /sales/ordered_product/edit/"
        response = self.client.get(
            reverse('sales_ordered_product_edit', args=[self.ordered_product.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_ordered_product_view_out(self):
        "Testing /sales/ordered_product/view/"
        response = self.client.get(
            reverse('sales_ordered_product_view', args=[self.ordered_product.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_ordered_product_delete_out(self):
        "Testing /sales/ordered_product/delete/"
        response = self.client.get(
            reverse('sales_ordered_product_delete', args=[self.ordered_product.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Sources
    def test_source_add_out(self):
        "Testing /sales/source/add"
        response = self.client.get(reverse('sales_source_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_source_edit_out(self):
        "Testing /sales/source/edit/"
        response = self.client.get(
            reverse('sales_source_edit', args=[self.source.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_source_view_out(self):
        "Testing /sales/source/view/"
        response = self.client.get(
            reverse('sales_source_view', args=[self.source.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_source_delete_out(self):
        "Testing /sales/source/delete/"
        response = self.client.get(
            reverse('sales_source_delete', args=[self.source.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Leads
    def test_lead_index_out(self):
        "Testing /sales/lead/index"
        response = self.client.get(reverse('sales_lead_index'))
        self.assertRedirects(response, reverse('user_login'))

    def test_lead_index_assigned_out(self):
        "Testing /sales/lead/index/assigned"
        response = self.client.get(reverse('sales_lead_index_assigned'))
        self.assertRedirects(response, reverse('user_login'))

    def test_lead_add_out(self):
        "Testing /sales/lead/add"
        response = self.client.get(reverse('sales_lead_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_lead_edit_out(self):
        "Testing /sales/lead/edit/"
        response = self.client.get(
            reverse('sales_lead_edit', args=[self.lead.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_lead_view_out(self):
        "Testing /sales/lead/view/"
        response = self.client.get(
            reverse('sales_lead_view', args=[self.lead.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_lead_delete_out(self):
        "Testing /sales/lead/delete/"
        response = self.client.get(
            reverse('sales_lead_delete', args=[self.lead.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Opportunities
    def test_opportunity_index_out(self):
        "Testing /sales/opportunity/index/"
        response = self.client.get(reverse('sales_opportunity_index'))
        self.assertRedirects(response, reverse('user_login'))

    def test_opportunity_index_assigned_out(self):
        "Testing /sales/opportunity/index/assigned/"
        response = self.client.get(reverse('sales_opportunity_index_assigned'))
        self.assertRedirects(response, reverse('user_login'))

    def test_opportunity_add_out(self):
        "Testing /sales/opportunity/add/"
        response = self.client.get(reverse('sales_opportunity_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_opportunity_add_lead_out(self):
        "Testing /sales/opportunity/add/lead/"
        response = self.client.get(
            reverse('sales_opportunity_add_with_lead', args=[self.lead.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_opportunity_edit_out(self):
        "Testing /sales/opportunity/edit/"
        response = self.client.get(
            reverse('sales_opportunity_edit', args=[self.opportunity.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_opportunity_view_out(self):
        "Testing /sales/opportunity/view/"
        response = self.client.get(
            reverse('sales_opportunity_view', args=[self.opportunity.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_opportunity_delete_out(self):
        "Testing /sales/opportunity/delete/"
        response = self.client.get(
            reverse('sales_opportunity_delete', args=[self.opportunity.id]))
        self.assertRedirects(response, reverse('user_login'))
