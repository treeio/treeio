# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core: Hardtree module definition
"""

PROPERTIES = {
    'title': 'Administration',
    'details': 'Core Administration',
    'url': '/admin/',
    'system': True,
    'type': 'user',
}

URL_PATTERNS = [
    '^/admin/',
]

#from treeio.core.cron import email_reply
#CRON = [email_reply, ]
CRON = []
