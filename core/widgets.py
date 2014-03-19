# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core module widgets
"""

#WIDGETS = {'widget_release': {'title': 'Time To Release', 'size': 300}}
WIDGETS = {'widget_welcome': {'title': 'Quick Start', 'size': "95%"}}


def get_widgets(request):
    "Returns a set of all available widgets"

    return WIDGETS
