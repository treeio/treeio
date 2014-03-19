# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Sales templatetags
"""
from coffin import template
from treeio.core.rendering import render_to_string
from jinja2 import contextfunction, Markup
from django.template import RequestContext

register = template.Library()


@contextfunction
def sales_order_list(context, orders, skip_group=False):
    "Print a list of orders"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('sales/tags/order_list',
                                   {'orders': orders,
                                       'skip_group': skip_group},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(sales_order_list)


@contextfunction
def sales_lead_list(context, leads, skip_group=False):
    "Print a list of leads"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('sales/tags/lead_list',
                                   {'leads': leads, 'skip_group': skip_group},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(sales_lead_list)


@contextfunction
def sales_opportunity_list(context, opportunities, skip_group=False):
    "Print a list of opportunitys"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('sales/tags/opportunity_list',
                                   {'opportunities': opportunities,
                                       'skip_group': skip_group},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(sales_opportunity_list)


@contextfunction
def sales_product_list(context, products, skip_group=False):
    "Print a list of products"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('sales/tags/product_list',
                                   {'products': products,
                                       'skip_group': skip_group},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(sales_product_list)
