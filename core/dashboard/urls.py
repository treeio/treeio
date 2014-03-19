# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core module Dashboard URLs
"""

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('treeio.core.dashboard.views',
                       url(r'^(\.(?P<response_format>\w+))?$',
                           'index', name='core_dashboard_index'),

                       # Widgets
                       url(r'^widget/add(\.(?P<response_format>\w+))?$',
                           'dashboard_widget_add', name='core_dashboard_widget_add'),
                       url(r'^widget/add/(?P<module_name>[a-z\.]+)/(?P<widget_name>\w+)(\.(?P<response_format>\w+))?$',
                           'dashboard_widget_add', name='core_dashboard_widget_add_selected'),
                       url(r'^widget/edit/(?P<widget_id>\d+)(\.(?P<response_format>\w+))?$',
                           'dashboard_widget_edit', name='core_dashboard_widget_edit'),
                       url(r'^widget/delete/(?P<widget_id>\d+)(\.(?P<response_format>\w+))?$',
                           'dashboard_widget_delete', name='core_dashboard_widget_delete'),

                       url(r'^widget/arrange/(?P<panel>\w+)?(\.(?P<response_format>\w+))?$',
                           'dashboard_widget_arrange', name='core_dashboard_widget_arrange'),


                       )
