# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core module Administration panel URLs
"""

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('treeio.core.trash.views',
                       url(r'^(\.(?P<response_format>\w+))?/?$',
                           'index', name='core_trash'),
                       url(r'^index(\.(?P<response_format>\w+))?/?$',
                           'index', name='core_trash_index'),

                       # Actions
                       url(r'^delete/(?P<object_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'object_delete', name='core_trash_object_delete'),
                       url(r'^untrash/(?P<object_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'object_untrash', name='core_trash_object_untrash'),
                       )
