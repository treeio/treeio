# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Hardtree Core decorators for views
"""

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse, NoReverseMatch
from treeio.core.conf import settings
from django.utils.html import escape
from jinja2.loaders import TemplateNotFound
from treeio.core.models import Module
from treeio.core.rss import verify_secret_key
import json
import re


def treeio_login_required(f):
    """ Check that the user has write access to the treeio.core module """

    def wrap(request, *args, **kwargs):
        "Wrap"
        if request.user.is_authenticated():
            user = request.user.get_profile()
            user_modules = user.get_perspective().get_modules()
            all_modules = Module.objects.all()
            active = None
            for module in all_modules:
                try:
                    import_name = module.name + "." + \
                        settings.HARDTREE_MODULE_IDENTIFIER
                    hmodule = __import__(
                        import_name, fromlist=[str(module.name)])
                    urls = hmodule.URL_PATTERNS
                    for regexp in urls:
                        if re.match(regexp, request.path):
                            active = module
                except ImportError:
                    pass
                except AttributeError:
                    pass
            if active:
                if active in user_modules:
                    if user.has_permission(active):
                        return f(request, *args, **kwargs)
                    else:
                        if request.path[:3] == '/m/':
                            return HttpResponseRedirect('/m/user/denied')
                        return HttpResponseRedirect('/user/denied')
                else:
                    if request.path[:3] == '/m/':
                        return HttpResponseRedirect('/m/user/denied')
                    return HttpResponseRedirect('/user/denied')
            else:
                return f(request, *args, **kwargs)
        else:
            if request.path[:3] == '/m/':
                return HttpResponseRedirect('/m/accounts/login')
            if 'response_format' in kwargs and kwargs['response_format'] == 'rss':
                if 'secret' in request.GET and verify_secret_key(request):
                    return f(request, *args, **kwargs)
            return HttpResponseRedirect('/accounts/login')

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__

    return wrap


def module_admin_required(module_name=None):
    """ Check that the user has write access to the treeio.core module """

    if not module_name:
        module_name = 'treeio.core'

    def wrap(f):
        "Wrap"
        def wrapped_f(request, *args, **kwargs):
            "Wrapped"

            if request.user.get_profile().is_admin(module_name):
                return f(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('user_denied'))

        wrapped_f.__doc__ = f.__doc__
        wrapped_f.__name__ = f.__name__

        return wrapped_f

    return wrap


def _is_full_redirect(redirect_url):
    "Returns True if this page requires full reload with AJAX enabled"
    redirect_views = getattr(
        settings, 'HARDTREE_AJAX_RELOAD_ON_REDIRECT', ['user_login'])
    for view in redirect_views:
        url = ''
        try:
            url = reverse(view)
        except NoReverseMatch:
            pass
        if url and url == redirect_url:
            return True
    return False


def handle_response_format(f):
    """ Handle response format for a view """

    def wrap(request, *args, **kwargs):
        "Wrap"
        try:
            if 'response_format' in kwargs:
                response_format = kwargs['response_format']
                if not response_format:
                    response_format = 'html'
                    kwargs['response_format'] = response_format

                response = f(request, *args, **kwargs)
                if response_format == 'ajax':
                    if response.__class__ == HttpResponseRedirect:
                        location = response['Location']
                        if not _is_full_redirect(location):
                            response = HttpResponse(json.dumps({'redirect': location}),
                                                    mimetype=settings.HARDTREE_RESPONSE_FORMATS['ajax'])
                        else:
                            if '.ajax' in location:
                                location = str(location).replace('.ajax', '')
                            response = HttpResponse(json.dumps({'redirect_out': location}),
                                                    mimetype=settings.HARDTREE_RESPONSE_FORMATS['ajax'])
                    elif hasattr(request, 'redirect'):
                        location = request.redirect
                        response = HttpResponse(json.dumps({'redirect': location}),
                                                mimetype=settings.HARDTREE_RESPONSE_FORMATS['ajax'])
                    elif 'Content-Disposition' in response and not response['Content-Type'] in settings.HARDTREE_RESPONSE_FORMATS.values():
                        location = request.get_full_path()
                        if '.ajax' in location:
                            location = str(location).replace('.ajax', '')
                        response = HttpResponse(json.dumps({'redirect_out': location}),
                                                mimetype=settings.HARDTREE_RESPONSE_FORMATS['ajax'])

                return response
            else:
                return f(request, *args, **kwargs)
        except TemplateNotFound:
            response_format = None
            if 'response_format' in kwargs:
                response_format = kwargs['response_format']
            if not response_format:
                response_format = 'html'
                kwargs['response_format'] = response_format
            if settings.DEBUG:
                raise
            raise Http404(
                'This page is not available in ' + response_format.upper() + ' format')

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__

    return wrap


# Forms pre-processing

from django.forms.forms import BoundField


def add_required_label_tag(original_function):
    """Adds the 'required' CSS class and an asterisks to required field labels."""

    def required_label_tag(self, contents=None, attrs=None):
        "Required label tag"
        contents = contents or escape(self.label)
        if self.field.required:
            if not self.label.endswith(" *"):
                self.label += " *"
                contents += " *"
            attrs = {'class': 'required'}
        return original_function(self, contents, attrs)
    return required_label_tag


def preprocess_form():
    "Add Asterisk To Field Labels"
    BoundField.label_tag = add_required_label_tag(BoundField.label_tag)
