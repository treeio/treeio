# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Events module URLs
"""
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('treeio.events.views',
                       url(r'^(\.(?P<response_format>\w+))?$',
                           'month_view', name='events'),

                       url(r'^index(\.(?P<response_format>\w+))?$',
                           'index', name='events_index'),
                       url(r'^upcoming(\.(?P<response_format>\w+))?/?$',
                           'upcoming', name='events_upcoming'),

                       url(r'^month(\.(?P<response_format>\w+))?/?$',
                           'month_view', name='events_month'),
                       url(r'^week(\.(?P<response_format>\w+))?/?$',
                           'week_view', name='events_week'),
                       url(r'^day(\.(?P<response_format>\w+))?/?$',
                           'day_view', name='events_day'),

                       # Events
                       url(r'^event/add(\.(?P<response_format>\w+))?/?$',
                           'event_add', name='events_event_add'),
                       url(r'^event/add/(?P<date>[0-9\-]+)/(?P<hour>[0-9]+)?(\.(?P<response_format>\w+))?/?$',
                           'event_add', name='events_event_add_to_date'),
                       url(r'^event/view/(?P<event_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'event_view', name='events_event_view'),
                       url(r'^event/edit/(?P<event_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'event_edit', name='events_event_edit'),
                       url(r'^event/delete/(?P<event_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'event_delete', name='events_event_delete'),


                       # Export iCalendar
                       url(r'^ical/?$', 'ical_all_event',
                           name='events_all_ical'),
                       )
