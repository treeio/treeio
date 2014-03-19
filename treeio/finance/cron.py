# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Finance Cron jobs
"""
from treeio.finance.models import Asset


def assets_depreciate():
    "Automatically depreciate assets as per their depreciation rate"

    assets = Asset.objects.all()
    for asset in assets:
        if not asset.trash:
            asset.set_current_value()
