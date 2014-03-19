# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- coding: utf-8 -*-

import handlers
from django.conf.urls import patterns, url
from treeio.core.api.auth import auth_engine
from treeio.core.api.doc import documentation_view
from treeio.core.api.resource import CsrfExemptResource

ad = {'authentication': auth_engine}

# sales resources
saleStatusResource = CsrfExemptResource(
    handler=handlers.SaleStatusHandler, **ad)
productResource = CsrfExemptResource(handler=handlers.ProductHandler, **ad)
sourceResource = CsrfExemptResource(handler=handlers.SaleSourceHandler, **ad)
leadResource = CsrfExemptResource(handler=handlers.LeadHandler, **ad)
opportunityResource = CsrfExemptResource(
    handler=handlers.OpportunityHandler, **ad)
orderResource = CsrfExemptResource(handler=handlers.SaleOrderHandler, **ad)
subscriptionResource = CsrfExemptResource(
    handler=handlers.SubscriptionHandler, **ad)
orderedProductResource = CsrfExemptResource(
    handler=handlers.OrderedProductHandler, **ad)

urlpatterns = patterns('',
    # Sales
    url(r'^doc$', documentation_view, kwargs={
        'module': handlers}, name="api_sales_doc"),
    url(r'^statuses$', saleStatusResource,
        name="api_sales_status"),
    url(r'^status/(?P<object_ptr>\d+)',
        saleStatusResource, name="api_sales_status"),
    url(r'^products$', productResource,
        name="api_sales_products"),
    url(r'^product/(?P<object_ptr>\d+)',
        productResource, name="api_sales_products"),
    url(r'^sources$', sourceResource,
        name="api_sales_sources"),
    url(r'^source/(?P<object_ptr>\d+)',
        sourceResource, name="api_sales_sources"),
    url(r'^leads$', leadResource, name="api_sales_leads"),
    url(r'^lead/(?P<object_ptr>\d+)',
        leadResource, name="api_sales_leads"),
    url(r'^opportunities$', opportunityResource,
        name="api_sales_opportunities"),
    url(r'^opportunity/(?P<object_ptr>\d+)',
        opportunityResource, name="api_sales_opportunities"),
    url(r'^orders$', orderResource,
        name="api_sales_orders"),
    url(r'^order/(?P<object_ptr>\d+)',
        orderResource, name="api_sales_orders"),
    url(r'^subscriptions$', subscriptionResource,
        name="api_sales_subscriptions"),
    url(r'^subscription/(?P<object_ptr>\d+)',
        subscriptionResource, name="api_sales_subscriptions"),
    url(r'^ordered_product/(?P<object_ptr>\d+)',
        orderedProductResource, name="api_sales_ordered_products"),
)
