# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Identities: Hardtree module definition
"""

PROPERTIES = {
              'title': 'Contacts',
              'details': 'Manage users, groups, companies and corresponding contacts',
              'url': '/contacts/',
              'system': True,
              'type': 'minor',
              }


URL_PATTERNS = [
                '^/contacts/',
                ]

#
# Cron
#

from treeio.identities.cron import cron_integration

CRON = [cron_integration]
