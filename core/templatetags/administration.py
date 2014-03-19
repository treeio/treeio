# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Administration templatetags
"""
from coffin import template
from treeio.core.rendering import render_to_string
from jinja2 import contextfunction, Markup
from django.template import RequestContext

register = template.Library()


@contextfunction
def administration_user_list(context, users, skip_group=False):
    "Print a list of users"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('core/administration/tags/user_list',
                                   {'users': users, 'skip_group': skip_group},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))


register.object(administration_user_list)


@contextfunction
def administration_group_list(context, groups, skip_group=False):
    "Print a list of groups"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('core/administration/tags/group_list',
                                   {'groups': groups,
                                       'skip_group': skip_group},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))


register.object(administration_group_list)


@contextfunction
def administration_module_list(context, modules):
    "Print a list of users"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('core/administration/tags/module_list',
                                   {'modules': modules},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(administration_module_list)
