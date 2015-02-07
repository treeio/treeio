# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Account: Hardtree module definition
"""

PROPERTIES = {
    'title': 'Account',
    'details': 'User Account',
    'url': '/account/',
    'system': True,
    'type': 'user',
}

URL_PATTERNS = [
    '^/account/',
]

#
# Cron
#
from treeio.account.cron import CronNotifier
cron_notifier = CronNotifier()

CRON = [cron_notifier.send_notifications]
