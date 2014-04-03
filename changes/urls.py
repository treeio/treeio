# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Change Control module URLs
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('treeio.changes.views',
    url(r'^(\.(?P<response_format>\w+))?$',
        'index', name='changes_index'),
    url(r'^owned(\.(?P<response_format>\w+))?$',
        'index_owned', name='changes_index_owned'),
    url(r'^resolved(\.(?P<response_format>\w+))?$',
        'index_resolved', name='changes_index_resolved'),

    # Statuses
    url(r'^status/view/(?P<status_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'status_view', name='changes_status_view'),
    url(r'^status/edit/(?P<status_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'status_edit', name='changes_status_edit'),
    url(r'^status/delete/(?P<status_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'status_delete', name='changes_status_delete'),
    url(r'^status/add(\.(?P<response_format>\w+))?/?$',
        'status_add', name='changes_status_add'),

    # Sets
    url(r'^set/view/(?P<set_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'set_view', name='changes_set_view'),
    url(r'^set/edit/(?P<set_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'set_edit', name='changes_set_edit'),
    url(r'^set/delete/(?P<set_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'set_delete', name='changes_set_delete'),
    url(r'^set/add(\.(?P<response_format>\w+))?/?$',
        'set_add', name='changes_set_add'),

    # Settings
    url(r'^settings/view(\.(?P<response_format>\w+))?/?$',
        'settings_view', name='changes_settings_view'),
    url(r'^settings/edit(\.(?P<response_format>\w+))?/?$',
        'settings_edit', name='changes_settings_edit'),
)
