# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Infrastructure templatetags
"""
from coffin import template
from treeio.core.rendering import render_to_string
from jinja2 import contextfunction, Markup
from django.template import RequestContext

register = template.Library()


@contextfunction
def infrastructure_item_list(context, items, skip_group=False):
    "Print a list of tasks"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('infrastructure/tags/item_list',
                                   {'items': items, 'skip_group': skip_group},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(infrastructure_item_list)


@contextfunction
def infrastructure_servicing_list(context, items, skip_group=False):
    "Print a list of tasks"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('infrastructure/tags/servicing_list',
                                   {'service_records': items,
                                       'skip_group': skip_group},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(infrastructure_servicing_list)
