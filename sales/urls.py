# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Sales module URLs
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('treeio.sales.views',
    url(r'^(\.(?P<response_format>\w+))?$', 'index', name='sales'),
    url(r'^index(\.(?P<response_format>\w+))?/?$', 'index',
        name='sales_index'),
    url(r'^index/open(\.(?P<response_format>\w+))?/?$', 'index_open',
        name='sales_index_open'),
    url(r'^index/assigned(\.(?P<response_format>\w+))?/?$', 'index_assigned',
        name='sales_index_assigned'),

    # Orders
    url(r'^order/add(\.(?P<response_format>\w+))?/?$', 'order_add',
        name='sales_order_add'),
    url(r'^order/add/lead/(?P<lead_id>\w+)(\.(?P<response_format>\w+))?/?$',
        'order_add', name='sales_order_add_with_lead'),
    url(r'^order/add/opportunity/(?P<opportunity_id>\w+)(\.(?P<response_format>\w+))?/?$',
        'order_add', name='sales_order_add_with_opportunity'),
    url(r'^order/edit/(?P<order_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'order_edit', name='sales_order_edit'),
    url(r'^order/view/(?P<order_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'order_view', name='sales_order_view'),
    url(r'^order/invoice/(?P<order_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'order_invoice_view', name='sales_order_invoice_view'),
    url(r'^order/delete/(?P<order_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'order_delete', name='sales_order_delete'),

    # Products
    url(r'^product/index(\.(?P<response_format>\w+))?/?$',
        'product_index', name='sales_product_index'),
    url(r'^product/add/(?P<parent_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'product_add', name='sales_product_add'),
    url(r'^product/add(\.(?P<response_format>\w+))?/?$',
        'product_add', name='sales_product_add'),
    url(r'^product/edit/(?P<product_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'product_edit', name='sales_product_edit'),
    url(r'^product/view/(?P<product_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'product_view', name='sales_product_view'),
    url(r'^product/delete/(?P<product_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'product_delete', name='sales_product_delete'),

    # Settings
    url(r'^settings/view(\.(?P<response_format>\w+))?/?$',
        'settings_view', name='sales_settings_view'),
    url(r'^settings/edit(\.(?P<response_format>\w+))?/?$',
        'settings_edit', name='sales_settings_edit'),

    # Statuses
    url(r'^status/add(\.(?P<response_format>\w+))?/?$',
        'status_add', name='sales_status_add'),
    url(r'^status/edit/(?P<status_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'status_edit', name='sales_status_edit'),
    url(r'^status/view/(?P<status_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'status_view', name='sales_status_view'),
    url(r'^status/delete/(?P<status_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'status_delete', name='sales_status_delete'),

    # Subscriptions
    url(r'^subscription/add(\.(?P<response_format>\w+))?/?$',
        'subscription_add', name='sales_subscription_add'),
    url(r'^subscription/add/order/(?P<order_id>\w+)/product/(?P<product_id>\w+)(\.(?P<response_format>\w+))?/?$',
        'subscription_add', name='sales_subscription_add_with_order_and_product'),
    url(r'^subscription/add/(?P<productset_id>\w+)(\.(?P<response_format>\w+))?/?$',
        'subscription_add', name='sales_subscription_add_with_product'),
    url(r'^subscription/edit/(?P<subscription_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'subscription_edit', name='sales_subscription_edit'),
    url(r'^subscription/view/(?P<subscription_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'subscription_view', name='sales_subscription_view'),
    url(r'^subscription/delete/(?P<subscription_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'subscription_delete', name='sales_subscription_delete'),

    # Ordered Products
    url(r'^ordered_product/add/(?P<order_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'ordered_product_add', name='sales_ordered_product_add'),
    url(r'^ordered_product/edit/(?P<ordered_product_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'ordered_product_edit', name='sales_ordered_product_edit'),
    url(r'^ordered_product/view/(?P<ordered_product_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'ordered_product_view', name='sales_ordered_product_view'),
    url(r'^ordered_product/delete/(?P<ordered_product_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'ordered_product_delete', name='sales_ordered_product_delete'),

    # Sources
    url(r'^source/add(\.(?P<response_format>\w+))?/?$',
        'source_add', name='sales_source_add'),
    url(r'^source/edit/(?P<source_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'source_edit', name='sales_source_edit'),
    url(r'^source/view/(?P<source_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'source_view', name='sales_source_view'),
    url(r'^source/delete/(?P<source_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'source_delete', name='sales_source_delete'),

    # Leads
    url(r'^lead/index(\.(?P<response_format>\w+))?/?$',
        'lead_index', name='sales_lead_index'),
    url(r'^lead/index/assigned(\.(?P<response_format>\w+))?/?$',
        'lead_index_assigned', name='sales_lead_index_assigned'),
    url(r'^lead/add(\.(?P<response_format>\w+))?/?$',
        'lead_add', name='sales_lead_add'),
    url(r'^lead/edit/(?P<lead_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'lead_edit', name='sales_lead_edit'),
    url(r'^lead/view/(?P<lead_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'lead_view', name='sales_lead_view'),
    url(r'^lead/delete/(?P<lead_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'lead_delete', name='sales_lead_delete'),

    # Opportunities
    url(r'^opportunity/index(\.(?P<response_format>\w+))?/?$',
        'opportunity_index', name='sales_opportunity_index'),
    url(r'^opportunity/index/assigned(\.(?P<response_format>\w+))?/?$',
        'opportunity_index_assigned', name='sales_opportunity_index_assigned'),
    url(r'^opportunity/add(\.(?P<response_format>\w+))?/?$',
        'opportunity_add', name='sales_opportunity_add'),
    url(r'^opportunity/add/lead/(?P<lead_id>\w+)(\.(?P<response_format>\w+))?/?$',
        'opportunity_add', name='sales_opportunity_add_with_lead'),
    url(r'^opportunity/edit/(?P<opportunity_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'opportunity_edit', name='sales_opportunity_edit'),
    url(r'^opportunity/view/(?P<opportunity_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'opportunity_view', name='sales_opportunity_view'),
    url(r'^opportunity/delete/(?P<opportunity_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'opportunity_delete', name='sales_opportunity_delete'),

    # AJAX lookups
    url(r'^ajax/subscription(\.(?P<response_format>\w+))?/?$',
        'ajax_subscription_lookup', name='sales_ajax_subscription_lookup'),
)
