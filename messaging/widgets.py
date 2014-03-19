# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Messaging module widgets
"""

WIDGETS = {'widget_new_messages': {'title': 'New Messages',
                                   'size': "95%"}}


def get_widgets(request):
    "Returns a set of all available widgets"

    return WIDGETS
