# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core module Dashboard views
"""

from treeio.core.rendering import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from treeio.core.decorators import treeio_login_required, handle_response_format
from treeio.core.models import Object, Widget
from treeio.core.dashboard.forms import WidgetForm
from treeio.core.conf import settings
from jinja2 import Markup
import json
import re
import copy


def _preprocess_widget(widget, name):
    "Populates widget with missing fields"

    module_name = widget['module_name']
    import_name = module_name + ".views"
    module_views = __import__(import_name, fromlist=[str(module_name)])
    if hasattr(module_views, name):
        if not 'title' in widget:
            widget['title'] = getattr(module_views, name).__doc__
        widget = copy.deepcopy(widget)

        if not 'view' in widget:
            widget['view'] = getattr(module_views, name)

    return widget


def _get_all_widgets(request):
    "Retrieve widgets from all available modules"

    user = request.user.get_profile()
    perspective = user.get_perspective()
    modules = perspective.get_modules()

    widgets = {}

    # For each Module in the Perspective get widgets
    for module in modules:
        try:
            import_name = module.name + ".widgets"
            module_widget_lib = __import__(
                import_name, fromlist=[str(module.name)])
            module_widgets = module_widget_lib.get_widgets(request)

            # Preprocess widget, ensure it has all required fields
            for name in module_widgets:
                if not 'module_name' in module_widgets[name]:
                    module_widgets[name]['module_name'] = module.name
                if not 'module_title' in module_widgets[name]:
                    module_widgets[name]['module_title'] = module.title
                module_widgets[name] = _preprocess_widget(
                    module_widgets[name], name)

            widgets.update(module_widgets)

        except ImportError:
            pass
        except AttributeError:
            pass

    return widgets


def _get_widget(request, module, widget_name):
    "Gets a widget by name"

    import_name = module.name + ".widgets"
    module_widget_lib = __import__(import_name, fromlist=[str(module.name)])
    module_widgets = module_widget_lib.get_widgets(request)

    widget = {}
    # Preprocess widget, ensure it has all required fields
    for name in module_widgets:
        if name == widget_name:
            widget = module_widgets[name]
            if not 'module_name' in widget:
                widget['module_name'] = module.name
            if not 'module_title' in widget:
                widget['module_title'] = module.title
            widget = _preprocess_widget(widget, widget_name)
            break

    return widget


def _create_widget_object(request, module_name, widget_name):
    "Create a Widget object if one is available for the current user Perspective"

    user = request.user.get_profile()
    perspective = user.get_perspective()
    modules = perspective.get_modules()

    obj = None

    current_module = modules.filter(name=module_name)
    widget = None
    if current_module:
        current_module = current_module[0]
        widget = _get_widget(request, current_module, widget_name)
    if widget:
        obj = Widget(user=user, perspective=perspective)
        obj.module_name = widget['module_name']
        obj.widget_name = widget_name
        obj.save()

    # except Exception:
    #    pass

    return obj


def _get_widget_content(content, response_format='html'):
    "Extracts widget content from rendred HTML"

    widget_content = ""
    regexp = r"<!-- widget_content -->(?P<widget_content>.*?)<!-- /widget_content -->"

    if response_format == 'ajax':
        try:
            ajax_content = json.loads(content)
            widget_content = ajax_content['response'][
                'content']['module_content']
        except:
            blocks = re.finditer(regexp, content, re.DOTALL)
            for block in blocks:
                widget_content = block.group('widget_content').strip()
    else:
        blocks = re.finditer(regexp, content, re.DOTALL)
        for block in blocks:
            widget_content = block.group('widget_content').strip()

    return Markup(widget_content)


@handle_response_format
@treeio_login_required
def index(request, response_format='html'):
    "Homepage"
    trash = Object.filter_by_request(request, manager=Object.objects.filter(trash=True),
                                     mode='r', filter_trash=False).count()
    user = request.user.get_profile()
    perspective = user.get_perspective()
    widget_objects = Widget.objects.filter(user=user, perspective=perspective)
    clean_widgets = []

    for widget_object in widget_objects:
        try:
            module = perspective.get_modules().filter(
                name=widget_object.module_name)[0]
            widget = _get_widget(request, module, widget_object.widget_name)
            if 'view' in widget:
                try:
                    content = unicode(
                        widget['view'](request, response_format=response_format).content, 'utf_8')
                    widget_content = _get_widget_content(
                        content, response_format=response_format)
                except Exception, e:
                    widget_content = ""
                    if settings.DEBUG:
                        widget_content = str(e)

                widget['content'] = widget_content
            if widget:
                widget_object.widget = widget
                clean_widgets.append(widget_object)
        except IndexError:
            widget_object.delete()

    return render_to_response('core/dashboard/index',
                              {'trash': trash,
                               'widgets': clean_widgets},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def dashboard_widget_add(request, module_name=None, widget_name=None, response_format='html'):
    "Add a Widget to the Dashboard"
    trash = Object.filter_by_request(request, manager=Object.objects.filter(trash=True),
                                     mode='r', filter_trash=False).count()

    if module_name and widget_name:
        widget = _create_widget_object(request, module_name, widget_name)
        if widget:
            return HttpResponseRedirect(reverse('core_dashboard_index'))

    widgets = _get_all_widgets(request)

    return render_to_response('core/dashboard/widget_add',
                              {'trash': trash,
                               'widgets': widgets},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def dashboard_widget_edit(request, widget_id, response_format='html'):
    "Edit an existing Widget on the Dashboard"

    user = request.user.get_profile()

    widget_object = get_object_or_404(Widget, pk=widget_id)
    if widget_object.user == user:
        perspective = user.get_perspective()
        module = perspective.get_modules().filter(
            name=widget_object.module_name)[0]
        widget = _get_widget(request, module, widget_object.widget_name)
        widget_object.widget = widget
        if 'view' in widget:
            try:
                content = unicode(
                    widget['view'](request, response_format=response_format).content, 'utf_8')
                widget_content = _get_widget_content(
                    content, response_format=response_format)
            except Exception:
                widget_content = ""
            widget['content'] = widget_content
        if request.POST:
            form = WidgetForm(user, request.POST, instance=widget_object)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('core_dashboard_index'))
        else:
            form = WidgetForm(user, instance=widget_object)
        return render_to_response('core/dashboard/widget_edit',
                                  {'widget': widget_object,
                                   'form': form},
                                  context_instance=RequestContext(request), response_format=response_format)

    return HttpResponseRedirect(reverse('home'))


@handle_response_format
@treeio_login_required
def dashboard_widget_delete(request, widget_id, response_format='html'):
    "Delete an existing Widget from the Dashboard"

    widget = get_object_or_404(Widget, pk=widget_id)

    if widget.user == request.user.get_profile():
        widget.delete()

    return HttpResponseRedirect(reverse('core_dashboard_index'))


@handle_response_format
@treeio_login_required
def dashboard_widget_arrange(request, panel='left', response_format='html'):
    "Arrange widgets with AJAX request"
    user = request.user.get_profile()

    if panel == 'left' or not panel:
        shift = -100
    else:
        shift = 100

    if request.GET and 'id_widget[]' in request.GET:
        widget_ids = request.GET.getlist('id_widget[]')
        widgets = Widget.objects.filter(user=user, pk__in=widget_ids)
        for widget in widgets:
            if unicode(widget.id) in widget_ids:
                widget.weight = shift + widget_ids.index(unicode(widget.id))
                widget.save()

    return HttpResponseRedirect(reverse('core_dashboard_index'))
