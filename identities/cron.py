# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Identities Cron jobs
"""

from treeio.identities import integration

def cron_integration():
    "Run integration"
    try:
        integration.sync()
    except:
        pass
