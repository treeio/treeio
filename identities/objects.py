# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Contact module helpers
"""
from treeio.core.models import Module
from django.utils.translation import ugettext_lazy as _


def _get_module_objects(module, current_user, related, getter_name):

    try:
        import_name = module.name + ".identities"
        modident = __import__(import_name, fromlist=[str(module.name)])
        getter = getattr(modident, getter_name)
        return getter(current_user, related)
    except ImportError:
        pass
    except AttributeError:
        pass
    except KeyError:
        pass

    return {}


def _preformat_objects(modules, objects):
    """
    Formats objects returned from get_contact_objects or get_user_objects
    for a more convenient output and templating, structured by module
    """

    output = {}

    if objects:
        for module in modules:
            output[module.name] = {'module': module,
                                   'label': _(module.title),
                                   'count': 0,
                                   'objects': {}}
            for key in objects:
                if objects[key]['module'] == module:
                    if hasattr(objects[key]['objects'], 'count'):
                        output[module.name][
                            'count'] += objects[key]['objects'].count()
                    objects[key]['label'] = _(objects[key]['label'])
                    output[module.name]['objects'][key] = objects[key]

    return output


def get_contact_objects(current_user, contact, module=None, preformat=False):
    """
    Returns a dictionary with keys specified as contact attributes
    and values as dictionaries with labels and set of relevant objects.

    Only modules enabled for the current_user are considered.
    """

    objects = dict()

    if module:
        contact_objects = _get_module_objects(
            module, current_user, contact, 'get_contact_objects')
        if contact_objects:
            for key in contact_objects:
                contact_objects[key]['module'] = module
            objects.update(contact_objects)
        if contact.related_user:
            try:
                objects.update(
                    get_user_objects(current_user, contact.related_user.user, module))
            except:
                pass
        modules = [module]
    else:
        perspective = current_user.get_perspective()

        modules = perspective.modules.filter(display=True).order_by('title')
        if not modules:
            modules = Module.objects.filter(display=True).order_by('title')

        for module in modules:
            contact_objects = _get_module_objects(
                module, current_user, contact, 'get_contact_objects')
            if contact_objects:
                for key in contact_objects:
                    contact_objects[key]['module'] = module
                objects.update(contact_objects)
            if contact.related_user:
                try:
                    objects.update(
                        get_user_objects(current_user, contact.related_user.user, module))
                except:
                    pass

    if preformat:
        return _preformat_objects(modules, objects)

    return objects


def get_user_objects(current_user, user, module=None, preformat=False):
    """
    Returns a dictionary with keys specified as user attributes
    and values as dictionaries with labels, number of relevant objects,
    and optionally the actual set of relevant objects.

    Only modules enabled for the current_user are considered.
    """

    objects = dict()

    if module:
        user_objects = _get_module_objects(
            module, current_user, user, 'get_user_objects')
        if user_objects:
            for key in user_objects:
                user_objects[key]['module'] = module
                objects['related_user.' + key] = user_objects[key]
        modules = [module]
    else:
        perspective = current_user.get_perspective()

        modules = perspective.modules.filter(display=True).order_by('title')
        if not modules:
            modules = Module.objects.filter(display=True).order_by('title')

        for module in modules:
            user_objects = _get_module_objects(
                module, current_user, user, 'get_user_objects')
            if user_objects:
                for key in user_objects:
                    user_objects[key]['module'] = module
                    objects['related_user.' + key] = user_objects[key]

    if preformat:
        return _preformat_objects(modules, objects)
    return objects
