# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Messaging: Hardtree module definition
"""

PROPERTIES = {
    'title': 'Messaging',
    'details': 'Sending messages',
    'url': '/messaging/',
    'system': False,
    'type': 'minor',
}

URL_PATTERNS = [
    '^/messaging/',
]


#
# Cron
#
from treeio.messaging.cron import process_email

CRON = [process_email]
