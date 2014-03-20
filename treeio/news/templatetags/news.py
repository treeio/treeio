# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
News templatetags
"""
from coffin import template
from treeio.core.rendering import render_to_string
from jinja2 import contextfunction, Markup
from django.template import RequestContext

register = template.Library()


@contextfunction
def news_update_list(context, updates, skip_group=False):
    "Print a list of orders"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('news/tags/update_list',
                                   {'updates': updates},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(news_update_list)
