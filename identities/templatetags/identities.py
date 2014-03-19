# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Identities templatetags
"""
from coffin import template
from treeio.core.rendering import render_to_string
from jinja2 import contextfunction, Markup
from django.template import RequestContext
from treeio.identities.models import ContactField

register = template.Library()


@contextfunction
def identities_contact_list(context, contacts, skip_group=''):
    "Print a list of contacts"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    contact_fields = ContactField.objects.all().filter(trash=False)

    return Markup(render_to_string('identities/tags/contact_list',
                                   {'contacts': contacts, 'skip_group': skip_group,
                                    'contact_fields': contact_fields},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(identities_contact_list)


@contextfunction
def identities_user_list(context, users, skip_group=False):
    "Print a list of users"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('identities/tags/user_list',
                                   {'users': users, 'skip_group': skip_group},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))


register.object(identities_user_list)


@contextfunction
def identities_group_list(context, groups, skip_group=False):
    "Print a list of groups"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('identities/tags/group_list',
                                   {'groups': groups,
                                       'skip_group': skip_group},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))


register.object(identities_group_list)
