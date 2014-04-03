# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

from decimal import Decimal, ROUND_UP


def convert(obj, name, currency=None):
    display = getattr(obj, name + '_display', None)
    if not currency:
        currency = getattr(obj, name + '_currency', None)
    if display and currency:
        if currency.is_default:
            setattr(obj, name, display)
        else:
            setattr(obj, name, (
                display * currency.factor).quantize(Decimal('.01'), rounding=ROUND_UP))
    obj.save()
    return
