# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core module: Trash views
"""
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from treeio.core.models import Object
from treeio.core.decorators import treeio_login_required, handle_response_format
from treeio.core.rendering import render_to_response
from treeio.core.views import user_denied
from treeio.core.trash.forms import MassActionForm


def _process_mass_form(f):
    "Pre-process request to handle mass action form for Tasks and Milestones"

    def wrap(request, *args, **kwargs):
        "Wrap"
        if 'massform' in request.POST:
            if 'delete_all' in request.POST.values():
                try:
                    object = Object.filter_by_request(request, manager=Object.objects.filter(trash=True),
                                                      mode='r', filter_trash=False)
                    form = MassActionForm(request.POST, instance=object)
                    if form.is_valid() and request.user.get_profile().has_permission(object, mode='w'):
                        form.save()
                except:
                    pass
            else:
                for key in request.POST:
                    if 'mass-object' in key:
                        try:
                            object = Object.objects.get(pk=request.POST[key])
                            form = MassActionForm(
                                request.POST, instance=object)
                            if form.is_valid() and request.user.get_profile().has_permission(object, mode='w'):
                                form.save()
                        except:
                            pass

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__

    return wrap


@treeio_login_required
@handle_response_format
@_process_mass_form
def index(request, response_format='html'):
    "List of items in Trash"

    trash = Object.filter_by_request(request, manager=Object.objects.filter(trash=True),
                                     mode='r', filter_trash=False)
    massform = MassActionForm()

    return render_to_response('core/trash/index',
                              {'trash': trash,
                               'massform': massform},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def object_delete(request, object_id, response_format='html'):
    "Completely delete item"

    object = get_object_or_404(Object, pk=object_id)
    if not request.user.get_profile().has_permission(object, mode='w'):
        return user_denied(request, message="You don't have access to this Object")

    if request.POST:
        if 'delete' in request.POST:
            object.delete()
            return HttpResponseRedirect(reverse('core_trash'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('core_trash'))

    return render_to_response('core/trash/object_delete',
                              {'object': object},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def object_untrash(request, object_id, response_format='html'):
    "Untrash item"

    object = get_object_or_404(Object, pk=object_id)
    if not request.user.get_profile().has_permission(object, mode='w'):
        return user_denied(request, message="You don't have access to this Object")

    related = object.get_related_object()
    if related:
        related.trash = False
        related.save()
    else:
        object.trash = False
        object.save()

    return HttpResponseRedirect(reverse('core_trash'))
