# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Identities module widgets
"""

WIDGETS = {'widget_contact_me': {'title': 'My Contact Card',
                                 'size': "95%"}}


def get_widgets(request):
    "Returns a set of all available widgets"

    return WIDGETS
