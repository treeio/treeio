# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Handle objects from this module relevant to a Contact or a User
"""
from treeio.core.models import Object
from treeio.services.models import Ticket
from treeio.services.templatetags.services import services_ticket_list

CONTACT_OBJECTS = {}
CONTACT_OBJECTS['ticket_set'] = {'label': 'Tickets',
                                 'objects': [],
                                 'templatetag': services_ticket_list}

CONTACT_OBJECTS['client_sla'] = {'label': 'Service Level Agreements',
                                 'objects': [],
                                 'templatetag': None}

CONTACT_OBJECTS['provider_sla'] = {'label': 'Provided SLAs',
                                   'objects': [],
                                   'templatetag': None}

USER_OBJECTS = {}
USER_OBJECTS['serviceagent_set'] = {'label': 'Assigned Tickets',
                                    'objects': [],
                                    'templatetag': services_ticket_list}


def get_contact_objects(current_user, contact):
    """
    Returns a dictionary with keys specified as contact attributes
    and values as dictionaries with labels and set of relevant objects.
    """

    objects = dict(CONTACT_OBJECTS)

    for key in objects:
        if hasattr(contact, key):
            manager = getattr(contact, key)
            try:
                manager = manager.filter(status__hidden=False)
            except:
                pass
            objects[key]['objects'] = Object.filter_permitted(
                current_user, manager)

    return objects


def get_user_objects(current_user, user):
    """
    Returns a dictionary with keys specified as contact attributes
    and values as dictionaries with labels and set of relevant objects.
    """

    objects = dict(USER_OBJECTS)

    for key in objects:
        if hasattr(user, key):
            if key == 'serviceagent_set':
                manager = Ticket.objects.filter(assigned__related_user=user)
            else:
                manager = getattr(user, key)
            if hasattr(manager, 'status'):
                manager = manager.filter(status__hidden=False)
            objects[key]['objects'] = Object.filter_permitted(
                current_user, manager)

    return objects
