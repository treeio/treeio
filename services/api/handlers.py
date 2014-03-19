# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- coding: utf-8 -*-

from __future__ import absolute_import, with_statement

__all__ = ['TicketStatusHandler',
           'ServiceHandler',
           'ServiceLevelAgreementHandler',
           'ServiceAgentHandler',
           'TicketQueueHandler',
           'TicketRecordHandler',
           'TicketHandler',
           ]

from treeio.core.api.utils import rc
from piston.handler import BaseHandler
from treeio.core.models import ModuleSetting
from treeio.core.api.handlers import ObjectHandler
from treeio.services.models import TicketStatus, Service, ServiceLevelAgreement, ServiceAgent, TicketQueue, Ticket, TicketRecord
from treeio.services.forms import TicketForm, TicketStatusForm, TicketRecordForm, QueueForm, \
    ServiceForm, ServiceLevelAgreementForm, AgentForm
from treeio.services.views import _get_default_context


class TicketStatusHandler(ObjectHandler):

    "Entrypoint for TicketStatus model."

    model = TicketStatus
    form = TicketStatusForm

    @staticmethod
    def resource_uri():
        return ('api_services_status', ['id'])

    def check_create_permission(self, request, mode):
        return request.user.get_profile().is_admin('treeio.services')


class ServiceHandler(ObjectHandler):

    "Entrypoint for Service model."

    model = Service
    form = ServiceForm

    @staticmethod
    def resource_uri():
        return ('api_services', ['id'])

    def check_create_permission(self, request, mode):
        return request.user.get_profile().is_admin('treeio.services')

    def check_instance_permission(self, request, inst, mode):
        return request.user.get_profile().has_permission(inst, mode=mode) \
            or request.user.get_profile().is_admin('treeio_services')


class ServiceLevelAgreementHandler(ObjectHandler):

    "Entrypoint for ServiceLevelAgreement model."

    model = ServiceLevelAgreement
    form = ServiceLevelAgreementForm

    @staticmethod
    def resource_uri():
        return ('api_services_sla', ['id'])

    def check_create_permission(self, request, mode):
        return request.user.get_profile().is_admin('treeio.services')


class ServiceAgentHandler(ObjectHandler):

    "Entrypoint for ServiceAgent model."

    model = ServiceAgent
    form = AgentForm

    @staticmethod
    def resource_uri():
        return ('api_services_agents', ['id'])

    def check_create_permission(self, request, mode):
        return request.user.get_profile().is_admin('treeio.services')


class TicketQueueHandler(ObjectHandler):

    "Entrypoint for TicketQueue model."

    model = TicketQueue
    form = QueueForm

    @staticmethod
    def resource_uri():
        return ('api_services_queues', ['id'])

    def check_create_permission(self, request, mode):
        return request.user.get_profile().is_admin('treeio.services')


class TicketRecordHandler(BaseHandler):

    "Entrypoint for TicketRecord model."

    model = TicketRecord
    allowed_methods = ('GET', 'POST')
    fields = ('body', 'record_type', 'author', 'comments')

    @staticmethod
    def resource_uri():
        return ('api_services_ticket_records', ['id'])

    @staticmethod
    def get_ticket(request, kwargs):
        if 'ticket_id' not in kwargs:
            return rc.BAD_REQUEST
        try:
            ticket = Ticket.objects.get(pk=kwargs['ticket_id'])
        except Ticket.DoesNotExist:
            return rc.NOT_FOUND

        if not request.user.get_profile().has_permission(ticket):
            return rc.FORBIDDEN
        return ticket

    def read(self, request, *args, **kwargs):
        ticket = self.get_ticket(request, kwargs)

        if isinstance(ticket, Ticket):
            return ticket.updates.all().order_by('date_created')
        else:
            return ticket

    def create(self, request, *args, **kwargs):
        ticket = self.get_ticket(request, kwargs)
        if isinstance(ticket, Ticket):
            profile = request.user.get_profile()
            if profile.has_permission(ticket, mode='x'):
                context = _get_default_context(request)
                agent = context['agent']

                record = TicketRecord(sender=profile.get_contact())
                record.record_type = 'manual'
                if ticket.message:
                    record.message = ticket.message
                form = TicketRecordForm(
                    agent, ticket, request.data, instance=record)
                if form.is_valid():
                    record = form.save()
                    record.save()
                    record.set_user_from_request(request)
                    record.about.add(ticket)
                    ticket.set_last_updated()
                    return record
                else:
                    self.status = 400
                    return form.errors
            else:
                return rc.FORBIDDEN
        else:
            return ticket


class TicketHandler(ObjectHandler):

    "Entrypoint for Ticket model."

    model = Ticket
    form = TicketForm

    @staticmethod
    def resource_uri():
        return ('api_services_tickets', ['id'])

    def check_create_permission(self, request, mode):
        request.context = _get_default_context(request)
        request.agent = request.context['agent']
        request.profile = request.user.get_profile()

        request.queue = None
        if 'queue_id' in request.GET:
            try:
                request.queue = TicketQueue.objects.get(
                    pk=request.GET['queue_id'])
            except self.model.DoesNotExist:
                return False
            if not request.user.get_profile().has_permission(request.queue, mode='x'):
                request.queue = None
        return True

    def check_instance_permission(self, request, inst, mode):
        context = _get_default_context(request)
        request.agent = context['agent']
        request.queue = None
        return request.user.get_profile().has_permission(inst, mode=mode)

    def flatten_dict(self, request):
        dct = super(TicketHandler, self).flatten_dict(request)
        dct['agent'] = request.agent
        dct['queue'] = request.queue
        return dct

    def create_instance(self, request, *args, **kwargs):
        ticket = Ticket(creator=request.user.get_profile())
        if not request.agent:
            if request.queue:
                ticket.queue = request.queue
                if request.queue.default_ticket_status:
                    ticket.status = request.queue.default_ticket_status
                else:
                    try:
                        conf = ModuleSetting.get_for_module(
                            'treeio.services', 'default_ticket_status')[0]
                        ticket.status = TicketStatus.objects.get(
                            pk=long(conf.value))
                    except:
                        if 'statuses' in request.context:
                            try:
                                ticket.status = request.context['statuses'][0]
                            except:
                                pass
                ticket.priority = request.queue.default_ticket_priority
                ticket.service = request.queue.default_service
            else:
                try:
                    conf = ModuleSetting.get_for_module(
                        'treeio.services', 'default_ticket_status')[0]
                    ticket.status = TicketStatus.objects.get(
                        pk=long(conf.value))
                except:
                    if 'statuses' in request.context:
                        try:
                            ticket.status = request.context['statuses'][0]
                        except:
                            pass
                try:
                    conf = ModuleSetting.get_for_module(
                        'treeio.services', 'default_ticket_queue')[0]
                    ticket.queue = TicketQueue.objects.get(pk=long(conf.value))
                except:
                    if 'queues' in request.context:
                        try:
                            ticket.queue = request.context['queues'][0]
                        except:
                            pass
            try:
                ticket.caller = request.user.get_profile().get_contact()
            except:
                pass
        return ticket
