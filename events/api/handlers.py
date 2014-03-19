# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- coding: utf-8 -*-

from __future__ import absolute_import, with_statement

__all__ = ['EventHandler', ]

from treeio.events.models import Event
from treeio.events.forms import EventForm
from treeio.core.api.handlers import ObjectHandler


class EventHandler(ObjectHandler):

    "Entrypoint for Event model."
    model = Event
    form = EventForm

    @staticmethod
    def resource_uri():
        return ('api_events', ['id'])

    def check_create_permission(self, request, mode):
        return True

    def flatten_dict(self, request):
        dct = super(self.__class__, self).flatten_dict(request)
        dct["date"] = None
        dct["hour"] = None
        return dct
