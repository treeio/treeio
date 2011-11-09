# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Service Support: back-end administrator definitions
"""
from django.contrib import admin
from treeio.sales.models import Product, SaleOrder, SaleSource, Lead, Opportunity, SaleStatus

admin.site.register(SaleOrder)
admin.site.register(Product)
admin.site.register(SaleStatus)
admin.site.register(SaleSource)
admin.site.register(Lead)
admin.site.register(Opportunity)
