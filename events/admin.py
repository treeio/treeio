# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Events: admin page
"""
from treeio.events.models import Event
from django.contrib import admin


class EventAdmin(admin.ModelAdmin):

    """ Event admin """
    list_display = ('name', 'start', 'end')

admin.site.register(Event, EventAdmin)
