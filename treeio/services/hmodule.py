# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Service Support: Hardtree module definition
"""

PROPERTIES = {
    'title': 'Service Support',
    'details': 'Service delivery and support management',
    'url': '/services/',
    'system': False,
    'type': 'major'
}

URL_PATTERNS = [
    '^/services/',
]

#
# Cron
#

from treeio.services.cron import tickets_escalate

CRON = [tickets_escalate]
