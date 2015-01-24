# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Services module widgets
"""

WIDGETS = {'widget_index': {'title': 'Active Service Tickets',
                            'size': "95%"},
           'widget_index_assigned': {'title': 'Service Tickets Assigned to me',
                                     'size': "95%"}}


def get_widgets(request):
    "Returns a set of all available widgets"

    widgets = {}
    widgets.update(WIDGETS)

    try:
        agent = request.user.get_profile().serviceagent_set.all()[0]
    except Exception:
        agent = None

    if not agent:
        del widgets['widget_index_assigned']

    return widgets
