# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Handle objects from this module relevant to a Contact or a User
"""
from treeio.core.models import Object
from treeio.projects.templatetags.projects import projects_task_list

CONTACT_OBJECTS = {}
CONTACT_OBJECTS['manager'] = {'label': 'Managed Projects',
                              'objects': [],
                              'templatetag': None}
CONTACT_OBJECTS['client'] = {'label': 'Ordered Projects',
                             'objects': [],
                             'templatetag': None}
CONTACT_OBJECTS['task_set'] = {'label': 'Managed Tasks',
                               'objects': [],
                               'templatetag': projects_task_list}

USER_OBJECTS = {}
USER_OBJECTS['task_set'] = {'label': 'Assigned Tasks',
                            'objects': [],
                            'templatetag': projects_task_list}


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
            manager = getattr(user, key)
            try:
                manager = manager.filter(status__hidden=False)
            except:
                pass
            objects[key]['objects'] = Object.filter_permitted(
                current_user, manager)

    return objects
