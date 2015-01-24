# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Events module views
"""
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.db.models import Q
from treeio.core.rendering import render_to_response
from treeio.core.models import Object
from treeio.core.views import user_denied
from treeio.core.decorators import treeio_login_required, handle_response_format
from treeio.events.models import Event
from treeio.events.forms import EventForm, GoToDateForm, FilterForm, MassActionForm
from treeio.events.rendering import EventCollection
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar

START_HOUR = 6
END_HOUR = 23


def _get_default_context(request):
    "Returns default context as a dict()"

    massform = MassActionForm(request.user.get_profile())

    context = {'massform': massform}

    return context


def _get_filter_query(args):
    "Creates a query to filter Events based on FilterForm arguments"
    query = Q()

    if 'datefrom' in args and 'dateto' in args and args['datefrom'] and args['dateto']:
        datefrom = datetime.date(
            datetime.strptime(args['datefrom'], '%m/%d/%Y'))
        dateto = datetime.date(datetime.strptime(args['dateto'], '%m/%d/%Y'))
        dateto = datetime(year=dateto.year, month=dateto.month,
                          day=dateto.day, hour=23, minute=59, second=59)
        query = Q(end__gte=datefrom)
        query = query & Q(Q(start__isnull=True) | Q(start__lte=dateto))

    return query


def _process_mass_form(f):
    "Pre-process request to handle mass action form for Events"

    def wrap(request, *args, **kwargs):
        "Wrap"
        user = request.user.get_profile()
        if 'massform' in request.POST:
            for key in request.POST:
                if 'mass-event' in key:
                    try:
                        event = Event.objects.get(pk=request.POST[key])
                        form = MassActionForm(
                            user, request.POST, instance=event)
                        if form.is_valid() and user.has_permission(event, mode='w'):
                            form.save()
                    except Exception:
                        pass

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__

    return wrap


@treeio_login_required
@handle_response_format
@_process_mass_form
def index(request, response_format='html'):
    "Index page: display all events"

    if request.GET:
        filters = FilterForm(request.GET)
        if filters.is_valid():
            query = _get_filter_query(request.GET)
        else:
            query = Q()
    else:
        query = Q()
        filters = FilterForm()

    events = Object.filter_by_request(request, Event.objects.filter(query))

    context = _get_default_context(request)
    context.update({'events': events,
                    'filters': filters})

    return render_to_response('events/index', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
@_process_mass_form
def upcoming(request, response_format='html'):
    "Upcoming Events"

    now = datetime.now()
    query = Q(start__gte=now) | Q(end__gte=now)
    events = Object.filter_by_request(
        request, Event.objects.filter(query).order_by('-end'))

    context = _get_default_context(request)
    context.update({'events': events})

    return render_to_response('events/upcoming', context,
                              context_instance=RequestContext(request), response_format=response_format)
#
# Calendar View
#


@treeio_login_required
@handle_response_format
def month_view(request, response_format='html'):
    "Month view - each cell represents a day"

    events = Object.filter_by_request(request, Event.objects)

    date_current = now = datetime.now()
    istoday = True

    gotoform = GoToDateForm(now, request.GET)
    if request.GET:
        if 'date_year' in request.GET and 'date_month' in request.GET:
            try:
                year = int(request.GET['date_year'])
                month = int(request.GET['date_month'])
                if year >= 1900 and month >= 1 and month <= 12:
                    date_current = datetime(year, month, 1)
                    istoday = date_current == now
            except Exception:
                pass
        if gotoform.is_valid() and gotoform.cleaned_data['goto']:
            date_current = gotoform.cleaned_data['goto']
            istoday = date_current == now
            now = datetime(
                date_current.year, date_current.month, date_current.day)

    dates = calendar.Calendar().monthdatescalendar(
        date_current.year, date_current.month)
    date_previous = date_current - relativedelta(months=+1)
    date_next = date_current + relativedelta(months=+1)

    wrapped_events = EventCollection(events)
    wrapped_events.collect_events(request)

    return render_to_response('events/month_view',
                              {'events': wrapped_events,
                               'dates': dates,
                               'date_previous': date_previous,
                               'date_next': date_next,
                               'date_current': date_current,
                               'gotoform': gotoform.as_ul(),
                               'istoday': istoday,
                               'now': now},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def week_view(request, response_format='html'):
    "Week view - each slot represents an hour"

    events = Object.filter_by_request(request, Event.objects)

    date_current = now = datetime.now()
    istoday = True

    gotoform = GoToDateForm(now, request.GET)
    if request.GET:
        if 'date_year' in request.GET and 'date_month' in request.GET and 'date_day' in request.GET:
            try:
                day = int(request.GET['date_day'])
                year = int(request.GET['date_year'])
                month = int(request.GET['date_month'])
                if year >= 1900 and month >= 1 and month <= 12 and day >= 1 and day <= 31:
                    date_current = datetime(year, month, day)
                    istoday = date_current == now
            except Exception:
                pass
        if gotoform.is_valid() and gotoform.cleaned_data['goto']:
            date_current = gotoform.cleaned_data['goto']
            istoday = date_current == now
            date_current = now = datetime(
                date_current.year, date_current.month, date_current.day)

    date_previous = date_current - relativedelta(weeks=+1)
    date_next = date_current + relativedelta(weeks=+1)

    weeks = calendar.Calendar().monthdatescalendar(
        date_current.year, date_current.month)
    current_week = []
    for week in weeks:
        if date_current.date() in week:
            current_week = week
            break

    wrapped_events = EventCollection(events, START_HOUR, END_HOUR)
    wrapped_events.collect_events(request)

    hours = range(START_HOUR, END_HOUR + 1)

    return render_to_response('events/week_view',
                              {'events': wrapped_events,
                               'week': current_week,
                               'start_date': current_week[0],
                               'end_date': current_week[6],
                               'date_previous': date_previous,
                               'date_next': date_next,
                               'date_current': date_current,
                               'gotoform': gotoform.as_ul(),
                               'istoday': istoday,
                               'hours': hours,
                               'now': now},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def day_view(request, response_format='html'):
    "Day view - each slot represents an hour"

    events = Object.filter_by_request(request, Event.objects)

    date_current = now = datetime.now()
    istoday = True

    gotoform = GoToDateForm(now, request.GET)
    if request.GET:
        if 'date_year' in request.GET and 'date_month' in request.GET and 'date_day' in request.GET:
            try:
                day = int(request.GET['date_day'])
                year = int(request.GET['date_year'])
                month = int(request.GET['date_month'])
                if year >= 1900 and month >= 1 and month <= 12 and day >= 1 and day <= 31:
                    date_current = datetime(year, month, day)
                    istoday = date_current == now
            except Exception:
                pass
        if gotoform.is_valid() and gotoform.cleaned_data['goto']:
            date_current = gotoform.cleaned_data['goto']
            istoday = date_current == now
            date_current = now = datetime(
                date_current.year, date_current.month, date_current.day)

    day = date_current.date()
    date_previous = date_current - relativedelta(days=+1)
    date_next = date_current + relativedelta(days=+1)

    wrapped_events = EventCollection(events, START_HOUR, END_HOUR)
    wrapped_events.collect_events(request)

    hours = range(START_HOUR, END_HOUR + 1)

    return render_to_response('events/day_view',
                              {'events': wrapped_events,
                               'day': day,
                               'hours': hours,
                               'date_previous': date_previous,
                               'date_next': date_next,
                               'date_current': date_current,
                               'gotoform': gotoform.as_ul(),
                               'istoday': istoday,
                               'now': now},
                              context_instance=RequestContext(request), response_format=response_format)

#
# Events
#


@treeio_login_required
@handle_response_format
def event_view(request, event_id, response_format='html'):
    "Event view"

    event = get_object_or_404(Event, pk=event_id)
    if not request.user.get_profile().has_permission(event):
        return user_denied(request, message="You don't have access to this Event")

    return render_to_response('events/event_view',
                              {'event': event},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def event_edit(request, event_id, response_format='html'):
    "Event edit"

    event = get_object_or_404(Event, pk=event_id)
    if not request.user.get_profile().has_permission(event, mode='w'):
        return user_denied(request, message="You don't have access to this Event")

    if request.POST:
        if not 'cancel' in request.POST:
            form = EventForm(
                request.user.get_profile(), None, None, request.POST, instance=event)
            if form.is_valid():
                event = form.save()
                return HttpResponseRedirect(reverse('events_event_view', args=[event.id]))
        else:
            return HttpResponseRedirect(reverse('events'))
    else:
        form = EventForm(request.user.get_profile(), instance=event)

    return render_to_response('events/event_edit',
                              {'event': event,
                               'form': form},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def event_delete(request, event_id, response_format='html'):
    "Event delete"

    event = get_object_or_404(Event, pk=event_id)
    if not request.user.get_profile().has_permission(event, mode='w'):
        return user_denied(request, message="You don't have access to this Event")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                event.trash = True
                event.save()
            else:
                event.delete()
            return HttpResponseRedirect(reverse('events_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('events_event_view', args=[event.id]))

    return render_to_response('events/event_delete',
                              {'event': event},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def event_add(request, date=None, hour=12, response_format='html'):
    "Event add form"

    if request.POST:
        if not 'cancel' in request.POST:
            event = Event()
            form = EventForm(
                request.user.get_profile(), date, hour, request.POST, instance=event)
            if form.is_valid():
                event = form.save()
                event.set_user_from_request(request)
                return HttpResponseRedirect(reverse('events_event_view', args=[event.id]))
        else:
            return HttpResponseRedirect(reverse('events'))
    else:
        form = EventForm(request.user.get_profile(), date, hour)

    return render_to_response('events/event_add',
                              {'form': form},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
def ical_all_event(request, response_format='ical'):
    "Export upcoming events "
    query = Q()
    events = Object.filter_by_request(request, Event.objects.filter(query))
    icalstream = """BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
PRODID:-//PYVOBJECT//NONSGML Version 1//EN
"""
    vevent = ""
    for event in events:
        vevent += "BEGIN:VEVENT\n"
        if event.start:
            vevent += "DTSTART;VALUE=DATE:%s\n" % str(
                (datetime.strptime(str(event.start)[0:10], '%Y-%m-%d')))[0:10].replace("-", "")
        vevent += "DTEND;VALUE=DATE:%s\n" % str(
            (datetime.strptime(str(event.end)[0:10], '%Y-%m-%d')))[0:10].replace("-", "")
        if not event.details:
            vevent += "SUMMARY:%s\n" % strip_tags(event.name)
        else:
            vevent += "SUMMARY:%s\n" % strip_tags(event.details)
        vevent += "UID:%s\n" % (event.name)
        vevent += "END:VEVENT\n"

    icalstream += vevent
    icalstream += """X-WR-CALDESC:Tree.io Calendar
X-WR-CALNAME:Tree.io
X-WR-TIMEZONE:London/UK
END:VCALENDAR
"""

    response = HttpResponse(icalstream, mimetype='text/calendar')
    response['Filename'] = 'events.ics'  # IE needs this
    response['Content-Disposition'] = 'attachment; filename=events.ics'
    return response


#
# Widgets
#

@handle_response_format
@treeio_login_required
def widget_week_view(request, response_format='html'):
    "Week view - each slot represents an hour"

    events = Object.filter_by_request(request, Event.objects)

    date_current = now = datetime.now()
    istoday = True

    gotoform = GoToDateForm(now, request.GET)
    if request.GET:
        if 'date_year' in request.GET and 'date_month' in request.GET and 'date_day' in request.GET:
            try:
                day = int(request.GET['date_day'])
                year = int(request.GET['date_year'])
                month = int(request.GET['date_month'])
                if year >= 1900 and month >= 1 and month <= 12 and day >= 1 and day <= 31:
                    date_current = datetime(year, month, day)
                    istoday = date_current == now
            except Exception:
                pass
        if gotoform.is_valid() and gotoform.cleaned_data['goto']:
            date_current = gotoform.cleaned_data['goto']
            istoday = date_current == now
            date_current = now = datetime(
                date_current.year, date_current.month, date_current.day)

    date_previous = date_current - relativedelta(weeks=+1)
    date_next = date_current + relativedelta(weeks=+1)

    weeks = calendar.Calendar().monthdatescalendar(
        date_current.year, date_current.month)
    current_week = []
    for week in weeks:
        if date_current.date() in week:
            current_week = week
            break

    wrapped_events = EventCollection(events, START_HOUR, END_HOUR)
    wrapped_events.collect_events(request)

    dates = calendar.Calendar().monthdatescalendar(
        date_current.year, date_current.month)

    wrapped_events = EventCollection(events)
    wrapped_events.collect_events(request)

    return render_to_response('events/widgets/week_view',
                              {'events': wrapped_events,
                               'dates': dates,
                               'week': current_week,
                               'date_previous': date_previous,
                               'date_next': date_next,
                               'start_date': current_week[0],
                               'end_date': current_week[6],
                               'date_current': date_current,
                               'gotoform': gotoform.as_ul(),
                               'istoday': istoday,
                               'now': now},
                              context_instance=RequestContext(request), response_format=response_format)
