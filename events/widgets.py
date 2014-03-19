# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Events module widgets
"""

WIDGETS = {'widget_week_view': {'title': 'Calendar: This Week',
                                'size': "95%"}}


def get_widgets(request):
    "Returns a set of all available widgets"

    return WIDGETS
