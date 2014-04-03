# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- coding: utf-8 -*-

import handlers
from django.conf.urls import patterns, url
from treeio.core.api.auth import auth_engine
from treeio.core.api.doc import documentation_view
from treeio.core.api.resource import CsrfExemptResource

ad = {'authentication': auth_engine}

# services resources
ticketStatusResource = CsrfExemptResource(
    handler=handlers.TicketStatusHandler, **ad)
serviceResource = CsrfExemptResource(handler=handlers.ServiceHandler, **ad)
slaResource = CsrfExemptResource(
    handler=handlers.ServiceLevelAgreementHandler, **ad)
agentResource = CsrfExemptResource(handler=handlers.ServiceAgentHandler, **ad)
queueResource = CsrfExemptResource(handler=handlers.TicketQueueHandler, **ad)
ticketResource = CsrfExemptResource(handler=handlers.TicketHandler, **ad)
ticketRecordResource = CsrfExemptResource(
    handler=handlers.TicketRecordHandler, **ad)

urlpatterns = patterns('',
    # Services
    url(r'^doc$', documentation_view, kwargs={
        'module': handlers}, name="api_services_doc"),
    url(r'^services$', serviceResource,
        name="api_services"),
    url(r'^service/(?P<object_ptr>\d+)',
        serviceResource, name="api_services"),
    url(r'^statuses$', ticketStatusResource,
        name="api_services_status"),
    url(r'^status/(?P<object_ptr>\d+)',
        ticketStatusResource, name="api_services_status"),
    url(r'^sla$', slaResource, name="api_services_sla"),
    url(r'^sla/(?P<object_ptr>\d+)',
        slaResource, name="api_services_sla"),
    url(r'^agents$', agentResource,
        name="api_services_agents"),
    url(r'^agent/(?P<object_ptr>\d+)',
        agentResource, name="api_services_agents"),
    url(r'^queues$', queueResource,
        name="api_services_queues"),
    url(r'^queue/(?P<object_ptr>\d+)',
        queueResource, name="api_services_queues"),
    url(r'^tickets$', ticketResource,
        name="api_services_tickets"),
    url(r'^ticket/(?P<object_ptr>\d+)',
        ticketResource, name="api_services_tickets"),
    url(r'^ticket/records/(?P<ticket_id>\d+)',
        ticketRecordResource, name="api_services_ticket_records"),
)
