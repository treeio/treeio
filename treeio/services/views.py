# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Service Support module: views
"""
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from treeio.core.conf import settings
from treeio.core.rendering import render_to_response, render_string_template, render_to_string
from treeio.core.decorators import treeio_login_required, handle_response_format
from treeio.core.views import user_denied
from treeio.core.models import Object, ModuleSetting
from treeio.services.models import Ticket, TicketRecord, TicketStatus, TicketQueue, Service, \
    ServiceLevelAgreement, ServiceAgent
from treeio.services.forms import SettingsForm, MassActionForm, TicketForm, TicketStatusForm, \
    TicketRecordForm, QueueForm, ServiceForm, ServiceLevelAgreementForm, \
    AgentForm, FilterForm, SLAFilterForm, AgentFilterForm
from treeio.identities.models import Contact


def _get_filter_query(args, model=Ticket):
    "Creates a query to filter Tickets based on FilterForm arguments"
    query = Q()

    for arg in args:
        if hasattr(model, arg) and args[arg]:
            kwargs = {str(arg + '__id'): long(args[arg])}
            query = query & Q(**kwargs)

    return query


def _get_default_context(request):
    "Returns default context for all views as dict()"

    queues = Object.filter_by_request(
        request, TicketQueue.objects.filter(active=True, parent__isnull=True))
    statuses = Object.filter_by_request(request, TicketStatus.objects)
    try:
        agent = request.user.get_profile().serviceagent_set.all()[0]
    except Exception:
        agent = None

    massform = MassActionForm(request.user.get_profile())

    context = {
        'statuses': statuses,
        'queues': queues,
        'agent': agent,
        'massform': massform
    }

    return context


def _process_mass_form(f):
    "Pre-process request to handle mass action form for Tasks and Milestones"

    def wrap(request, *args, **kwargs):
        "wrap"
        if 'massform' in request.POST:
            for key in request.POST:
                if 'mass-ticket' in key:
                    try:
                        ticket = Ticket.objects.get(pk=request.POST[key])
                        form = MassActionForm(
                            request.user.get_profile(), request.POST, instance=ticket)
                        if form.is_valid() and request.user.get_profile().has_permission(ticket, mode='w'):
                            form.save()
                    except Exception:
                        pass

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__

    return wrap


@handle_response_format
@treeio_login_required
@_process_mass_form
def index(request, response_format='html'):
    "All available tickets"

    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = _get_filter_query(request.GET)
        else:
            query = Q(status__hidden=False) & _get_filter_query(request.GET)
        tickets = Object.filter_by_request(
            request, Ticket.objects.filter(query))
    else:
        tickets = Object.filter_by_request(
            request, Ticket.objects.filter(status__hidden=False))

    filters = FilterForm(request.user.get_profile(), '', request.GET)

    context = _get_default_context(request)
    context.update({'tickets': tickets,
                    'filters': filters, })

    return render_to_response('services/index', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def index_assigned(request, response_format='html'):
    "Tickets assigned to current user"

    context = _get_default_context(request)
    agent = context['agent']

    if agent:
        query = Q(assigned=agent)
        if request.GET:
            if 'status' in request.GET and request.GET['status']:
                query = query & _get_filter_query(request.GET)
            else:
                query = query & Q(
                    status__hidden=False) & _get_filter_query(request.GET)
        else:
            query = query & Q(status__hidden=False)
        tickets = Object.filter_by_request(
            request, Ticket.objects.filter(query))
    else:
        return user_denied(request, "You are not a Service Support Agent.", response_format=response_format)

    filters = FilterForm(request.user.get_profile(), 'assigned', request.GET)

    context.update({'tickets': tickets,
                    'filters': filters})

    return render_to_response('services/index_assigned', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def index_owned(request, response_format='html'):
    "Tickets owned by current user"

    context = _get_default_context(request)

    query = Q(caller__related_user=request.user.get_profile())
    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = query & _get_filter_query(request.GET)
        else:
            query = query & Q(
                status__hidden=False) & _get_filter_query(request.GET)
    else:
        query = query & Q(status__hidden=False)

    tickets = Object.filter_by_request(request, Ticket.objects.filter(query))

    filters = FilterForm(request.user.get_profile(), 'caller', request.GET)

    context.update({'tickets': tickets,
                    'filters': filters})

    return render_to_response('services/index_owned', context,
                              context_instance=RequestContext(request), response_format=response_format)

#
# Ticket Statuses
#


@handle_response_format
@treeio_login_required
@_process_mass_form
def status_view(request, status_id, response_format='html'):
    "Tickets filtered by status"

    status = get_object_or_404(TicketStatus, pk=status_id)
    if not request.user.get_profile().has_permission(status):
        return user_denied(request, message="You don't have access to this Ticket Status")

    query = Q(status=status)
    if request.GET:
        query = query & _get_filter_query(request.GET)
    tickets = Object.filter_by_request(request, Ticket.objects.filter(query))

    filters = FilterForm(request.user.get_profile(), 'status', request.GET)

    context = _get_default_context(request)
    context.update({'status': status,
                    'filters': filters,
                    'tickets': tickets})

    return render_to_response('services/status_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def status_edit(request, status_id, response_format='html'):
    "TicketStatus edit"

    status = get_object_or_404(TicketStatus, pk=status_id)
    if not request.user.get_profile().has_permission(status, mode='w') \
            and not request.user.get_profile().is_admin('treeio_services'):
        return user_denied(request, "You don't have access to this Ticket Status", response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            form = TicketStatusForm(
                request.user.get_profile(), request.POST, instance=status)
            if form.is_valid():
                status = form.save()
                return HttpResponseRedirect(reverse('services_status_view', args=[status.id]))
        else:
            return HttpResponseRedirect(reverse('services_status_view', args=[status.id]))
    else:
        form = TicketStatusForm(request.user.get_profile(), instance=status)

    context = _get_default_context(request)
    context.update({'form': form,
                    'status': status})

    return render_to_response('services/status_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def status_delete(request, status_id, response_format='html'):
    "TicketStatus delete"

    status = get_object_or_404(TicketStatus, pk=status_id)
    if not request.user.get_profile().has_permission(status, mode='w'):
        return user_denied(request, "You don't have access to this Ticket Status", response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                status.trash = True
                status.save()
            else:
                status.delete()
            return HttpResponseRedirect(reverse('services_settings_view'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('services_status_view', args=[status.id]))

    context = _get_default_context(request)
    context.update({'status': status})

    return render_to_response('services/status_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def status_add(request, response_format='html'):
    "TicketStatus add"

    if not request.user.get_profile().is_admin('treeio.services'):
        return user_denied(request,
                           message="You don't have administrator access to the Service Support module")

    if request.POST:
        if not 'cancel' in request.POST:
            status = TicketStatus()
            form = TicketStatusForm(
                request.user.get_profile(), request.POST, instance=status)
            if form.is_valid():
                status = form.save()
                status.set_user_from_request(request)
                return HttpResponseRedirect(reverse('services_status_view', args=[status.id]))
        else:
            return HttpResponseRedirect(reverse('services_settings_view'))
    else:
        form = TicketStatusForm(request.user.get_profile())

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('services/status_add', context,
                              context_instance=RequestContext(request), response_format=response_format)

#
# Queues
#


@handle_response_format
@treeio_login_required
@_process_mass_form
def queue_view(request, queue_id, response_format='html'):
    "Queue view"

    queue = get_object_or_404(TicketQueue, pk=queue_id)
    if not request.user.get_profile().has_permission(queue):
        return user_denied(request, message="You don't have access to this Queue")

    query = Q(queue=queue)
    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = query & _get_filter_query(request.GET)
        else:
            query = query & Q(
                status__hidden=False) & _get_filter_query(request.GET)
    else:
        query = query & Q(status__hidden=False)
    tickets = Object.filter_by_request(request, Ticket.objects.filter(query))

    filters = FilterForm(request.user.get_profile(), 'queue', request.GET)
    subqueues = Object.filter_by_request(
        request, TicketQueue.objects.filter(parent=queue))

    context = _get_default_context(request)
    context.update({'queue': queue,
                    'subqueues': subqueues,
                    'filters': filters,
                    'tickets': tickets})

    return render_to_response('services/queue_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def queue_edit(request, queue_id, response_format='html'):
    "Queue edit"

    queue = get_object_or_404(TicketQueue, pk=queue_id)
    if not request.user.get_profile().has_permission(queue, mode='w'):
        return user_denied(request, message="You don't have access to this Queue")

    if request.POST:
        if not 'cancel' in request.POST:
            form = QueueForm(
                request.user.get_profile(), request.POST, instance=queue)
            if form.is_valid():
                queue = form.save()
                return HttpResponseRedirect(reverse('services_queue_view', args=[queue.id]))
        else:
            return HttpResponseRedirect(reverse('services_queue_view', args=[queue.id]))
    else:
        form = QueueForm(request.user.get_profile(), instance=queue)

    context = _get_default_context(request)
    context.update({'queue': queue, 'form': form})

    return render_to_response('services/queue_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def queue_delete(request, queue_id, response_format='html'):
    "Queue delete"

    queue = get_object_or_404(TicketQueue, pk=queue_id)
    if not request.user.get_profile().has_permission(queue, mode='w'):
        return user_denied(request, message="You don't have access to this Queue")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                queue.trash = True
                queue.save()
            else:
                queue.delete()
            return HttpResponseRedirect(reverse('services_settings_view'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('services_queue_view', args=[queue.id]))

    query = Q(queue=queue) & Q(status__hidden=False)
    tickets = Object.filter_by_request(request, Ticket.objects.filter(query))
    subqueues = Object.filter_by_request(
        request, TicketQueue.objects.filter(parent=queue))

    context = _get_default_context(request)
    context.update({'queue': queue,
                    'subqueues': subqueues,
                    'tickets': tickets})

    return render_to_response('services/queue_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def queue_add(request, response_format='html'):
    "Queue add"

    if not request.user.get_profile().is_admin('treeio.services'):
        return user_denied(request,
                           message="You don't have administrator access to the Service Support module")

    if request.POST:
        if not 'cancel' in request.POST:
            queue = TicketQueue()
            form = QueueForm(
                request.user.get_profile(), request.POST, instance=queue)
            if form.is_valid():
                queue = form.save()
                queue.set_user_from_request(request)
                return HttpResponseRedirect(reverse('services_queue_view', args=[queue.id]))
        else:
            return HttpResponseRedirect(reverse('services_settings_view'))
    else:
        form = QueueForm(request.user.get_profile())

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('services/queue_add', context,
                              context_instance=RequestContext(request), response_format=response_format)

#
# Tickets
#


@handle_response_format
@treeio_login_required
def ticket_view(request, ticket_id, response_format='html'):
    "Ticket view"

    context = _get_default_context(request)
    agent = context['agent']
    profile = request.user.get_profile()

    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if not profile.has_permission(ticket):
        return user_denied(request, message="You don't have access to this Ticket")

    if ticket.message:
        ticket.message.read_by.add(profile)

    if profile.has_permission(ticket, mode='x'):
        if request.POST:
            record = TicketRecord(sender=profile.get_contact())
            record.record_type = 'manual'
            if ticket.message:
                record.message = ticket.message
            form = TicketRecordForm(
                agent, ticket, request.POST, instance=record)
            if form.is_valid():
                record = form.save()
                record.save()
                record.set_user_from_request(request)
                record.about.add(ticket)
                ticket.set_last_updated()
                return HttpResponseRedirect(reverse('services_ticket_view', args=[ticket.id]))

        else:
            form = TicketRecordForm(agent, ticket)
    else:
        form = None

    context.update({'ticket': ticket, 'record_form': form})

    return render_to_response('services/ticket_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def ticket_edit(request, ticket_id, response_format='html'):
    "Ticket edit"

    context = _get_default_context(request)
    agent = context['agent']

    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if not request.user.get_profile().has_permission(ticket, mode='w'):
        return user_denied(request, message="You don't have access to this Ticket")

    if request.POST:
        if not 'cancel' in request.POST:
            form = TicketForm(
                request.user.get_profile(), None, agent, request.POST, instance=ticket)
            if form.is_valid():
                ticket = form.save()
                return HttpResponseRedirect(reverse('services_ticket_view', args=[ticket.id]))
        else:
            return HttpResponseRedirect(reverse('services_ticket_view', args=[ticket.id]))
    else:
        form = TicketForm(
            request.user.get_profile(), None, agent, instance=ticket)

    context.update({'form': form,
                    'ticket': ticket})

    return render_to_response('services/ticket_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def ticket_set_status(request, ticket_id, status_id, response_format='html'):
    "Ticket quick set: Status"
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if not request.user.get_profile().has_permission(ticket, mode='w'):
        return user_denied(request, message="You don't have access to this Ticket")

    status = get_object_or_404(TicketStatus, pk=status_id)
    if not request.user.get_profile().has_permission(status):
        return user_denied(request, message="You don't have access to this Ticket Status")

    if not ticket.status == status:
        ticket.status = status
        ticket.save()

    return ticket_view(request, ticket_id, response_format)


@handle_response_format
@treeio_login_required
def ticket_delete(request, ticket_id, response_format='html'):
    "Ticket delete"

    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if not request.user.get_profile().has_permission(ticket, mode='w'):
        return user_denied(request, message="You don't have access to this Ticket")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                ticket.trash = True
                ticket.save()
            else:
                ticket.delete()
            return HttpResponseRedirect(reverse('services_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('services_ticket_view', args=[ticket.id]))

    context = _get_default_context(request)
    context.update({'ticket': ticket})

    return render_to_response('services/ticket_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def ticket_add(request, queue_id=None, response_format='html'):
    "Ticket add"

    context = _get_default_context(request)
    agent = context['agent']
    profile = request.user.get_profile()

    queue = None
    if queue_id:
        queue = get_object_or_404(TicketQueue, pk=queue_id)
        if not profile.has_permission(queue, mode='x'):
            queue = None

    if request.POST:
        if not 'cancel' in request.POST:
            ticket = Ticket(creator=profile)
            if not agent:
                if queue:
                    ticket.queue = queue
                    if queue.default_ticket_status:
                        ticket.status = queue.default_ticket_status
                    else:
                        try:
                            conf = ModuleSetting.get_for_module(
                                'treeio.services', 'default_ticket_status')[0]
                            ticket.status = TicketStatus.objects.get(
                                pk=long(conf.value))
                        except:
                            if 'statuses' in context:
                                try:
                                    ticket.status = context['statuses'][0]
                                except:
                                    pass
                    ticket.priority = queue.default_ticket_priority
                    ticket.service = queue.default_service
                else:
                    try:
                        conf = ModuleSetting.get_for_module(
                            'treeio.services', 'default_ticket_status')[0]
                        ticket.status = TicketStatus.objects.get(
                            pk=long(conf.value))
                    except:
                        if 'statuses' in context:
                            try:
                                ticket.status = context['statuses'][0]
                            except:
                                pass
                    try:
                        conf = ModuleSetting.get_for_module(
                            'treeio.services', 'default_ticket_queue')[0]
                        ticket.queue = TicketQueue.objects.get(
                            pk=long(conf.value))
                    except:
                        if 'queues' in context:
                            try:
                                ticket.queue = context['queues'][0]
                            except:
                                pass
                try:
                    ticket.caller = profile.get_contact()
                except:
                    pass
            form = TicketForm(
                profile, queue, agent, request.POST, instance=ticket)
            if form.is_valid():
                ticket = form.save()
                ticket.set_user_from_request(request)
                return HttpResponseRedirect(reverse('services_ticket_view', args=[ticket.id]))
        else:
            return HttpResponseRedirect(reverse('services'))
    else:
        form = TicketForm(request.user.get_profile(), queue, agent)

    context.update({'form': form, 'queue': queue})

    return render_to_response('services/ticket_add', context,
                              context_instance=RequestContext(request), response_format=response_format)

#
# Services
#


@handle_response_format
@treeio_login_required
def service_catalogue(request, response_format='html'):
    "All available Services"

    services = Object.filter_by_request(
        request, Service.objects.filter(parent__isnull=True))

    filters = FilterForm(request.user.get_profile(), '', request.GET)

    context = _get_default_context(request)
    context.update({'services': services, 'filters': filters})

    return render_to_response('services/service_catalogue', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def service_view(request, service_id, response_format='html'):
    "Service view"

    service = get_object_or_404(Service, pk=service_id)
    if not request.user.get_profile().has_permission(service) \
            and not request.user.get_profile().is_admin('treeio_services'):
        return user_denied(request, message="You don't have access to this Service")

    context = _get_default_context(request)
    context.update({'service': service})

    return render_to_response('services/service_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def service_edit(request, service_id, response_format='html'):
    "Service edit"

    service = get_object_or_404(Service, pk=service_id)
    if not request.user.get_profile().has_permission(service, mode='w') \
            and not request.user.get_profile().is_admin('treeio_services'):
        return user_denied(request, message="You don't have access to this Service")

    if request.POST:
        if not 'cancel' in request.POST:
            form = ServiceForm(
                request.user.get_profile(), request.POST, instance=service)
            if form.is_valid():
                service = form.save()
                return HttpResponseRedirect(reverse('services_service_view', args=[service.id]))
        else:
            return HttpResponseRedirect(reverse('services_service_view', args=[service.id]))
    else:
        form = ServiceForm(request.user.get_profile(), instance=service)

    context = _get_default_context(request)
    context.update({'form': form, 'service': service})

    return render_to_response('services/service_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def service_delete(request, service_id, response_format='html'):
    "Service delete"

    service = get_object_or_404(Service, pk=service_id)
    if not request.user.get_profile().has_permission(service, mode='w') \
            and not request.user.get_profile().is_admin('treeio_services'):
        return user_denied(request, message="You don't have access to this Service")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                service.trash = True
                service.save()
            else:
                service.delete()
            return HttpResponseRedirect(reverse('services_service_catalogue'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('services_service_view', args=[service.id]))

    context = _get_default_context(request)
    context.update({'service': service})

    return render_to_response('services/service_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def service_add(request, response_format='html'):
    "Service add"

    if not request.user.get_profile().is_admin('treeio.services'):
        return user_denied(request,
                           message="You don't have administrator access to the Service Support module")

    if request.POST:
        if not 'cancel' in request.POST:
            service = Service()
            form = ServiceForm(
                request.user.get_profile(), request.POST, instance=service)
            if form.is_valid():
                service = form.save()
                service.set_user_from_request(request)
                return HttpResponseRedirect(reverse('services_service_view', args=[service.id]))
        else:
            return HttpResponseRedirect(reverse('services'))
    else:
        form = ServiceForm(request.user.get_profile())

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('services/service_add', context,
                              context_instance=RequestContext(request), response_format=response_format)


#
# ServiceLevelAgreements
#

@handle_response_format
@treeio_login_required
def sla_index(request, response_format='html'):
    "All available Service Level Agreements"

    if request.GET:
        query = _get_filter_query(request.GET, ServiceLevelAgreement)
        slas = Object.filter_by_request(request,
                                        ServiceLevelAgreement.objects.filter(query))
    else:
        slas = Object.filter_by_request(request,
                                        ServiceLevelAgreement.objects)

    filters = SLAFilterForm(request.user.get_profile(), '', request.GET)

    context = _get_default_context(request)
    context.update({'slas': slas, 'filters': filters})

    return render_to_response('services/sla_index', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def sla_view(request, sla_id, response_format='html'):
    "ServiceLevelAgreement view"

    sla = get_object_or_404(ServiceLevelAgreement, pk=sla_id)
    if not request.user.get_profile().has_permission(sla):
        return user_denied(request, message="You don't have access to this Service Level Agreement")

    context = _get_default_context(request)
    context.update({'sla': sla})

    return render_to_response('services/sla_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def sla_edit(request, sla_id, response_format='html'):
    "ServiceLevelAgreement edit"

    sla = get_object_or_404(ServiceLevelAgreement, pk=sla_id)
    if not request.user.get_profile().has_permission(sla, mode='w'):
        return user_denied(request, message="You don't have access to this Service Level Agreement")

    if request.POST:
        if not 'cancel' in request.POST:
            form = ServiceLevelAgreementForm(
                request.user.get_profile(), request.POST, instance=sla)
            if form.is_valid():
                sla = form.save()
                return HttpResponseRedirect(reverse('services_sla_view', args=[sla.id]))
        else:
            return HttpResponseRedirect(reverse('services_sla_view', args=[sla.id]))
    else:
        form = ServiceLevelAgreementForm(
            request.user.get_profile(), instance=sla)

    context = _get_default_context(request)
    context.update({'sla': sla, 'form': form})

    return render_to_response('services/sla_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def sla_delete(request, sla_id, response_format='html'):
    "ServiceLevelAgreement delete"

    sla = get_object_or_404(ServiceLevelAgreement, pk=sla_id)
    if not request.user.get_profile().has_permission(sla, mode='w'):
        return user_denied(request, message="You don't have access to this Service Level Agreement")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                sla.trash = True
                sla.save()
            else:
                sla.delete()
            return HttpResponseRedirect(reverse('services_sla_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('services_sla_view', args=[sla.id]))

    context = _get_default_context(request)
    context.update({'sla': sla})

    return render_to_response('services/sla_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def sla_add(request, response_format='html'):
    "ServiceLevelAgreement add"

    if not request.user.get_profile().is_admin('treeio.services'):
        return user_denied(request,
                           message="You don't have administrator access to the Service Support module")

    if request.POST:
        if not 'cancel' in request.POST:
            sla = ServiceLevelAgreement()
            form = ServiceLevelAgreementForm(
                request.user.get_profile(), request.POST, instance=sla)
            if form.is_valid():
                sla = form.save()
                sla.set_user_from_request(request)
                return HttpResponseRedirect(reverse('services_sla_view', args=[sla.id]))
        else:
            return HttpResponseRedirect(reverse('services'))
    else:
        form = ServiceLevelAgreementForm(request.user.get_profile())

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('services/sla_add', context,
                              context_instance=RequestContext(request), response_format=response_format)


#
# Settings
#
@handle_response_format
@treeio_login_required
def settings_view(request, response_format='html'):
    "Settings"

    if not request.user.get_profile().is_admin('treeio.services'):
        return user_denied(request,
                           message="You don't have administrator access to the Service Support module")

    # default ticket status
    try:
        conf = ModuleSetting.get_for_module(
            'treeio.services', 'default_ticket_status')[0]
        default_ticket_status = TicketStatus.objects.get(pk=long(conf.value))
    except Exception:
        default_ticket_status = None

    # default queue
    try:
        conf = ModuleSetting.get_for_module(
            'treeio.services', 'default_ticket_queue')[0]
        default_ticket_queue = TicketQueue.objects.get(pk=long(conf.value))
    except Exception:
        default_ticket_queue = None

    # notify ticket caller by email
    try:
        conf = ModuleSetting.get_for_module(
            'treeio.services', 'send_email_to_caller')[0]
        send_email_to_caller = conf.value
    except Exception:
        send_email_to_caller = settings.HARDTREE_SEND_EMAIL_TO_CALLER

    # notification template
    send_email_example = ''
    try:
        conf = ModuleSetting.get_for_module(
            'treeio.services', 'send_email_template')[0]
        send_email_template = conf.value
    except Exception:
        send_email_template = None

    queues = TicketQueue.objects.filter(trash=False, parent__isnull=True)
    statuses = TicketStatus.objects.filter(trash=False)

    if send_email_to_caller:
        # Render example e-mail
        try:
            ticket = Object.filter_by_request(
                request, Ticket.objects.filter(status__hidden=False, caller__isnull=False))[0]
        except IndexError:
            ticket = Ticket(reference='REF123', name='New request')
        if not ticket.caller:
            try:
                caller = Object.filter_by_request(request, Contact.objects)[0]
            except IndexError:
                caller = Contact(name='John Smith')
            ticket.caller = caller
        try:
            ticket.status
        except:
            try:
                ticket.status = statuses[0]
            except IndexError:
                ticket.status = TicketStatus(name='Open')
        if send_email_template:
            try:
                send_email_example = render_string_template(
                    send_email_template, {'ticket': ticket})
            except:
                send_email_example = render_to_string(
                    'services/emails/notify_caller', {'ticket': ticket}, response_format='html')
        else:
            send_email_example = render_to_string(
                'services/emails/notify_caller', {'ticket': ticket}, response_format='html')

    context = _get_default_context(request)
    context.update({'settings_queues': queues,
                    'settings_statuses': statuses,
                    'default_ticket_status': default_ticket_status,
                    'default_ticket_queue': default_ticket_queue,
                    'send_email_to_caller': send_email_to_caller,
                    'send_email_example': send_email_example})

    return render_to_response('services/settings_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def settings_edit(request, response_format='html'):
    "Settings"

    if not request.user.get_profile().is_admin('treeio.services'):
        return user_denied(request,
                           message="You don't have administrator access to the Service Support module")

    if request.POST:
        if not 'cancel' in request.POST:
            form = SettingsForm(request.user.get_profile(), request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('services_settings_view'))
        else:
            return HttpResponseRedirect(reverse('services_settings_view'))
    else:
        form = SettingsForm(request.user.get_profile())

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('services/settings_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)

#
# Agents
#


@handle_response_format
@treeio_login_required
def agent_index(request, response_format='html'):
    "All available Agents"

    if not request.user.get_profile().is_admin('treeio.services'):
        return user_denied(request,
                           message="You don't have administrator access to the Service Support module")

    if request.GET:
        query = _get_filter_query(request.GET, ServiceAgent)
        agents = Object.filter_by_request(request,
                                          ServiceAgent.objects.filter(query))
    else:
        agents = Object.filter_by_request(request,
                                          ServiceAgent.objects)

    filters = AgentFilterForm(request.user.get_profile(), '', request.GET)

    context = _get_default_context(request)
    context.update({'agents': agents, 'filters': filters})

    return render_to_response('services/agent_index', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def agent_view(request, agent_id, response_format='html'):
    "Agent view"

    view_agent = get_object_or_404(ServiceAgent, pk=agent_id)
    if not request.user.get_profile().has_permission(view_agent):
        return user_denied(request, message="You don't have access to this Service Agent")

    context = _get_default_context(request)
    context.update({'view_agent': view_agent})

    return render_to_response('services/agent_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def agent_edit(request, agent_id, response_format='html'):
    "Agent edit"

    view_agent = get_object_or_404(ServiceAgent, pk=agent_id)
    if not request.user.get_profile().has_permission(view_agent):
        return user_denied(request, message="You don't have access to this Service Agent")

    if request.POST:
        if not 'cancel' in request.POST:
            form = AgentForm(
                request.user.get_profile(), request.POST, instance=view_agent)
            if form.is_valid():
                view_agent = form.save()
                return HttpResponseRedirect(reverse('services_agent_view', args=[view_agent.id]))
        else:
            return HttpResponseRedirect(reverse('services_agent_view', args=[view_agent.id]))
    else:
        form = AgentForm(request.user.get_profile(), instance=view_agent)

    context = _get_default_context(request)
    context.update({'form': form, 'view_agent': view_agent})

    return render_to_response('services/agent_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def agent_delete(request, agent_id, response_format='html'):
    "Agent delete"

    view_agent = get_object_or_404(ServiceAgent, pk=agent_id)
    if not request.user.get_profile().has_permission(view_agent, mode='w'):
        return user_denied(request, message="You don't have access to this Service Agent")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                view_agent.trash = True
                view_agent.save()
            else:
                view_agent.delete()
            return HttpResponseRedirect(reverse('services_agent_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('services_agent_view', args=[view_agent.id]))

    context = _get_default_context(request)
    context.update({'view_agent': view_agent})

    return render_to_response('services/agent_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def agent_add(request, response_format='html'):
    "Agent add"

    if not request.user.get_profile().is_admin('treeio.services'):
        return user_denied(request,
                           message="You don't have administrator access to the Service Support module")

    if request.POST:
        if not 'cancel' in request.POST:
            new_agent = ServiceAgent()
            form = AgentForm(
                request.user.get_profile(), request.POST, instance=new_agent)
            if form.is_valid():
                new_agent = form.save()
                new_agent.set_user_from_request(request)
                return HttpResponseRedirect(reverse('services_agent_view', args=[new_agent.id]))
        else:
            return HttpResponseRedirect(reverse('services_agent_index'))
    else:
        form = AgentForm(request.user.get_profile())

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('services/agent_add', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
def widget_index(request, response_format='html'):
    "All Active Tickets"

    tickets = Object.filter_by_request(
        request, Ticket.objects.filter(status__hidden=False))

    context = _get_default_context(request)
    context.update({'tickets': tickets})

    return render_to_response('services/widgets/index', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@treeio_login_required
def widget_index_assigned(request, response_format='html'):
    "Tickets assigned to current user"

    context = _get_default_context(request)
    agent = context['agent']

    if agent:
        tickets = Object.filter_by_request(request, Ticket.objects.filter(assigned=agent,
                                                                          status__hidden=False))
    else:
        return user_denied(request, "You are not a Service Support Agent.")

    context.update({'tickets': tickets})

    return render_to_response('services/widgets/index_assigned', context,
                              context_instance=RequestContext(request), response_format=response_format)


#
# AJAX lookups
#
@treeio_login_required
def ajax_ticket_lookup(request, response_format='html'):
    "Returns a list of matching tickets"

    tickets = []
    if request.GET and 'term' in request.GET:
        tickets = Ticket.objects.filter(
            name__icontains=request.GET['term'])[:10]

    return render_to_response('services/ajax_ticket_lookup',
                              {'tickets': tickets},
                              context_instance=RequestContext(request),
                              response_format=response_format)


@treeio_login_required
def ajax_agent_lookup(request, response_format='html'):
    "Returns a list of matching agents"

    agents = []
    if request.GET and 'term' in request.GET:
        agents = ServiceAgent.objects.filter(Q(related_user__name__icontains=request.GET['term']) |
                                             Q(related_user__contact__name__icontains=request.GET['term']))

    return render_to_response('services/ajax_agent_lookup',
                              {'agents': agents},
                              context_instance=RequestContext(request),
                              response_format=response_format)
