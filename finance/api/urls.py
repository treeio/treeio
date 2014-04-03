# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- coding: utf-8 -*-

import handlers
from treeio.core.api.auth import auth_engine
from treeio.core.api.doc import documentation_view
from treeio.core.api.resource import CsrfExemptResource

from django.conf.urls import patterns, url

ad = {'authentication': auth_engine}

# finance resources
currencyResource = CsrfExemptResource(handler=handlers.CurrencyHandler, **ad)
taxResource = CsrfExemptResource(handler=handlers.TaxHandler, **ad)
categoryResource = CsrfExemptResource(handler=handlers.CategoryHandler, **ad)
assetResource = CsrfExemptResource(handler=handlers.AssetHandler, **ad)
accountResource = CsrfExemptResource(handler=handlers.AccountHandler, **ad)
equityResource = CsrfExemptResource(handler=handlers.EquityHandler, **ad)
liabilityResource = CsrfExemptResource(handler=handlers.LiabilityHandler, **ad)
transactionResource = CsrfExemptResource(
    handler=handlers.TransactionHandler, **ad)

urlpatterns = patterns('',
    # Finance
    url(r'^doc$', documentation_view, kwargs={
        'module': handlers}, name="api_finance_doc"),
    url(r'^currencies$', currencyResource,
        name="api_finance_currencies"),
    url(r'^currency/(?P<object_ptr>\d+)',
        currencyResource, name="api_finance_currencies"),
    url(r'^taxes$', taxResource, name='api_finance_taxes'),
    url(r'^tax/(?P<object_ptr>\d+)',
        taxResource, name='api_finance_taxes'),
    url(r'^categories$', categoryResource,
        name='api_finance_categories'),
    url(r'^category/(?P<object_ptr>\d+)',
        categoryResource, name='api_finance_categories'),
    url(r'^assets$', assetResource,
        name='api_finance_assets'),
    url(r'^asset/(?P<object_ptr>\d+)',
        assetResource, name='api_finance_assets'),
    url(r'^accounts$', accountResource,
        name='api_finance_accounts'),
    url(r'^account/(?P<object_ptr>\d+)',
        accountResource, name='api_finance_accounts'),
    url(r'^equities$', equityResource,
        name='api_finance_equities'),
    url(r'^equity/(?P<object_ptr>\d+)',
        equityResource, name='api_finance_equities'),
    url(r'^liabilities$', liabilityResource,
        name='api_finance_liabilities'),
    url(r'^liability/(?P<object_ptr>\d+)',
        liabilityResource, name='api_finance_liabilities'),
    url(r'^transactions$', transactionResource,
        name='api_finance_transactions'),
    url(r'^transaction/(?P<object_ptr>\d+)',
        transactionResource, name='api_finance_transactions'),
)
