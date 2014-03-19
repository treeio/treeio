# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Reporting module URLs
"""
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('treeio.reports.views',

                       # Index pages
                       url(r'^(\.(?P<response_format>\w+))?$',
                           'index', name='reports'),

                       url(r'^index(\.(?P<response_format>\w+))?$',
                           'index', name='reports_index'),

                       url(r'^index/owned(\.(?P<response_format>\w+))?$',
                           'index_owned', name='reports_index_owned'),

                       # Charts

                       url(r'^chart/(?P<chart_id>\d+)/options/(?P<div_id>[a-zA-Z0-9-]+)$',
                           '_get_chart_ajax', name='reports_get_chart_ajax'),

                       url(r'^chart/add/(?P<report_id>\d+)(\.(?P<response_format>\w+))?$',
                           'chart_add', name='reports_chart_add'),

                       url(r'^chart/add/(\.(?P<response_format>\w+))?$',
                           'chart_add', name='reports_chart_add'),

                       url(r'^chart/edit/(?P<chart_id>\d+)(\.(?P<response_format>\w+))?$',
                           'chart_edit', name='reports_chart_edit'),

                       url(r'^chart/delete/(?P<chart_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'chart_delete', name='reports_chart_delete'),

                       # Reports
                       url(r'^report/edit/(?P<report_id>\d+)(\.(?P<response_format>\w+))?$',
                           'report_edit', name='reports_report_edit'),

                       url(r'^report/add(\.(?P<response_format>\w+))?$',
                           'report_add', name='reports_report_add'),

                       url(r'^report/filter/(?P<report_id>\d+)/(?P<field_name>\w+)(\.(?P<response_format>\w+))?/?$',
                           'report_filter', name='reports_report_filter'),
                       url(r'^report/filter/(?P<report_id>\d+)/(?P<field_name>\w+)/(?P<filter_index>\w+)(\.(?P<response_format>\w+))?/?$',
                           'report_filter_remove', name='reports_report_filter_remove'),
                       url(r'^report/group/(?P<report_id>\d+)/(?P<field_name>\w+)(\.(?P<response_format>\w+))?/?$',
                           'report_group', name='reports_report_group'),

                       url(r'^report/view/(?P<report_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'report_view', name='reports_report_view'),

                       url(r'^report/delete/(?P<report_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'report_delete', name='reports_report_delete'),

                       )
