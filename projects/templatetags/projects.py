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
                               {'time_slots': time_slots, 'no_dates': no_dates},
                               context_instance=RequestContext(request),
                               response_format=response_format))

register.object(projects_time_slot_list)

@contextfunction
def breadcrumb(context, object):
    "Print a breadcrumb hierarchy of an object's path"

    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    projects, milestones, tasks = [], [], []

    while True:

        if isinstance(object, Project):
            projects.append(object)
        elif isinstance(object, Milestone):
            milestones.append(object)
        elif isinstance(object, Task):
            tasks.append(object)

        if hasattr(object, 'parent') and object.parent and object.parent != object:
            object = object.parent
        elif hasattr(object, 'milestone') and object.milestone and object.milestone != object:
            object = object.milestone
        elif hasattr(object, 'project') and object.project and object.project != object:
            object = object.project
        else:
            break

    return Markup(render_to_string('projects/tags/breadcrumb',
            {'projects': projects,
             'milestones': milestones,
             'tasks': tasks},
        context_instance=RequestContext(request),
        response_format=response_format))

register.object(breadcrumb)