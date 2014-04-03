# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- coding: utf-8 -*-

import re
import sys
import inspect
import piston.handler as handler

from types import ModuleType
from resource import CsrfExemptResource
from handlers import ObjectHandlerMetaClass

from django.core.urlresolvers import get_resolver, get_callable, get_script_prefix
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import models


def get_module(mdl):
    if isinstance(mdl, basestring):
        __import__(mdl)
        return sys.modules[mdl]
    elif isinstance(mdl, ModuleType):
        return mdl
    else:
        raise ValueError("mdl must be string or module type.")


def generate_doc(handler_cls):
    """
    Returns a `HandlerDocumentation` object
    for the given handler. Use this to generate
    documentation for your API.
    """
    if not (type(handler_cls) is ObjectHandlerMetaClass
            or type(handler_cls) is handler.HandlerMetaClass):
        raise ValueError("Give me handler, not %s" % type(handler_cls))

    return HandlerDocumentation(handler_cls)


def get_field_data_type(field):
    """Returns the description for a given field type, if it exists,
    Fields' descriptions can contain format strings, which will be interpolated
    against the values of field.__dict__ before being output."""

    return field.description % field.__dict__


class HandlerMethod(object):

    def __init__(self, method, stale=False):
        self.method = method
        self.stale = stale

    def iter_args(self):
        args, _, _, defaults = inspect.getargspec(self.method)  # NOQA

        for idx, arg in enumerate(args):
            if arg in ('self', 'request', 'form'):
                continue

            didx = len(args) - idx

            if defaults and len(defaults) >= didx:
                yield (arg, str(defaults[-didx]))
            else:
                yield (arg, None)

    def get_signature(self, parse_optional=True):
        spec = ""

        for argn, argdef in self.iter_args():
            spec += argn

            if argdef:
                spec += '=%s' % argdef

            spec += ', '

        spec = spec.rstrip(", ")

        if parse_optional:
            return spec.replace("=None", "=<optional>")

        return spec

    signature = property(get_signature)

    def get_fields(self):
        to_update = False
        doc = inspect.getdoc(self.method)
        if not doc and issubclass(self.method.im_class.model, models.Model):
            fields = None
            if self.method.__name__ == 'read':
                fields = self.method.im_class.fields if self.method.im_class.fields else tuple(
                    attr.name for attr in self.method.im_class.model._meta.local_fields)
            elif self.method.__name__ in ('create', 'update'):
                to_update = True
                if hasattr(self.method.im_class, 'form') and \
                   hasattr(self.method.im_class.form, '_meta'):
                    fields = self.method.im_class.form._meta.fields
                else:
                    fields = self.method.im_class.fields
            if fields:
                for field in fields:
                    for mfield in self.method.im_class.model._meta.fields:
                        if mfield.name == field:
                            yield {'name': mfield.name,
                                   'required': not mfield.blank if to_update else False,
                                   'type': get_field_data_type(mfield),
                                   'verbose': mfield.verbose_name,
                                   'help_text': mfield.help_text, }
                            break

    def get_doc(self):
        doc = inspect.getdoc(self.method)
        if not doc and issubclass(self.method.im_class.model, models.Model):
            if self.method.__name__ == 'delete':
                doc = _(
                    'Function deletes object with object_ptr. If you declare "trash" parameter as true, object is marked as trash.')
            elif self.method.__name__ == 'read':
                doc = _(
                    'Function gets info about object and returns following fields:')
            elif hasattr(self.method.im_class, 'form'):
                if self.method.__name__ == 'create':
                    doc = _('Function creates entry with following fields:')
                elif self.method.__name__ == 'update':
                    doc = _('Function updates following fields:')
        return doc

    doc = property(get_doc)

    def get_name(self):
        return self.method.__name__

    name = property(get_name)

    def __repr__(self):
        return "<Method: %s>" % self.name


def _convert(template, params=[]):
    """URI template converter"""
    paths = template % dict([p, "{%s}" % p] for p in params)
    return u'/api%s%s' % (get_script_prefix(), paths)


class HandlerDocumentation(object):

    def __init__(self, handler):
        self.handler = handler

    def get_methods(self, include_default=False):
        for method in self.handler.allowed_methods:
            met = getattr(self.handler, CsrfExemptResource.callmap.get(method))
            stale = inspect.getmodule(met) is handler

            if not self.handler.is_anonymous:
                if met and (not stale or include_default):
                    yield HandlerMethod(met, stale)
            else:
                if not stale or met.__name__ == "read" \
                        and 'GET' in self.allowed_methods:

                    yield HandlerMethod(met, stale)

    def get_all_methods(self):
        return self.get_methods(include_default=True)

    @property
    def is_anonymous(self):
        return handler.is_anonymous

    def get_model(self):
        return getattr(self, 'model', None)

    def get_doc(self):
        return self.handler.__doc__

    doc = property(get_doc)

    @property
    def name(self):
        return self.handler.__name__

    @property
    def display_name(self):
        name = self.handler.__name__.replace('Handler', '')
        try:
            pattern = re.compile('([A-Z][A-Z][a-z])|([a-z][A-Z])')
            name = pattern.sub(
                lambda m: m.group()[:1] + " " + m.group()[1:], name)
        except:
            pass
        return name

    @property
    def allowed_methods(self):
        return self.handler.allowed_methods

    def get_resource_uri_template(self):
        """
        URI template processor.

        See http://bitworking.org/projects/URI-Templates/
        """
        try:
            resource_uri = self.handler.resource_uri()

            components = [None, [], {}]

            for i, value in enumerate(resource_uri):
                components[i] = value

            lookup_view, args, kwargs = components
            lookup_view = get_callable(lookup_view, True)

            possibilities = get_resolver(
                'treeio.core.api.urls').reverse_dict.getlist(lookup_view)

            for possibility, pattern in possibilities:
                for result, params in possibility:
                    if args:
                        if len(args) != len(params):
                            continue
                        return _convert(result, params)
                    else:
                        if set(kwargs.keys()) != set(params):
                            continue
                        return _convert(result, params)

        except:
            return None

    def get_resource_uri_index(self):
        """
        INDEX URI template processor.
        """
        try:
            resource_uri = self.handler.resource_uri()

            components = [None, [], {}]

            for i, value in enumerate(resource_uri):
                components[i] = value

            lookup_view, args, kwargs = components
            # else this url will be in get_resource_uri_template
            if args or kwargs:
                lookup_view = get_callable(lookup_view, True)

                possibilities = get_resolver(
                    'treeio.core.api.urls').reverse_dict.getlist(lookup_view)

                for possibility, pattern in possibilities:
                    for result, params in possibility:
                        if not params:
                            return _convert(result)
        except:
            return None

    resource_uri_template = property(get_resource_uri_template)

    def __repr__(self):
        return u'<Documentation for "%s">' % self.name


def documentation_view(request, module):
    docs = []

    for name, clsmember in inspect.getmembers(get_module(module), inspect.isclass):
        if issubclass(clsmember, handler.BaseHandler) and getattr(clsmember, 'model', None):
            docs.append(generate_doc(clsmember))

    return render_to_response('api/reference.html', {'docs': docs}, RequestContext(request))
