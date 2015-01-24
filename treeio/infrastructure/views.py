# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Infrastructure module views
"""
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from treeio.core.rendering import render_to_response
from treeio.infrastructure.models import Item, ItemField, ItemType, ItemStatus, ItemServicing
from treeio.infrastructure.forms import ItemForm, ItemTypeForm, ItemStatusForm, FilterForm, \
    MassActionForm, ItemFieldForm, ServiceRecordForm, SettingsForm
from treeio.core.forms import LocationForm
from treeio.core.models import Object, ModuleSetting, Location
from treeio.core.views import user_denied
from treeio.core.decorators import treeio_login_required, handle_response_format, module_admin_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q


def _get_filter_query(args, model=Item):
    "Creates a query to filter Items based on FilterForm arguments"
    query = Q()

    for arg in args:
        if hasattr(model, arg) and args[arg]:
            kwargs = {str(arg + '__id'): long(args[arg])}
            query = query & Q(**kwargs)

    return query


def _get_default_context(request):
    "Returns default context for all views as dict()"

    types = Object.filter_by_request(
        request, ItemType.objects.filter(parent__isnull=True))
    statuses = Object.filter_by_request(request, ItemStatus.objects)
    locations = Object.filter_by_request(request, Location.objects)
    massform = MassActionForm(request.user.get_profile())

    context = {
        'statuses': statuses,
        'types': types,
        'massform': massform,
        'locations': locations
    }

    return context


def _process_mass_form(f):
    "Pre-process request to handle mass action form for Tasks and Milestones"

    def wrap(request, *args, **kwargs):
        "Wrap"
        if 'massform' in request.POST:
            for key in request.POST:
                if 'mass-item' in key:
                    try:
                        item = Item.objects.get(pk=request.POST[key])
                        form = MassActionForm(
                            request.user.get_profile(), request.POST, instance=item)
                        if form.is_valid() and request.user.get_profile().has_permission(item, mode='w'):
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
    "Index page: displays all Items"

    query = Q(status__hidden=False)
    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = _get_filter_query(request.GET)
        else:
            query = query & _get_filter_query(request.GET)
    if request.GET:
        query = query & _get_filter_query(request.GET)

    items = Object.filter_by_request(
        request, Item.objects.filter(query).order_by('name'))

    filters = FilterForm(request.user.get_profile(), '', request.GET)

    context = _get_default_context(request)
    context.update({'items': items,
                    'filters': filters})

    return render_to_response('infrastructure/index', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
@_process_mass_form
def index_owned(request, response_format='html'):
    "Items owned by current user"

    query = Q(owner=request.user.get_profile().get_contact())
    if request.GET:
        query = query & _get_filter_query(request.GET)
    items = Object.filter_by_request(
        request, Item.objects.filter(query).order_by('-date_created'))

    filters = FilterForm(request.user.get_profile(), ['owner'], request.GET)

    context = _get_default_context(request)
    context.update({'items': items,
                    'filters': filters})

    return render_to_response('infrastructure/index_owned', context,
                              context_instance=RequestContext(request), response_format=response_format)

#
# ItemTypes
#


@treeio_login_required
@handle_response_format
@_process_mass_form
def type_view(request, type_id, response_format='html'):
    "ItemType view"

    item_type = get_object_or_404(ItemType, pk=type_id)
    if not request.user.get_profile().has_permission(item_type):
        return user_denied(request, message="You don't have access to this Item Type",
                           response_format=response_format)

    query = Q(item_type=item_type)
    if request.GET:
        query = query & _get_filter_query(request.GET)
    items = Object.filter_by_request(
        request, Item.objects.filter(query).order_by('name'))

    filters = FilterForm(
        request.user.get_profile(), ['item_type'], request.GET)

    context = _get_default_context(request)
    context.update({'items': items,
                    'filters': filters,
                    'item_type': item_type})

    return render_to_response('infrastructure/item_type_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def type_edit(request, type_id, response_format='html'):
    "ItemType edit"

    item_type = get_object_or_404(ItemType, pk=type_id)
    if not request.user.get_profile().has_permission(item_type, mode='w'):
        return user_denied(request, message="You don't have access to this Item Type",
                           response_format=response_format)
    infrastructure = Object.filter_by_request(request,
                                              Item.objects.filter(item_type=item_type).order_by('name'))

    if request.POST:
        if not 'cancel' in request.POST:
            form = ItemTypeForm(
                request.user.get_profile(), request.POST, instance=item_type)
            if form.is_valid():
                item_type = form.save(request)
                return HttpResponseRedirect(reverse('infrastructure_type_view', args=[item_type.id]))
        else:
            return HttpResponseRedirect(reverse('infrastructure_type_view', args=[item_type.id]))
    else:
        form = ItemTypeForm(request.user.get_profile(), instance=item_type)

    context = _get_default_context(request)
    context.update({'infrastructure': infrastructure,
                    'form': form,
                    'item_type': item_type})

    return render_to_response('infrastructure/item_type_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def type_add(request, response_format='html'):
    "ItemType add"

    if not request.user.get_profile().is_admin('treeio.infrastructure'):
        return user_denied(request, message="You don't have administrator access to the Infrastructure module",
                           response_format=response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            item_type = ItemType()
            form = ItemTypeForm(
                request.user.get_profile(), request.POST, instance=item_type)
            if form.is_valid():
                item = form.save(request)
                item_type.set_user_from_request(request)
                return HttpResponseRedirect(reverse('infrastructure_type_view', args=[item.id]))
        else:
            return HttpResponseRedirect(reverse('infrastructure_settings_view'))
    else:
        form = ItemTypeForm(request.user.get_profile())

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('infrastructure/item_type_add', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def type_delete(request, type_id, response_format='html'):
    "ItemType delete page"
    type = get_object_or_404(ItemType, pk=type_id)
    if not request.user.get_profile().has_permission(type, mode="w"):
        return user_denied(request, message="You don't have write access to this ItemType")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                type.trash = True
                type.save()
            else:
                type.delete()
            return HttpResponseRedirect(reverse('infrastructure_settings_view'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('infrastructure_item_type_view', args=[type.id]))

    context = _get_default_context(request)
    context.update({'item_type': type})

    return render_to_response('infrastructure/item_type_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)

#
# Fields
#


@treeio_login_required
@handle_response_format
@_process_mass_form
def field_view(request, field_id, response_format='html'):
    "ItemField view"

    field = get_object_or_404(ItemField, pk=field_id)
    if not request.user.get_profile().has_permission(field):
        return user_denied(request, message="You don't have access to this Field Type",
                           response_format=response_format)

    context = _get_default_context(request)
    context.update({'field': field})

    return render_to_response('infrastructure/field_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def field_edit(request, field_id, response_format='html'):
    "ItemField edit"

    field = get_object_or_404(ItemField, pk=field_id)
    if not request.user.get_profile().has_permission(field, mode='w'):
        return user_denied(request, message="You don't have access to this Field Type",
                           response_format=response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            form = ItemFieldForm(request.POST, instance=field)
            if form.is_valid():
                item = form.save(request)
                return HttpResponseRedirect(reverse('infrastructure_field_view', args=[item.id]))
        else:
            return HttpResponseRedirect(reverse('infrastructure_field_view', args=[item.id]))
    else:
        form = ItemFieldForm(instance=field)

    context = _get_default_context(request)
    context.update({'form': form,
                    'field': field})

    return render_to_response('infrastructure/field_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def field_add(request, response_format='html'):
    "ItemField add"

    if not request.user.get_profile().is_admin('treeio.infrastructure'):
        return user_denied(request,
                           message="You don't have administrator access to the Infrastructure module",
                           response_format=response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            field = ItemField()
            form = ItemFieldForm(request.POST, instance=field)
            if form.is_valid():
                field = form.save(request)
                field.set_user_from_request(request)
                return HttpResponseRedirect(reverse('infrastructure_field_view', args=[field.id]))
        else:
            return HttpResponseRedirect(reverse('infrastructure_settings_view'))
    else:
        form = ItemFieldForm()

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('infrastructure/field_add', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def field_delete(request, field_id, response_format='html'):
    "ItemField delete page"
    field = get_object_or_404(ItemField, pk=field_id)
    if not request.user.get_profile().has_permission(field, mode="w"):
        return user_denied(request, message="You don't have write access to this ItemField")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                field.trash = True
                field.save()
            else:
                field.delete()
            return HttpResponseRedirect(reverse('infrastructure_settings_view'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('infrastructure_field_view', args=[field.id]))

    context = _get_default_context(request)
    context.update({'field': field})

    return render_to_response('infrastructure/field_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)


#
# Statuses
#
@treeio_login_required
@handle_response_format
@_process_mass_form
def status_view(request, status_id, response_format='html'):
    "ItemStatus view"

    item_status = get_object_or_404(ItemStatus, pk=status_id)
    if not request.user.get_profile().has_permission(item_status):
        return user_denied(request, message="You don't have access to this Item Status",
                           response_format=response_format)

    query = Q(status=item_status)
    if request.GET:
        query = query & _get_filter_query(request.GET)
    items = Object.filter_by_request(
        request, Item.objects.filter(query).order_by('name'))

    filters = FilterForm(request.user.get_profile(), ['status'], request.GET)

    context = _get_default_context(request)
    context.update({'items': items,
                   'filters': filters,
                   'item_status': item_status
                    })

    return render_to_response('infrastructure/item_status_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def status_edit(request, status_id, response_format='html'):
    "ItemStatus edit"

    item_status = get_object_or_404(ItemStatus, pk=status_id)
    if not request.user.get_profile().has_permission(item_status, mode='w'):
        return user_denied(request, message="You don't have access to this Item Status",
                           response_format=response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            form = ItemStatusForm(request.POST, instance=item_status)
            if form.is_valid():
                item_status = form.save(request)
                return HttpResponseRedirect(reverse('infrastructure_status_view', args=[item_status.id]))
        else:
            return HttpResponseRedirect(reverse('infrastructure_status_view', args=[item_status.id]))
    else:
        form = ItemStatusForm(instance=item_status)

    context = _get_default_context(request)
    context.update({'item_status': item_status,
                    'form': form})

    return render_to_response('infrastructure/item_status_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def status_delete(request, status_id, response_format='html'):
    "ItemStatus delete"

    item_status = get_object_or_404(ItemStatus, pk=status_id)
    if not request.user.get_profile().has_permission(item_status, mode='w'):
        return user_denied(request, message="You don't have access to this Item Status",
                           response_format=response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                item_status.trash = True
                item_status.save()
            else:
                item_status.delete()
            return HttpResponseRedirect(reverse('infrastructure_settings_view'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('infrastructure_item_view', args=[item_status.id]))

    context = _get_default_context(request)
    context.update({'item_status': item_status})

    return render_to_response('infrastructure/item_status_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def status_add(request, response_format='html'):
    "ItemStatus edit"

    if not request.user.get_profile().is_admin('treeio.infrastructure'):
        return user_denied(request, message="You are not an Administrator of the Infrastructure module",
                           response_format=response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            item_status = ItemStatus()
            form = ItemStatusForm(request.POST, instance=item_status)
            if form.is_valid():
                item_status = form.save(request)
                item_status.set_user_from_request(request)
                return HttpResponseRedirect(reverse('infrastructure_status_view', args=[item_status.id]))
        else:
            return HttpResponseRedirect(reverse('infrastructure_settings_view'))
    else:
        form = ItemStatusForm()

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('infrastructure/item_status_add', context,
                              context_instance=RequestContext(request), response_format=response_format)
#
# Items
#


@treeio_login_required
@handle_response_format
def item_add(request, response_format='html'):
    "New item form"

    context = _get_default_context(request)

    return render_to_response('infrastructure/item_add', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def item_add_typed(request, type_id, response_format='html'):
    "Item add with preselected type"

    item_type = get_object_or_404(ItemType, pk=type_id)
    if not request.user.get_profile().has_permission(item_type, mode='x'):
        return user_denied(request, message="You don't have access to create " + unicode(item_type),
                           response_format=response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            form = ItemForm(
                request.user.get_profile(), item_type, request.POST, files=request.FILES)
            if form.is_valid():
                item = form.save(request)
                return HttpResponseRedirect(reverse('infrastructure_item_view', args=[item.id]))
        else:
            return HttpResponseRedirect(reverse('infrastructure_index'))
    else:
        form = ItemForm(request.user.get_profile(), item_type)

    context = _get_default_context(request)
    context.update({'item_type': item_type,
                    'form': form})

    return render_to_response('infrastructure/item_add_typed', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def item_view(request, item_id, response_format='html'):
    "Item view"
    item = get_object_or_404(Item, pk=item_id)
    if not request.user.get_profile().has_permission(item):
        return user_denied(request, message="You don't have access to this Item",
                           response_format=response_format)

    context = _get_default_context(request)
    context.update({'item': item})

    return render_to_response('infrastructure/item_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def item_edit(request, item_id, response_format='html'):
    "Item edit page"
    item = get_object_or_404(Item, pk=item_id)
    if not request.user.get_profile().has_permission(item, mode="w"):
        return user_denied(request, message="You don't have write access to this Item",
                           response_format=response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            form = ItemForm(request.user.get_profile(), item.item_type, request.POST,
                            files=request.FILES, instance=item)
            if form.is_valid():
                item = form.save(request)
                return HttpResponseRedirect(reverse('infrastructure_item_view', args=[item.id]))
        else:
            return HttpResponseRedirect(reverse('infrastructure_item_view', args=[item.id]))
    else:
        form = ItemForm(
            request.user.get_profile(), item.item_type, instance=item)

    context = _get_default_context(request)
    context.update({'item': item,
                    'form': form})

    return render_to_response('infrastructure/item_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def item_delete(request, item_id, response_format='html'):
    "Item delete page"
    item = get_object_or_404(Item, pk=item_id)
    if not request.user.get_profile().has_permission(item, mode="w"):
        return user_denied(request, message="You don't have write access to this Item")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                item.trash = True
                item.save()
            else:
                item.delete()
            return HttpResponseRedirect(reverse('infrastructure_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('infrastructure_item_view', args=[item.id]))

    context = _get_default_context(request)
    context.update({'item': item})

    return render_to_response('infrastructure/item_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)


#
# Locations
#
@treeio_login_required
@handle_response_format
def location_add(request, response_format='html'):
    "New location form"

    if request.POST:
        if not 'cancel' in request.POST:
            location = Location()
            form = LocationForm(
                request.user.get_profile(), None, request.POST, instance=location)
            if form.is_valid():
                location = form.save()
                location.set_user_from_request(request)
                return HttpResponseRedirect(reverse('infrastructure_location_view', args=[location.id]))
        else:
            return HttpResponseRedirect(reverse('infrastructure_index'))
    else:
        form = LocationForm(request.user.get_profile(), None)

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('infrastructure/location_add', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
@_process_mass_form
def location_view(request, location_id, response_format='html'):
    "Location view"
    location = get_object_or_404(Location, pk=location_id)
    if not request.user.get_profile().has_permission(location):
        return user_denied(request, message="You don't have access to this Location",
                           response_format=response_format)

    query = Q(location=location)
    if request.GET:
        query = query & _get_filter_query(request.GET)
    items = Object.filter_by_request(
        request, Item.objects.filter(query).order_by('name'))

    context = _get_default_context(request)
    context.update({
        'location': location,
        'items': items
    })

    return render_to_response('infrastructure/location_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def location_edit(request, location_id, response_format='html'):
    "Location edit page"
    location = get_object_or_404(Location, pk=location_id)
    if not request.user.get_profile().has_permission(location, mode="w"):
        return user_denied(request, message="You don't have write access to this Location",
                           response_format=response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            form = LocationForm(
                request.user.get_profile(), None, request.POST, instance=location)
            if form.is_valid():
                location = form.save(request)
                return HttpResponseRedirect(reverse('infrastructure_location_view', args=[location.id]))
        else:
            return HttpResponseRedirect(reverse('infrastructure_location_view', args=[location.id]))
    else:
        form = LocationForm(
            request.user.get_profile(), None, instance=location)

    context = _get_default_context(request)
    context.update({'location': location,
                    'form': form})

    return render_to_response('infrastructure/location_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def location_delete(request, location_id, response_format='html'):
    "Location delete page"
    location = get_object_or_404(Location, pk=location_id)
    if not request.user.get_profile().has_permission(location, mode="w"):
        return user_denied(request, message="You don't have write access to this Location")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                location.trash = True
                location.save()
            else:
                location.delete()
            return HttpResponseRedirect(reverse('infrastructure_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('infrastructure_location_view', args=[location.id]))

    context = _get_default_context(request)
    context.update({'location': location})

    return render_to_response('infrastructure/location_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)


#
# Settings
#
@handle_response_format
@treeio_login_required
@module_admin_required('treeio.infrastructure')
def settings_view(request, response_format='html'):
    "Settings"

    if not request.user.get_profile().is_admin('treeio.infrastructure'):
        return user_denied(request, message="You are not an Administrator of the Infrastructure module",
                           response_format=response_format)

    item_types = ItemType.objects.all().filter(trash=False)
    item_statuses = ItemStatus.objects.all().filter(trash=False)
    item_fields = ItemField.objects.all().filter(trash=False)

    default_item_status = None
    try:
        conf = ModuleSetting.get_for_module(
            'treeio.infrastructure', 'default_item_status')[0]
        default_item_status = ItemStatus.objects.get(
            pk=long(conf.value), trash=False)
    except Exception:
        pass

    context = _get_default_context(request)
    context.update({'item_types': item_types,
                    'item_fields': item_fields,
                    'item_statuses': item_statuses,
                    'default_item_status': default_item_status})

    return render_to_response('infrastructure/settings_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
@module_admin_required('treeio.infrastructure')
def settings_edit(request, response_format='html'):
    "Settings"

    if request.POST:
        if not 'cancel' in request.POST:
            form = SettingsForm(request.user.get_profile(), request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('infrastructure_settings_view'))
        else:
            return HttpResponseRedirect(reverse('infrastructure_settings_view'))
    else:
        form = SettingsForm(request.user.get_profile())

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('infrastructure/settings_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)

#
# Service Records
#


@treeio_login_required
@handle_response_format
@_process_mass_form
def service_record_index(request, response_format='html'):
    "Index page: displays all Items"
    query = Q()
    if request.GET:
        query = query & _get_filter_query(request.GET)
    service_records = Object.filter_by_request(
        request, ItemServicing.objects.filter(query))

    filters = FilterForm(request.user.get_profile(), '', request.GET)

    context = _get_default_context(request)
    context.update({'service_records': service_records,
                    'filters': filters})

    return render_to_response('infrastructure/service_record_index', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def service_record_add(request, response_format='html'):
    "New service_record form"

    if not request.user.get_profile().is_admin('treeio.infrastructure'):
        return user_denied(request,
                           message="You don't have administrator access to the Infrastructure module")

    service_record = ItemServicing()

    if request.POST:
        if not 'cancel' in request.POST:
            form = ServiceRecordForm(
                request.user.get_profile(), service_record, request.POST)
            if form.is_valid():
                record = form.save(request)
                return HttpResponseRedirect(reverse('infrastructure_service_record_view', args=[record.id]))
        else:
            return HttpResponseRedirect(reverse('infrastructure_service_record_index'))
    else:
        form = ServiceRecordForm(request.user.get_profile(), service_record)

    context = _get_default_context(request)
    context.update({'service_record': service_record,
                    'form': form})

    return render_to_response('infrastructure/service_record_add', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def service_record_view(request, service_record_id, response_format='html'):
    "ServiceRecord view"
    service_record = get_object_or_404(ItemServicing, pk=service_record_id)
    if not request.user.get_profile().has_permission(service_record):
        return user_denied(request, message="You don't have access to this ServiceRecord",
                           response_format=response_format)

    context = _get_default_context(request)
    context.update({'service_record': service_record})

    return render_to_response('infrastructure/service_record_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def service_record_edit(request, service_record_id, response_format='html'):
    "ServiceRecord edit page"

    service_record = get_object_or_404(ItemServicing, pk=service_record_id)
    if not request.user.get_profile().has_permission(service_record, mode="w"):
        return user_denied(request, message="You don't have write access to this ServiceRecord",
                           response_format=response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            form = ServiceRecordForm(
                request.user.get_profile(), None, request.POST, instance=service_record)
            if form.is_valid():
                service_record = form.save(request)
                return HttpResponseRedirect(reverse('infrastructure_service_record_view',
                                                    args=[service_record.id]))
        else:
            return HttpResponseRedirect(reverse('infrastructure_service_record_view',
                                                args=[service_record.id]))
    else:
        form = ServiceRecordForm(
            request.user.get_profile(), None, instance=service_record)

    context = _get_default_context(request)
    context.update({'service_record': service_record,
                    'form': form})

    return render_to_response('infrastructure/service_record_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def service_record_delete(request, service_record_id, response_format='html'):
    "ServiceRecord delete page"
    service_record = get_object_or_404(ItemServicing, pk=service_record_id)
    if not request.user.get_profile().has_permission(service_record, mode="w"):
        return user_denied(request, message="You don't have write access to this ServiceRecord")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                service_record.trash = True
                service_record.save()
            else:
                service_record.delete()
            return HttpResponseRedirect(reverse('infrastructure_settings_view'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('infrastructure_service_record_view',
                                                args=[service_record.id]))

    context = _get_default_context(request)
    context.update({'service_record': service_record})

    return render_to_response('infrastructure/service_record_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)
