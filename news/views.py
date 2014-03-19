# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
News module: views
"""
from django.shortcuts import Http404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.db.models import Q
from treeio.core.models import UpdateRecord, Module, Object, Widget
from treeio.core.rendering import render_to_response
from treeio.core.decorators import treeio_login_required, handle_response_format
from treeio.news.forms import UpdateRecordForm, UpdateRecordFilterForm
from treeio.core.rss import ObjectFeed


def _get_default_context(request):
    "Preprocess context"

    query = Q(name__icontains='account') | Q(name__icontains='news')
    modules = request.user.get_profile(
    ).get_perspective().get_modules().exclude(query)
    filters = UpdateRecordFilterForm(request.user.get_profile(), request.GET)

    context = {'modules': modules, 'filters': filters}

    return context


def _get_filter_query(user, do_permissions=True, do_recipients=True, filters={}):

    is_admin = user.is_admin()
    query = Q()

    for arg in filters:
        if hasattr(UpdateRecord, arg) and filters[arg]:
            kwargs = {str(arg + '__id'): long(filters[arg])}
            query = query & Q(**kwargs)

    if do_permissions and not is_admin:
        query = Q(about__isnull=True) | Q(about__full_access=user) | Q(
            about__full_access__isnull=True)
        query = query | Q(about__full_access=user.default_group) | Q(
            about__full_access__in=user.other_groups.all())
        query = query | Q(about__read_access=user)
        query = query | Q(about__read_access=user.default_group) | Q(
            about__read_access__in=user.other_groups.all())
        modules = Object.filter_permitted(
            user, user.get_perspective().get_modules())
        if not len(modules) == Module.objects.all().count():
            modquery = Q()
            for module in modules:
                modquery = modquery | Q(
                    about__object_type__contains=module.name)
            query = query & modquery

    if do_recipients:
        if not is_admin:
            query = query & ((~Q(author=user) | Q(record_type='share')) & (Q(recipients=user) |
                                                                           Q(recipients__isnull=True) | Q(recipients=user.default_group) |
                                                                           Q(recipients__in=user.other_groups.all())))
        else:
            query = query & (Q(record_type='share') | (~Q(author=user) & (Q(recipients=user) |
                                                                          Q(recipients__isnull=True) | Q(recipients=user.default_group) | Q(recipients__in=user.other_groups.all()))))

    return query


@handle_response_format
@treeio_login_required
def index(request, response_format='html'):
    "Default index page"

    profile = request.user.get_profile()
    query = _get_filter_query(profile, filters=request.GET)
    updates = UpdateRecord.objects.filter(query).distinct()

    if request.POST:
        record = UpdateRecord()
        record.record_type = 'share'
        form = UpdateRecordForm(request.POST, user=profile, instance=record)
        if form.is_valid():
            record = form.save()
            record.body = record.body.replace('\n', ' <br />')
            record.save()
            record.set_user_from_request(request)
            return HttpResponseRedirect(reverse('news_index'))
    else:
        form = UpdateRecordForm(user=profile)

    if response_format == 'rss':
        return ObjectFeed(title=_('All Activity'),
                          link=request.path,
                          description=_('Updates on activity in your Tree.io'),
                          objects=updates)(request)

    context = _get_default_context(request)
    context.update({'form': form,
                    'updates': updates,
                    'profile': profile})

    return render_to_response('news/index', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def index_social(request, response_format='html'):
    "Social Activity"

    profile = request.user.get_profile()
    query = _get_filter_query(
        profile, filters=request.GET) & Q(record_type='share')
    updates = UpdateRecord.objects.filter(query).distinct()

    if request.POST:
        record = UpdateRecord()
        record.record_type = 'share'
        form = UpdateRecordForm(request.POST, user=profile, instance=record)
        if form.is_valid():
            record = form.save()
            record.body = record.body.replace('\n', ' <br />')
            record.save()
            record.set_user_from_request(request)
            return HttpResponseRedirect(reverse('news_social'))
    else:
        form = UpdateRecordForm(user=profile)

    context = _get_default_context(request)
    context.update({'form': form,
                    'updates': updates,
                    'profile': profile})

    return render_to_response('news/social', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def top_news(request, response_format='html'):
    "Default index page - top news"

    profile = request.user.get_profile()
    query = _get_filter_query(profile, filters=request.GET) & Q(score__gt=0)
    updates = UpdateRecord.objects.filter(query).distinct()

    if request.POST:
        record = UpdateRecord()
        record.record_type = 'share'
        form = UpdateRecordForm(request.POST, user=profile, instance=record)
        if form.is_valid():
            record = form.save()
            record.body = record.body.replace('\n', ' <br />')
            record.save()
            record.set_user_from_request(request)
            return HttpResponseRedirect(reverse('news_index'))
    else:
        form = UpdateRecordForm(user=profile)

    if response_format == 'rss':
        return ObjectFeed(title=_('Top News'),
                          link=request.path,
                          description=_('Updates on activity in your Tree.io'),
                          objects=updates)(request)

    context = _get_default_context(request)
    context.update({'form': form,
                    'updates': updates,
                    'profile': profile})

    return render_to_response('news/top_news', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def my_watchlist(request, response_format='html'):
    "Displays news about all objects a User is subscribed to"

    profile = request.user.get_profile()
    query = _get_filter_query(profile, do_recipients=False, filters=request.GET) & Q(
        about__in=profile.subscriptions.all()) & ~Q(author=profile)
    updates = UpdateRecord.objects.filter(query).distinct()

    if request.POST:
        record = UpdateRecord()
        record.record_type = 'share'
        form = UpdateRecordForm(request.POST, user=profile, instance=record)
        if form.is_valid():
            record = form.save(commit=False)
            record.body = record.body.replace('\n', ' <br />')
            record.save()
            record.set_user_from_request(request)
            return HttpResponseRedirect(reverse('news_index'))
    else:
        form = UpdateRecordForm(user=profile)

    if response_format == 'rss':
        return ObjectFeed(title=_('My Watchlist'),
                          link=request.path,
                          description=_(
                              'Updates on your watchlist in Tree.io'),
                          objects=updates)(request)

    context = _get_default_context(request)
    context.update({'form': form,
                    'updates': updates,
                    'profile': profile})

    return render_to_response('news/my_watchlist', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def my_activity(request, response_format='html'):
    "Default index page"

    profile = request.user.get_profile()
    updates = UpdateRecord.objects.filter(author=profile).distinct()

    if request.POST:
        record = UpdateRecord()
        record.record_type = 'share'
        form = UpdateRecordForm(request.POST, user=profile, instance=record)
        if form.is_valid():
            record = form.save(commit=False)
            record.body = record.body.replace('\n', ' <br />')
            record.save()
            record.set_user_from_request(request)
            return HttpResponseRedirect(reverse('news_my_activity'))
    else:
        form = UpdateRecordForm(user=profile)

    if response_format == 'rss':
        return ObjectFeed(title=_('My Activity'),
                          link=request.path,
                          description=_('Updates on activity in your Tree.io'),
                          objects=updates)(request)

    context = _get_default_context(request)
    context.update({'form': form,
                    'updates': updates,
                    'profile': profile})

    return render_to_response('news/my_activity', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def index_by_module(request, module_name, response_format='html'):
    "Default index page"

    profile = request.user.get_profile()
    try:
        module = profile.get_perspective().get_modules().filter(
            name__icontains=module_name)[0]
    except:
        raise Http404('No such module in your Perspective')
    query = _get_filter_query(profile, filters=request.GET) & Q(
        about__object_type__icontains=module_name) & (~Q(author=profile) | Q(score__gt=0))
    updates = UpdateRecord.objects.filter(query).distinct()

    if request.POST:
        record = UpdateRecord()
        record.record_type = 'share'
        form = UpdateRecordForm(request.POST, user=profile, instance=record)
        if form.is_valid():
            record = form.save()
            record.body = record.body.replace('\n', ' <br />')
            record.save()
            record.set_user_from_request(request)
            return HttpResponseRedirect(reverse('news_index_by_module', filters=[module_name]))
    else:
        form = UpdateRecordForm(user=profile)

    if response_format == 'rss':
        return ObjectFeed(title=(_(module.title) + ' ' + _('Activity')),
                          link=request.path,
                          description=_('Updates on activity in your Tree.io'),
                          objects=updates)(request)

    context = _get_default_context(request)
    context.update({'form': form,
                    'active_module': module,
                    'updates': updates,
                    'profile': profile,
                    'module_name': module_name})

    return render_to_response('news/index_by_module', context,
                              context_instance=RequestContext(request), response_format=response_format)

#
# Widgets
#


@handle_response_format
@treeio_login_required
def widget_news_index(request, response_format='html'):
    "Widget: All Activity"

    profile = request.user.get_profile()
    query = _get_filter_query(profile) & (
        ~Q(author=profile) | Q(record_type='share') | Q(score__gt=0))
    updates = UpdateRecord.objects.filter(query).distinct()

    # don't do updates if social widget is used
    if Widget.objects.filter(user=profile, widget_name='widget_news_social').exists():
        form = None

    else:
        if request.POST:
            record = UpdateRecord()
            record.record_type = 'share'
            form = UpdateRecordForm(
                request.POST, user=profile, instance=record)
            if form.is_valid():
                record = form.save()
                record.body = record.body.replace('\n', ' <br />')
                record.save()
                record.set_user_from_request(request)
                return HttpResponseRedirect(reverse('core_dashboard_index'))
        else:
            form = UpdateRecordForm(user=profile)

    context = _get_default_context(request)
    context.update({'form': form,
                    'updates': updates,
                    'profile': profile})

    return render_to_response('news/widgets/index', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def widget_news_social(request, response_format='html'):
    "Widget: Social Activity"

    profile = request.user.get_profile()
    query = _get_filter_query(profile) & Q(record_type='share')
    updates = UpdateRecord.objects.filter(query).distinct()

    if request.POST:
        record = UpdateRecord()
        record.record_type = 'share'
        form = UpdateRecordForm(request.POST, user=profile, instance=record)
        if form.is_valid():
            record = form.save()
            record.body = record.body.replace('\n', ' <br />')
            record.save()
            record.set_user_from_request(request)
            return HttpResponseRedirect(reverse('core_dashboard_index'))
    else:
        form = UpdateRecordForm(user=profile)

    context = _get_default_context(request)
    context.update({'form': form,
                    'updates': updates,
                    'profile': profile})

    return render_to_response('news/widgets/social', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def widget_my_watchlist(request, response_format='html'):
    "Displays news about all objects a User is subscribed to"

    profile = request.user.get_profile()
    query = _get_filter_query(profile, do_recipients=False) & Q(
        about__in=profile.subscriptions.all()) & ~Q(author=profile)
    updates = UpdateRecord.objects.filter(query).distinct()

    context = _get_default_context(request)
    context.update({'updates': updates,
                    'profile': profile})

    return render_to_response('news/widgets/my_watchlist', context,
                              context_instance=RequestContext(request), response_format=response_format)
