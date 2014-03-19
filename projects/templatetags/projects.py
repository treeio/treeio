# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Projects templatetags
"""
from coffin import template
from treeio.core.rendering import render_to_string
from jinja2 import contextfunction, Markup
from django.template import RequestContext

register = template.Library()


@contextfunction
def projects_task_list(context, tasks, time_slots=[], nomass=False,
                       in_progress=False, by_project=False, by_milestone=False,
                       by_assigned=False, noheader=False):
    "Print a list of tasks"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('projects/tags/task_list',
                                   {'tasks': tasks,
                                    'nomass': nomass,
                                    'by_project': by_project,
                                    'by_milestone': by_milestone,
                                    'by_assigned': by_assigned,
                                    'in_progress': in_progress,
                                    'noheader': noheader,
                                    'time_slots': time_slots},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(projects_task_list)


@contextfunction
def projects_time_slot_list(context, time_slots, no_dates=False):
    "Print a list of time slots"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('projects/tags/time_slot_list',
                                   {'time_slots': time_slots,
                                       'no_dates': no_dates},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(projects_time_slot_list)
