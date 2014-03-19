# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Services module URLs
"""
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('treeio.services.views',
                       url(r'^(\.(?P<response_format>\w+))?$',
                           'index', name='services'),
                       url(r'^index(\.(?P<response_format>\w+))?/?$',
                           'index', name='services_index'),
                       url(r'^owned(\.(?P<response_format>\w+))?/?$',
                           'index_owned', name='services_index_owned'),
                       url(r'^assigned(\.(?P<response_format>\w+))?/?$',
                           'index_assigned', name='services_index_assigned'),

                       # Statuses
                       url(r'^status/view/(?P<status_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'status_view', name='services_status_view'),
                       url(r'^status/edit/(?P<status_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'status_edit', name='services_status_edit'),
                       url(r'^status/delete/(?P<status_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'status_delete', name='services_status_delete'),
                       url(r'^status/add(\.(?P<response_format>\w+))?/?$',
                           'status_add', name='services_status_add'),

                       # Queues
                       url(r'^queue/view/(?P<queue_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'queue_view', name='services_queue_view'),
                       url(r'^queue/edit/(?P<queue_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'queue_edit', name='services_queue_edit'),
                       url(r'^queue/delete/(?P<queue_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'queue_delete', name='services_queue_delete'),
                       url(r'^queue/add(\.(?P<response_format>\w+))?/?$',
                           'queue_add', name='services_queue_add'),

                       # Tickets
                       url(r'^ticket/view/(?P<ticket_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'ticket_view', name='services_ticket_view'),
                       url(r'^ticket/edit/(?P<ticket_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'ticket_edit', name='services_ticket_edit'),
                       url(r'^ticket/delete/(?P<ticket_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'ticket_delete', name='services_ticket_delete'),
                       url(r'^ticket/set/(?P<ticket_id>\d+)/status/(?P<status_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'ticket_set_status', name='services_ticket_set_status'),
                       url(r'^ticket/add(\.(?P<response_format>\w+))?/?$',
                           'ticket_add', name='services_ticket_add'),
                       url(r'^ticket/add/queue/(?P<queue_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'ticket_add', name='services_ticket_add_by_queue'),

                       url(r'^catalogue(\.(?P<response_format>\w+))?/?$',
                           'service_catalogue', name='services_service_catalogue'),

                       # Services
                       url(r'^service/view/(?P<service_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'service_view', name='services_service_view'),
                       url(r'^service/edit/(?P<service_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'service_edit', name='services_service_edit'),
                       url(r'^service/delete/(?P<service_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'service_delete', name='services_service_delete'),
                       url(r'^service/add(\.(?P<response_format>\w+))?/?$',
                           'service_add', name='services_service_add'),

                       # SLAs
                       url(r'^sla/add(\.(?P<response_format>\w+))?/?$',
                           'sla_add', name='services_sla_add'),
                       url(r'^sla(\.(?P<response_format>\w+))?/?$',
                           'sla_index', name='services_sla_index'),
                       url(r'^sla/view/(?P<sla_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'sla_view', name='services_sla_view'),
                       url(r'^sla/edit/(?P<sla_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'sla_edit', name='services_sla_edit'),
                       url(r'^sla/delete/(?P<sla_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'sla_delete', name='services_sla_delete'),

                       # Settings
                       url(r'^settings/view(\.(?P<response_format>\w+))?/?$',
                           'settings_view', name='services_settings_view'),
                       url(r'^settings/edit(\.(?P<response_format>\w+))?/?$',
                           'settings_edit', name='services_settings_edit'),

                       # Agents
                       url(r'^agent(\.(?P<response_format>\w+))?/?$',
                           'agent_index', name='services_agent_index'),
                       url(r'^agent/view/(?P<agent_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'agent_view', name='services_agent_view'),
                       url(r'^agent/edit/(?P<agent_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'agent_edit', name='services_agent_edit'),
                       url(r'^agent/delete/(?P<agent_id>\d+)(\.(?P<response_format>\w+))?/?$',
                           'agent_delete', name='services_agent_delete'),
                       url(r'^agent/add(\.(?P<response_format>\w+))?/?$',
                           'agent_add', name='services_agent_add'),

                       # Widgets
                       url(r'^widget/index(\.(?P<response_format>\w+))?/?$',
                           'widget_index', name='services_widget_index'),

                       # AJAX lookups
                       url(r'^ajax/tickets(\.(?P<response_format>\w+))?/?$',
                           'ajax_ticket_lookup', name='services_ajax_ticket_lookup'),
                       url(r'^ajax/agents(\.(?P<response_format>\w+))?/?$',
                           'ajax_agent_lookup', name='services_ajax_agent_lookup'),
                       )
