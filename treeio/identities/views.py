# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Identities module: views
"""
from treeio.identities.identicon import render_identicon
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_control
from django.db.models import Q
from treeio.core.rendering import render_to_response
from treeio.core.forms import LocationForm
from treeio.core.models import User, Group, Object, Location, AccessEntity
from treeio.core.views import user_denied
from treeio.core.decorators import treeio_login_required, handle_response_format
from treeio.identities.csvapi import ProcessContacts
from treeio.identities.models import Contact, ContactType, ContactField
from treeio.identities.forms import ContactForm, FilterForm, ContactTypeForm, ContactFieldForm, \
    MassActionForm
from treeio.identities.objects import get_contact_objects


def _get_filter_query(args):
    "Creates a query to filter Identities based on FilterForm arguments"
    query = Q()

    for arg in args:
        if hasattr(Contact, arg) and args[arg]:
            kwargs = {str(arg + '__id'): long(args[arg])}
            query = query & Q(**kwargs)

    return query


def _get_default_context(request):
    "Preprocess context"

    context = {}
    types = Object.filter_by_request(
        request, ContactType.objects.order_by('name'))
    massform = MassActionForm(request.user.get_profile())
    context.update({'types': types,
                    'massform': massform})

    return context


def _process_mass_form(f):
    "Pre-process request to handle mass action form for Messages"

    def wrap(request, *args, **kwargs):
        "Wrap"
        user = request.user.get_profile()
        if 'massform' in request.POST:
            for key in request.POST:
                if 'mass-contact' in key:
                    try:
                        contact = Contact.objects.get(pk=request.POST[key])
                        form = MassActionForm(
                            user, request.POST, instance=contact)
                        if form.is_valid() and user.has_permission(contact, mode='w'):
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
    "Default page"

    if request.GET:
        query = _get_filter_query(request.GET)
        contacts = Object.filter_by_request(
            request, Contact.objects.filter(query).order_by('name'))
    else:
        contacts = Object.filter_by_request(
            request, Contact.objects.order_by('name'))

    filters = FilterForm(request.user.get_profile(), 'name', request.GET)

    context = _get_default_context(request)
    context.update({'contacts': contacts,
                    'filters': filters})

    return render_to_response('identities/index', context,
                              context_instance=RequestContext(request), response_format=response_format)


#
# ContactTypes
#
@handle_response_format
@treeio_login_required
@_process_mass_form
def type_view(request, type_id, response_format='html'):
    "Contacts by type"

    contact_type = get_object_or_404(ContactType, pk=type_id)
    if not request.user.get_profile().has_permission(contact_type):
        return user_denied(request, message="You don't have access to this Contact Type")
    contacts = Object.filter_by_request(
        request, Contact.objects.filter(contact_type=contact_type))

    context = _get_default_context(request)
    context.update({'contacts': contacts,
                    'type': contact_type})

    return render_to_response('identities/contact_type_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def type_edit(request, type_id, response_format='html'):
    "ContactType edit"

    contact_type = get_object_or_404(ContactType, pk=type_id)
    if not request.user.get_profile().has_permission(contact_type, mode='w'):
        return user_denied(request, message="You don't have access to this Contact Type",
                           response_format=response_format)
    identities = Object.filter_by_request(request,
                                          Contact.objects.filter(contact_type=contact_type).order_by('name'))

    if request.POST:
        if not 'cancel' in request.POST:
            form = ContactTypeForm(
                request.user.get_profile(), request.POST, instance=contact_type)
            if form.is_valid():
                contact_type = form.save(request)
                return HttpResponseRedirect(reverse('identities_type_view', args=[contact_type.id]))
        else:
            return HttpResponseRedirect(reverse('identities_type_view', args=[contact_type.id]))
    else:
        form = ContactTypeForm(
            request.user.get_profile(), instance=contact_type)

    context = _get_default_context(request)
    context.update({'identities': identities,
                    'form': form,
                    'type': contact_type})

    return render_to_response('identities/contact_type_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def type_add(request, response_format='html'):
    "ContactType add"

    if not request.user.get_profile().is_admin('treeio.identities'):
        return user_denied(request,
                           message="You don't have administrator access to the Infrastructure module",
                           response_format=response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            contact_type = ContactType()
            form = ContactTypeForm(
                request.user.get_profile(), request.POST, instance=contact_type)
            if form.is_valid():
                contact_type = form.save(request)
                contact_type.set_user_from_request(request)
                return HttpResponseRedirect(reverse('identities_type_view', args=[contact_type.id]))
        else:
            return HttpResponseRedirect(reverse('identities_settings_view'))
    else:
        form = ContactTypeForm(request.user.get_profile())

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('identities/contact_type_add', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def type_delete(request, type_id, response_format='html'):
    "ContactType delete page"
    type = get_object_or_404(ContactType, pk=type_id)
    if not request.user.get_profile().has_permission(type, mode="w"):
        return user_denied(request, message="You don't have write access to this ContactType")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                type.trash = True
                type.save()
            else:
                type.delete()
            return HttpResponseRedirect(reverse('identities_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('identities_type_view', args=[type.id]))

    context = _get_default_context(request)
    context.update({'type': type})

    return render_to_response('identities/contact_type_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)

#
# Fields
#


@handle_response_format
@treeio_login_required
def field_view(request, field_id, response_format='html'):
    "ContactField view"

    field = get_object_or_404(ContactField, pk=field_id)
    if not request.user.get_profile().has_permission(field):
        return user_denied(request, message="You don't have access to this Field Type",
                           response_format=response_format)

    context = _get_default_context(request)
    context.update({'field': field})

    return render_to_response('identities/field_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def field_edit(request, field_id, response_format='html'):
    "ContactField edit"

    field = get_object_or_404(ContactField, pk=field_id)
    if not request.user.get_profile().has_permission(field, mode='w'):
        return user_denied(request, message="You don't have access to this Field Type",
                           response_format=response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            form = ContactFieldForm(request.POST, instance=field)
            if form.is_valid():
                field = form.save(request)
                return HttpResponseRedirect(reverse('identities_field_view', args=[field.id]))
        else:
            return HttpResponseRedirect(reverse('identities_field_view', args=[field.id]))
    else:
        form = ContactFieldForm(instance=field)

    context = _get_default_context(request)
    context.update({'form': form,
                    'field': field})

    return render_to_response('identities/field_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def field_add(request, response_format='html'):
    "ContactField add"

    if not request.user.get_profile().is_admin('treeio.identities'):
        return user_denied(request,
                           message="You don't have administrator access to the Infrastructure module",
                           response_format=response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            field = ContactField()
            form = ContactFieldForm(request.POST, instance=field)
            if form.is_valid():
                field = form.save(request)
                field.set_user_from_request(request)
                return HttpResponseRedirect(reverse('identities_field_view', args=[field.id]))
        else:
            return HttpResponseRedirect(reverse('identities_settings_view'))
    else:
        form = ContactFieldForm()

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('identities/field_add', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def field_delete(request, field_id, response_format='html'):
    "ContactField delete page"
    field = get_object_or_404(ContactField, pk=field_id)
    if not request.user.get_profile().has_permission(field, mode="w"):
        return user_denied(request, message="You don't have write access to this ContactField")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                field.trash = True
                field.save()
            else:
                field.delete()
            return HttpResponseRedirect(reverse('identities_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('identities_field_view', args=[field.id]))

    context = _get_default_context(request)
    context.update({'field': field})

    return render_to_response('identities/field_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def contact_add(request, response_format='html'):
    "Contact add"

    types = Object.filter_by_request(
        request, ContactType.objects.order_by('name'))

    return render_to_response('identities/contact_add',
                              {'types': types},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def contact_add_typed(request, type_id, response_format='html'):
    "Contact add with preselected type"

    contact_type = get_object_or_404(ContactType, pk=type_id)
    if not request.user.get_profile().has_permission(contact_type, mode='x'):
        return user_denied(request, message="You don't have access to create " + unicode(contact_type))

    if request.POST:
        if not 'cancel' in request.POST:
            form = ContactForm(
                request.user.get_profile(), contact_type, request.POST, files=request.FILES)
            if form.is_valid():
                contact = form.save(request, contact_type)
                contact.set_user_from_request(request)
                return HttpResponseRedirect(reverse('identities_contact_view', args=[contact.id]))
        else:
            return HttpResponseRedirect(reverse('identities_index'))
    else:
        form = ContactForm(request.user.get_profile(), contact_type)

    types = Object.filter_by_request(
        request, ContactType.objects.order_by('name'))

    return render_to_response('identities/contact_add_typed',
                              {'type': contact_type,
                                  'types': types, 'form': form},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def contact_view(request, contact_id, attribute='', response_format='html'):
    "Contact view"

    contact = get_object_or_404(Contact, pk=contact_id)
    if not request.user.get_profile().has_permission(contact):
        return user_denied(request, message="You don't have access to this Contact")
    types = Object.filter_by_request(
        request, ContactType.objects.order_by('name'))

    subcontacts = Object.filter_by_request(request, contact.child_set)
    contact_values = contact.contactvalue_set.order_by('field__name')

    objects = get_contact_objects(
        request.user.get_profile(), contact, preformat=True)

    module = None
    for key in objects:
        if not attribute:
            if objects[key]['count']:
                #attribute = objects[key]['objects'].keys()[0]
                module = objects[key]['module']
        else:
            if attribute in objects[key]['objects'].keys():
                module = objects[key]['module']
                break

    return render_to_response('identities/contact_view',
                              {'contact': contact,
                               'subcontacts': subcontacts,
                               'objects': objects,
                               'current_module': module,
                               'attribute': attribute,
                               'types': types,
                               'contact_values': contact_values},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def contact_me(request, attribute='', response_format='html'):
    "My Contact card"

    contact = request.user.get_profile().get_contact()
    if not request.user.get_profile().has_permission(contact):
        return user_denied(request, message="You don't have access to this Contact")
    types = Object.filter_by_request(
        request, ContactType.objects.order_by('name'))

    if not contact:
        return render_to_response('identities/contact_me_missing', {'types': types},
                                  context_instance=RequestContext(request), response_format=response_format)

    subcontacts = Object.filter_by_request(request, contact.child_set)
    contact_values = contact.contactvalue_set.order_by('field__name')

    objects = get_contact_objects(
        request.user.get_profile(), contact, preformat=True)

    module = None
    for key in objects:
        if not attribute:
            if objects[key]['count']:
                #attribute = objects[key]['objects'].keys()[0]
                module = objects[key]['module']
        else:
            if attribute in objects[key]['objects'].keys():
                module = objects[key]['module']
                break

    return render_to_response('identities/contact_me',
                              {'contact': contact, 'types': types,
                               'subcontacts': subcontacts,
                               'objects': objects,
                               'current_module': module,
                               'attribute': attribute,
                               'types': types,
                               'contact_values': contact_values},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@cache_control(private=True, max_age=31536000)
def contact_view_picture(request, contact_id, response_format='html'):
    "Contact view Picture"
    response = HttpResponse(mimetype="image/png")
    render_identicon(contact_id * 5000).save(response, "PNG")
    return response


@handle_response_format
@treeio_login_required
def contact_edit(request, contact_id, response_format='html'):
    "Contact edit"

    contact = get_object_or_404(Contact, pk=contact_id)
    if not request.user.get_profile().has_permission(contact, mode='w'):
        return user_denied(request, message="You don't have write access to this Contact")

    if request.POST:
        if not 'cancel' in request.POST:
            form = ContactForm(request.user.get_profile(), contact.contact_type, request.POST,
                               files=request.FILES, instance=contact)
            if form.is_valid():
                contact = form.save(request)
                return HttpResponseRedirect(reverse('identities_contact_view', args=[contact.id]))
        else:
            return HttpResponseRedirect(reverse('identities_contact_view', args=[contact.id]))
    else:
        form = ContactForm(
            request.user.get_profile(), contact.contact_type, instance=contact)

    types = Object.filter_by_request(
        request, ContactType.objects.order_by('name'))

    return render_to_response('identities/contact_edit',
                              {'contact': contact,
                               'types': types,
                               'form': form},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def contact_delete(request, contact_id, response_format='html'):
    "Contact delete"

    contact = get_object_or_404(Contact, pk=contact_id)
    if not request.user.get_profile().has_permission(contact, mode='w'):
        return user_denied(request, message="You don't have access to this Contact")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                contact.trash = True
                contact.save()
            else:
                contact.delete()
            return HttpResponseRedirect(reverse('identities_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('identities_contact_view', args=[contact.id]))

    types = Object.filter_by_request(
        request, ContactType.objects.order_by('name'))

    return render_to_response('identities/contact_delete',
                              {'contact': contact, 'types': types},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def index_users(request, response_format='html'):
    "User List"

    users = User.objects.exclude(disabled=True).order_by('user__username')
    types = Object.filter_by_request(
        request, ContactType.objects.order_by('name'))

    return render_to_response('identities/index_users',
                              {'users': users, 'types': types},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def index_groups(request, response_format='html'):
    "Group List"

    groups = Group.objects.order_by('parent', 'name')
    types = Object.filter_by_request(
        request, ContactType.objects.order_by('name'))

    return render_to_response('identities/index_groups',
                              {'groups': groups, 'types': types},
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
def user_view(request, user_id, response_format='html'):
    "User view"
    user = get_object_or_404(User, pk=user_id)
    contact_id = Contact.objects.filter(related_user=user)[0].id
    return contact_view(request, contact_id, attribute='', response_format=response_format)


@handle_response_format
@treeio_login_required
def group_view(request, group_id, response_format='html'):
    "Group view"

    group = get_object_or_404(Group, pk=group_id)
    contacts = Object.filter_by_request(
        request, Contact.objects.filter(related_user=group).order_by('name'))
    members = User.objects.filter(
        Q(default_group=group) | Q(other_groups=group)).distinct()
    subgroups = Group.objects.filter(parent=group)
    types = Object.filter_by_request(
        request, ContactType.objects.order_by('name'))

    return render_to_response('identities/group_view',
                              {'group': group,
                               'subgroups': subgroups,
                               'members': members,
                               'contacts': contacts,
                               'types': types},
                              context_instance=RequestContext(request), response_format=response_format)


#
# Locations
#
@treeio_login_required
@handle_response_format
def location_index(request, location_id, response_format='html'):
    "Location index"

    locations = Object.filter_permitted(request.user.get_profile(),
                                        Location.objects)

    context = _get_default_context(request)
    context.update({
        'locations': locations,
    })

    return render_to_response('identities/location_index', context,
                              context_instance=RequestContext(request), response_format=response_format)


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
                return HttpResponseRedirect(reverse('identities_location_view', args=[location.id]))
        else:
            return HttpResponseRedirect(reverse('identities_index'))
    else:
        form = LocationForm(request.user.get_profile(), None)

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('identities/location_add', context,
                              context_instance=RequestContext(request), response_format=response_format)


@treeio_login_required
@handle_response_format
def location_view(request, location_id, response_format='html'):
    "Location view"
    location = get_object_or_404(Location, pk=location_id)
    if not request.user.get_profile().has_permission(location):
        return user_denied(request, message="You don't have access to this Location",
                           response_format=response_format)

    context = _get_default_context(request)
    context.update({
        'location': location,
    })

    return render_to_response('identities/location_view', context,
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
                return HttpResponseRedirect(reverse('identities_location_view', args=[location.id]))
        else:
            return HttpResponseRedirect(reverse('identities_location_view', args=[location.id]))
    else:
        form = LocationForm(
            request.user.get_profile(), None, instance=location)

    context = _get_default_context(request)
    context.update({'location': location,
                    'form': form})

    return render_to_response('identities/location_edit', context,
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
            return HttpResponseRedirect(reverse('identities_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('identities_location_view', args=[location.id]))

    context = _get_default_context(request)
    context.update({'location': location})

    return render_to_response('identities/location_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)


#
# Settings
#
@handle_response_format
@treeio_login_required
def settings_view(request, response_format='html'):
    "Settings"

    if not request.user.get_profile().is_admin('treeio.identities'):
        return user_denied(request, message="You are not an Administrator of the Identities module",
                           response_format=response_format)

    contact_types = ContactType.objects.all().filter(trash=False)
    contact_fields = ContactField.objects.all().filter(trash=False)
    contacts = Object.filter_by_request(
        request, Contact.objects.order_by('name'))

    context = _get_default_context(request)
    context.update({'contact_types': contact_types,
                    'contact_fields': contact_fields,
                    'contacts': contacts})

    if request.POST:
        if 'file' in request.FILES:
            csv_file = request.FILES['file']

            # TODO: check file extension
            content = csv_file.read()
            import_c = ProcessContacts()
            import_c.import_contacts(content)

            return HttpResponseRedirect(reverse('identities_index'))

    return render_to_response('identities/settings_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


#
# AJAX autocomplete handlers
#


@treeio_login_required
def ajax_access_lookup(request, response_format='html'):
    "Returns a list of matching users"

    entities = []
    if request.GET and 'term' in request.GET:
        entities = AccessEntity.objects.filter(Q(user__name__icontains=request.GET['term']) |
                                               Q(user__contact__name__icontains=request.GET['term']) |
                                               Q(group__name__icontains=request.GET['term']))

    return render_to_response('identities/ajax_access_lookup',
                              {'entities': entities},
                              context_instance=RequestContext(request),
                              response_format=response_format)


@treeio_login_required
def ajax_user_lookup(request, response_format='html'):
    "Returns a list of matching users"

    users = []
    if request.GET and 'term' in request.GET:
        users = User.objects.filter(Q(name__icontains=request.GET['term']) |
                                    Q(contact__name__icontains=request.GET['term']))

    return render_to_response('identities/ajax_user_lookup',
                              {'users': users},
                              context_instance=RequestContext(request),
                              response_format=response_format)


@treeio_login_required
def ajax_contact_lookup(request, response_format='html'):
    "Returns a list of matching contacts"

    contacts = []
    if request.GET and 'term' in request.GET:
        user = request.user.get_profile()
        contacts = Object.filter_permitted(user, Contact.objects,
                                           mode='x').filter(Q(name__icontains=request.GET['term']))[:10]

    return render_to_response('identities/ajax_contact_lookup',
                              {'contacts': contacts},
                              context_instance=RequestContext(request),
                              response_format=response_format)


@treeio_login_required
def ajax_location_lookup(request, response_format='html'):
    "Returns a list of matching locations"

    locations = []
    if request.GET and 'term' in request.GET:
        user = request.user.get_profile()
        locations = Object.filter_permitted(user, Location.objects,
                                            mode='x').filter(
            Q(name__icontains=request.GET['term'])
        )[:10]

    return render_to_response('identities/ajax_location_lookup',
                              {'locations': locations},
                              context_instance=RequestContext(request),
                              response_format=response_format)


#
# Widgets
#

@handle_response_format
@treeio_login_required
def widget_contact_me(request, response_format='html'):
    "My Contact card"

    contact = request.user.get_profile().get_contact()
    if not request.user.get_profile().has_permission(contact):
        return user_denied(request, message="You don't have access to this Contact")
    types = Object.filter_by_request(
        request, ContactType.objects.order_by('name'))
    if contact:
        return render_to_response('identities/widgets/contact_me',
                                  {'contact': contact, 'types': types},
                                  context_instance=RequestContext(request), response_format=response_format)
    else:
        return render_to_response('identities/widgets/contact_me_missing', {'types': types},
                                  context_instance=RequestContext(request), response_format=response_format)
