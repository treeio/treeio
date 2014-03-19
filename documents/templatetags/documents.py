# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Documents templatetags
"""
from coffin import template
from treeio.core.rendering import render_to_string
from jinja2 import contextfunction, Markup
from django.template import RequestContext

register = template.Library()


@contextfunction
def documents_document_list(context, documents, skip_group=False):
    "Print a list of documents"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('documents/tags/document_list',
                                   {'documents': documents,
                                       'skip_group': skip_group},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(documents_document_list)


@contextfunction
def documents_file_list(context, files, skip_group=False):
    "Print a list of files"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('documents/tags/file_list',
                                   {'files': files, 'skip_group': skip_group},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(documents_file_list)


@contextfunction
def documents_weblink_list(context, links, skip_group=False):
    "Print a list of links"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('documents/tags/weblink_list',
                                   {'links': links, 'skip_group': skip_group},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(documents_weblink_list)


@contextfunction
def documents_objects_list(context, objects, folder, skip_group=False):
    "Print a list of all objects"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('documents/tags/objects_list',
                                   {'objects': objects,
                                       'skip_group': skip_group, 'folder': folder},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(documents_objects_list)
