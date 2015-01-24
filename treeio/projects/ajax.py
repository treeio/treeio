# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

from datetime import datetime
from dajaxice.core import dajaxice_functions
from dajax.core import Dajax
from treeio.projects.models import Task, Milestone
from django.contrib import messages
from django.utils.translation import ugettext as _


def gantt(request, task, start, end):
    dajax = Dajax()
    try:
        t = Task.objects.get(pk=task)
        ot = _("Task")
    except:
        t = Milestone.objects.get(pk=task)
        ot = _("Milestone")
    s = datetime.strptime(start, '%Y-%m-%d').replace(hour=12)
    e = datetime.strptime(end, '%Y-%m-%d').replace(hour=12)
    t.start_date = s
    t.end_date = e
    t.save()
    messages.add_message(request, messages.INFO, _(
        "%(ot)s \"%(t)s\" dates have been updated.") % {'ot': ot, 't': unicode(t)})
    return dajax.json()

dajaxice_functions.register(gantt)
