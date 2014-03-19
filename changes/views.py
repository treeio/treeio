# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Change Control module views
"""
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from treeio.core.models import Object, ModuleSetting
from treeio.core.rendering import render_to_response
from treeio.core.views import user_denied
from treeio.core.decorators import handle_response_format, treeio_login_required, module_admin_required
from treeio.changes.forms import ChangeSetForm, ChangeSetStatusForm, FilterForm, SettingsForm, \
    MassActionForm
from treeio.changes.models import ChangeSet, ChangeSetStatus


def _get_filter_query(args):
    "Creates a query to filter Documents and Tasks based on FilterForm arguments"
    query = Q()

    for arg in args:
        if hasattr(ChangeSet, arg) and args[arg]:
            kwargs = {str(arg + '__id'): long(args[arg])}
            query = query & Q(**kwargs)

    if not 'status' in args:
        query = query & Q(status__hidden=False)

    return query


def _get_default_context(request):
    "Returns Default context applicable to all views"

    all_statuses = Object.filter_by_request(request, ChangeSetStatus.objects)
    massform = MassActionForm(request.user.get_profile())

    context = {'all_statuses': all_statuses,
               'massform': massform}

    return context


def _process_mass_form(f):
    "Pre-process request to handle mass action form for Change Sets"

    def wrap(request, *args, **kwargs):
        "Wrap"
        user = request.user.get_profile()
        if 'massform' in request.POST:
            for key in request.POST:
                if 'mass-changeset' in key:
                    try:
                        changeset = ChangeSet.objects.get(pk=request.POST[key])
                        form = MassActionForm(
                            request.user.get_profile(), request.POST, instance=changeset)
                        if form.is_valid() and user.has_permission(changeset, mode='w'):
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
    "Change Control index page"

    query = Q(object__in=Object.filter_by_request(request, Object.objects))
    if request.GET:
        query = query & _get_filter_query(request.GET)
        filters = FilterForm(request.user.get_profile(), [], request.GET)
    else:
        query = query & Q(status__hidden=False)
        filters = FilterForm(request.user.get_profile())

    changesets = ChangeSet.objects.filter(query)

    context = _get_default_context(request)
    context.update({'changesets': changesets, 'filters': filters})

    return render_to_response('changes/index', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def index_owned(request, response_format='html'):
    "Change Control owned by me page"

    query = Q(object__in=Object.filter_by_request(request,
                                                  Object.objects)) & Q(author=request.user.get_profile())
    if request.GET:
        query = query & _get_filter_query(request.GET)
        filters = FilterForm(request.user.get_profile(), 'author', request.GET)
    else:
        query = query & Q(status__hidden=False)
        filters = FilterForm(request.user.get_profile(), 'author')

    changesets = ChangeSet.objects.filter(query)

    context = _get_default_context(request)
    context.update({'filters': filters,
                    'changesets': changesets})

    return render_to_response('changes/index_owned', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def index_resolved(request, response_format='html'):
    "Change Control resolved by me page"

    query = Q(object__in=Object.filter_by_request(request,
                                                  Object.objects)) & Q(resolved_by=request.user.get_profile())
    if request.GET:
        query = query & _get_filter_query(request.GET)
        filters = FilterForm(
            request.user.get_profile(), 'resolved_by', request.GET)
    else:
        filters = FilterForm(request.user.get_profile(), 'resolved_by')

    changesets = ChangeSet.objects.filter(query)

    context = _get_default_context(request)
    context.update({'filters': filters,
                    'changesets': changesets})

    return render_to_response('changes/index_resolved', context,
                              context_instance=RequestContext(request), response_format=response_format)

#
# ChangeSetStatus
#


@handle_response_format
@treeio_login_required
@_process_mass_form
def status_view(request, status_id, response_format='html'):
    "Status view"

    status = get_object_or_404(ChangeSetStatus, pk=status_id)

    if not request.user.get_profile().has_permission(status) \
            and not request.user.get_profile().is_admin('treeio.changes'):
        return user_denied(request, "You don't have access to this Change Set Status.",
                           response_format=response_format)

    query = Q(object__in=Object.filter_by_request(request, Object.objects)) & Q(
        status=status)
    if request.GET:
        query = query & _get_filter_query(request.GET)
        filters = FilterForm(request.user.get_profile(), 'status', request.GET)
    else:
        filters = FilterForm(request.user.get_profile(), 'status')

    changesets = ChangeSet.objects.filter(query)

    context = _get_default_context(request)
    context.update({'status': status,
                    'changesets': changesets,
                    'filters': filters})

    return render_to_response('changes/status_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
@module_admin_required('treeio.changes')
def status_edit(request, status_id, response_format='html'):
    "Status edit"

    status = get_object_or_404(ChangeSetStatus, pk=status_id)

    if request.POST:
        form = ChangeSetStatusForm(
            request.user.get_profile(), request.POST, instance=status)
        if form.is_valid():
            status = form.save()
            return HttpResponseRedirect(reverse('changes_status_view', args=[status.id]))
    else:
        form = ChangeSetStatusForm(request.user.get_profile(), instance=status)

    context = _get_default_context(request)
    context.update({'status': status, 'form': form})

    return render_to_response('changes/status_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
@module_admin_required('treeio.changes')
def status_delete(request, status_id, response_format='html'):
    "Status delete"

    status = get_object_or_404(ChangeSetStatus, pk=status_id)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                status.trash = True
                status.save()
            else:
                status.delete()
            return HttpResponseRedirect(reverse('changes_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('changes_status_view', args=[status.id]))

    context = _get_default_context(request)
    context.update({'status': status})

    return render_to_response('changes/status_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
@module_admin_required('treeio.changes')
def status_add(request, response_format='html'):
    "Status add"

    if request.POST:
        form = ChangeSetStatusForm(request.user.get_profile(), request.POST)
        if form.is_valid():
            status = form.save()
            return HttpResponseRedirect(reverse('changes_status_view', args=[status.id]))
    else:
        form = ChangeSetStatusForm(request.user.get_profile())

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('changes/status_add', context,
                              context_instance=RequestContext(request), response_format=response_format)


#
# ChangeSet
#
@handle_response_format
@treeio_login_required
def set_view(request, set_id, response_format='html'):
    "ChangeSet view"

    changeset = get_object_or_404(ChangeSet, pk=set_id)

    if not request.user.get_profile().has_permission(changeset.object) \
            and not request.user.get_profile().is_admin('treeio.changes'):
        return user_denied(request, "You don't have access to this Change Set.",
                           response_format=response_format)

    context = _get_default_context(request)
    context.update({'changeset': changeset})

    return render_to_response('changes/set_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def set_edit(request, set_id, response_format='html'):
    "ChangeSet edit"

    changeset = get_object_or_404(ChangeSet, pk=set_id)

    if not request.user.get_profile().has_permission(changeset.object, mode='w') \
            and not request.user.get_profile().is_admin('treeio.changes'):
        return user_denied(request, "You don't have access to this Change Set.",
                           response_format=response_format)

    if request.POST:
        form = ChangeSetForm(
            request.user.get_profile(), request.POST, instance=changeset)
        if form.is_valid():
            changeset = form.save()
            return HttpResponseRedirect(reverse('changes_set_view', args=[changeset.id]))
    else:
        form = ChangeSetForm(request.user.get_profile(), instance=changeset)

    context = _get_default_context(request)
    context.update({'changeset': changeset,
                    'form': form})

    return render_to_response('changes/set_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def set_delete(request, set_id, response_format='html'):
    "ChangeSet delete"

    changeset = get_object_or_404(ChangeSet, pk=set_id)

    if not request.user.get_profile().has_permission(changeset.object, mode='w') \
            and not request.user.get_profile().is_admin('treeio.changes'):
        return user_denied(request, "You don't have access to this Change Set.",
                           response_format=response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                changeset.trash = True
                changeset.save()
            else:
                changeset.delete()
            return HttpResponseRedirect(reverse('changes_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('changes_set_view', args=[changeset.id]))

    context = _get_default_context(request)
    context.update({'changeset': changeset})

    return render_to_response('changes/set_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def set_add(request, response_format='html'):
    "ChangeSet add"

    if request.POST:
        changeset = ChangeSet(author=request.user.get_profile())
        form = ChangeSetForm(
            request.user.get_profile(), request.POST, instance=changeset)
        if form.is_valid():
            set = form.save()
            return HttpResponseRedirect(reverse('changes_set_view', args=[set.id]))
    else:
        form = ChangeSetForm(request.user.get_profile())

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('changes/set_add', context,
                              context_instance=RequestContext(request), response_format=response_format)


#
# Settings
#
@handle_response_format
@treeio_login_required
@module_admin_required('treeio.changes')
def settings_view(request, response_format='html'):
    "Settings"

    # default changeset status
    try:
        conf = ModuleSetting.get_for_module(
            'treeio.changes', 'default_changeset_status')[0]
        default_changeset_status = ChangeSetStatus.objects.get(
            pk=long(conf.value))

    except Exception:
        default_changeset_status = None

    # check not trashed
    if default_changeset_status:
        if default_changeset_status.trash:
            default_changeset_status = None

    settings_statuses = ChangeSetStatus.objects.filter(trash=False)

    context = _get_default_context(request)
    context.update({'default_changeset_status': default_changeset_status,
                    'settings_statuses': settings_statuses})

    return render_to_response('changes/settings_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
@module_admin_required('treeio.changes')
def settings_edit(request, response_format='html'):
    "Settings"

    if request.POST:
        form = SettingsForm(request.user.get_profile(), request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('changes_settings_view'))
    else:
        form = SettingsForm(request.user.get_profile())

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('changes/settings_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)
