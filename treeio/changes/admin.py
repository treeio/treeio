# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Change management: admin page
"""
from treeio.changes.models import Change, ChangeSet
from django.contrib import admin


class ChangeAdmin(admin.ModelAdmin):

    """ Change admin """
    list_display = (
        'change_set', 'change_type', 'field', 'change_from', 'change_to')


class ChangeSetAdmin(admin.ModelAdmin):

    """ Change request admin """
    list_display = (
        'object', 'author', 'resolved_by', 'resolved_on', 'status', 'name')
    list_filter = ['status']

admin.site.register(Change, ChangeAdmin)
admin.site.register(ChangeSet, ChangeSetAdmin)
