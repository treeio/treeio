# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Sales integration with Events module
"""

from treeio.sales.models import Opportunity
from treeio.core.models import Object
from treeio.events.rendering import EventRenderer
from django.db.models import Q
import datetime
import time


def get_events(request):
    "Return a list of EventRenderers from available Sales"
    events = []

    query = Q(expected_date__isnull=False)
    sales = Object.filter_by_request(
        request, manager=Opportunity.objects.filter(query))

    for sale in sales:
#        event = EventRenderer(sale.contact.name, None, sale.expected_date, sale.get_absolute_url())
        event = EventRenderer(sale.contact.name, None, datetime.datetime.fromtimestamp(time.mktime(
            time.strptime(str(sale.expected_date), "%Y-%m-%d"))), sale.get_absolute_url())  # bad code
        event.css_class += " projects-calendar-task"
        events.append(event)

    return events
