# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Sales: Hardtree module definition
"""

PROPERTIES = {
    'title': 'Sales & Stock',
    'details': 'Sales and Client Relationship Management',
    'url': '/sales/',
    'system': False,
    'type': 'major'
}

URL_PATTERNS = [
    '^/sales/',
]

from treeio.sales.cron import subscription_check

# Temporarily disabled cron due to failing .currency setting
#CRON = [subscription_check]
