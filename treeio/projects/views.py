# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Project Management module views
"""

from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.db.models import Q
from treeio.core.models import Object, ModuleSetting, UpdateRecord
from treeio.core.views import user_denied
from treeio.core.rendering import render_to_response
from treeio.core.decorators import treeio_login_required, handle_response_format
from treeio.projects.models import Project, Milestone, Task, TaskStatus, TaskTimeSlot
from treeio.projects.forms import ProjectForm, MilestoneForm, TaskForm, FilterForm, TaskRecordForm, \
    MassActionForm, TaskTimeSlotForm, TaskStatusForm, SettingsForm
from django.utils.translation import ugettext as _
from datetime import datetime
import json


def _get_filter_query(args):
    "Creates a query to filter Tasks based on FilterForm arguments"
    query = Q()

    for arg in args:
        if hasattr(Task, arg) and args[arg]:
            kwargs = {str(arg + '__id'): long(args[arg])}
            query = query & Q(**kwargs)

    return query


def _get_default_context(request):
    "Returns default context as a dict()"

    projects = Object.filter_by_request(request, Project.objects)
    statuses = Object.filter_by_request(request, TaskStatus.objects)
    massform = MassActionForm(request.user.get_profile())

    context = {'projects': projects,
               'statuses': statuses,
               'massform': massform}

    return context


def _process_mass_form(f):
    "Pre-process request to handle mass action form for Tasks and Milestones"

    def wrap(request, *args, **kwargs):
        "Wrap"
        if 'massform' in request.POST:
            for key in request.POST:
                if 'mass-milestone' in key:
                    try:
                        milestone = Milestone.objects.get(pk=request.POST[key])
                        form = MassActionForm(
                            request.user.get_profile(), request.POST, instance=milestone)
                        if form.is_valid() and request.user.get_profile().has_permission(milestone, mode='w'):
                            form.save()
                    except Exception:
                        pass
            for key in request.POST:
                if 'mass-task' in key:
                    try:
                        task = Task.objects.get(pk=request.POST[key])
                        form = MassActionForm(
                            request.user.get_profile(), request.POST, instance=task)
                        if form.is_valid() and request.user.get_profile().has_permission(task, mode='w'):
                            form.save()
                    except Exception:
                        pass

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__

    return wrap


@handle_response_format
@treeio_login_required
@_process_mass_form
def index(request, response_format='html'):
    "Project Management index page"

    query = Q(parent__isnull=True)
    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = query & _get_filter_query(request.GET)
        else:
            query = query & Q(
                status__hidden=False) & _get_filter_query(request.GET)
    else:
        query = query & Q(status__hidden=False)

    tasks = Object.filter_by_request(request, Task.objects.filter(query))
    milestones = Object.filter_by_request(
        request, Milestone.objects.filter(status__hidden=False))
    filters = FilterForm(request.user.get_profile(), '', request.GET)

    context = _get_default_context(request)
    context.update({'milestones': milestones,
                    'tasks': tasks,
                    'filters': filters})

    return render_to_response('projects/index', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def index_owned(request, response_format='html'):
    "Tasks owned by current user"

    query = Q(
        parent__isnull=True, caller__related_user=request.user.get_profile())
    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = query & _get_filter_query(request.GET)
        else:
            query = query & Q(
                status__hidden=False) & _get_filter_query(request.GET)
    else:
        query = query & Q(status__hidden=False)

    tasks = Object.filter_by_request(request, Task.objects.filter(query))
    milestones = Object.filter_by_request(
        request, Milestone.objects.filter(status__hidden=False))
    filters = FilterForm(request.user.get_profile(), 'status', request.GET)

    context = _get_default_context(request)
    context.update({'milestones': milestones,
                    'tasks': tasks,
                    'filters': filters})

    return render_to_response('projects/index_owned', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def index_assigned(request, response_format='html'):
    "Tasks assigned to current user"

    query = Q(parent__isnull=True, assigned=request.user.get_profile())
    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = query & _get_filter_query(request.GET)
        else:
            query = query & Q(
                status__hidden=False) & _get_filter_query(request.GET)
    else:
        query = query & Q(status__hidden=False)

    tasks = Object.filter_by_request(request, Task.objects.filter(query))

    milestones = Object.filter_by_request(
        request, Milestone.objects.filter(status__hidden=False))
    filters = FilterForm(request.user.get_profile(), 'assigned', request.GET)

    context = _get_default_context(request)
    context.update({'milestones': milestones,
                    'tasks': tasks,
                    'filters': filters})

    return render_to_response('projects/index_assigned', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def index_by_status(request, status_id, response_format='html'):
    "Sort tasks by status"

    status = get_object_or_404(TaskStatus, pk=status_id)

    if not request.user.get_profile().has_permission(status):
        return user_denied(request, message="You don't have access to this Task Status")

    query = Q(parent__isnull=True, status=status)
    if request.GET:
        query = query & _get_filter_query(request.GET)
    tasks = Object.filter_by_request(request, Task.objects.filter(query))

    milestones = Object.filter_by_request(
        request, Milestone.objects.filter(task__status=status).distinct())
    filters = FilterForm(request.user.get_profile(), 'status', request.GET)

    context = _get_default_context(request)
    context.update({'milestones': milestones,
                    'tasks': tasks,
                    'status': status,
                    'filters': filters})

    return render_to_response('projects/index_by_status', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def index_in_progress(request, response_format='html'):
    "A page with a list of tasks in progress"

    query = Q(parent__isnull=True)
    if request.GET:
        query = query & Q(
            status__hidden=False) & _get_filter_query(request.GET)
    else:
        query = query & Q(status__hidden=False)

    tasks = Object.filter_by_request(request, Task.objects.filter(query))

    milestones = Object.filter_by_request(
        request, Milestone.objects.filter(status__hidden=False))
    filters = FilterForm(request.user.get_profile(), 'status', request.GET)
    time_slots = Object.filter_by_request(
        request, TaskTimeSlot.objects.filter(time_from__isnull=False, time_to__isnull=True))

    context = _get_default_context(request)
    context.update({'milestones': milestones,
                    'tasks': tasks,
                    'filters': filters,
                    'time_slots': time_slots})

    return render_to_response('projects/index_in_progress', context,
                              context_instance=RequestContext(request), response_format=response_format)


#
# Projects
#
@handle_response_format
@treeio_login_required
def project_add(request, response_format='html'):
    "New project form"

    if request.POST:
        if not 'cancel' in request.POST:
            project = Project()
            form = ProjectForm(
                request.user.get_profile(), None, request.POST, instance=project)
            if form.is_valid():
                project = form.save()
                project.set_user_from_request(request)
                return HttpResponseRedirect(reverse('projects_project_view', args=[project.id]))
        else:
            return HttpResponseRedirect(reverse('projects'))
    else:
        form = ProjectForm(request.user.get_profile(), None)

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('projects/project_add', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def project_add_typed(request, project_id=None, response_format='html'):
    "Project add to preselected parent project"

    parent_project = None
    if project_id:
        parent_project = get_object_or_404(Project, pk=project_id)
        if not request.user.get_profile().has_permission(parent_project, mode='x'):
            parent_project = None

    if request.POST:
        if not 'cancel' in request.POST:
            project = Project()
            form = ProjectForm(
                request.user.get_profile(), project_id, request.POST, instance=project)
            if form.is_valid():
                project = form.save()
                project.set_user_from_request(request)
                return HttpResponseRedirect(reverse('projects_project_view', args=[project.id]))
        else:
            return HttpResponseRedirect(reverse('projects'))
    else:
        form = ProjectForm(request.user.get_profile(), project_id)

    context = _get_default_context(request)
    context.update({'form': form, 'project': parent_project})

    return render_to_response('projects/project_add_typed', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def project_view(request, project_id, response_format='html'):
    "Single project view page"

    project = get_object_or_404(Project, pk=project_id)
    if not request.user.get_profile().has_permission(project):
        return user_denied(request, message="You don't have access to this Project")

    query = Q(parent__isnull=True, project=project)
    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = query & _get_filter_query(request.GET)
        else:
            query = query & Q(
                status__hidden=False) & _get_filter_query(request.GET)
    else:
        query = query & Q(status__hidden=False)

    if request.user.get_profile().has_permission(project, mode='r'):
        if request.POST:
            record = UpdateRecord()
            record.record_type = 'manual'
            form = TaskRecordForm(
                request.user.get_profile(), request.POST, instance=record)
            if form.is_valid():
                record = form.save()
                record.set_user_from_request(request)
                record.save()
                record.about.add(project)
                project.set_last_updated()
                return HttpResponseRedirect(reverse('projects_project_view', args=[project.id]))
        else:
            form = TaskRecordForm(request.user.get_profile())
    else:
        form = None

    tasks = Object.filter_by_request(request, Task.objects.filter(query))

    tasks_progress = float(0)
    tasks_progress_query = Object.filter_by_request(
        request, Task.objects.filter(Q(parent__isnull=True, project=project)))
    if tasks_progress_query:
        for task in tasks_progress_query:
            if not task.status.active:
                tasks_progress += 1
        tasks_progress = (tasks_progress / len(tasks_progress_query)) * 100
        tasks_progress = round(tasks_progress, ndigits=1)

    filters = FilterForm(request.user.get_profile(), 'project', request.GET)

    milestones = Object.filter_by_request(request,
                                          Milestone.objects.filter(project=project).filter(status__hidden=False))
    subprojects = Project.objects.filter(parent=project)

    context = _get_default_context(request)
    context.update({'project': project,
                    'milestones': milestones,
                    'tasks': tasks,
                    'tasks_progress': tasks_progress,
                    'record_form': form,
                    'subprojects': subprojects,
                    'filters': filters})

    return render_to_response('projects/project_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def project_edit(request, project_id, response_format='html'):
    "Project edit page"

    project = get_object_or_404(Project, pk=project_id)
    if not request.user.get_profile().has_permission(project, mode='w'):
        return user_denied(request, message="You don't have access to this Project")

    if request.POST:
        if not 'cancel' in request.POST:
            form = ProjectForm(
                request.user.get_profile(), None, request.POST, instance=project)
            if form.is_valid():
                project = form.save()
                return HttpResponseRedirect(reverse('projects_project_view', args=[project.id]))
        else:
            return HttpResponseRedirect(reverse('projects_project_view', args=[project.id]))
    else:
        form = ProjectForm(request.user.get_profile(), None, instance=project)

    context = _get_default_context(request)
    context.update({'form': form, 'project': project})

    return render_to_response('projects/project_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def project_delete(request, project_id, response_format='html'):
    "Project delete"

    project = get_object_or_404(Project, pk=project_id)
    if not request.user.get_profile().has_permission(project, mode='w'):
        return user_denied(request, message="You don't have access to this Project")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                project.trash = True
                project.save()
            else:
                project.delete()
            return HttpResponseRedirect(reverse('projects_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('projects_project_view', args=[project.id]))

    context = _get_default_context(request)
    context.update({'project': project})

    return render_to_response('projects/project_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)


#
# Milestones
#

@handle_response_format
@treeio_login_required
def milestone_add(request, response_format='html'):
    "New milestone form"

    if request.POST:
        if not 'cancel' in request.POST:
            milestone = Milestone()
            form = MilestoneForm(
                request.user.get_profile(), None, request.POST, instance=milestone)
            if form.is_valid():
                milestone = form.save()
                milestone.set_user_from_request(request)
                return HttpResponseRedirect(reverse('projects_milestone_view', args=[milestone.id]))
        else:
            return HttpResponseRedirect(reverse('projects'))
    else:
        form = MilestoneForm(request.user.get_profile(), None)

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('projects/milestone_add', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def milestone_add_typed(request, project_id=None, response_format='html'):
    "Milestone add to preselected project"

    project = None
    if project_id:
        project = get_object_or_404(Project, pk=project_id)
        if not request.user.get_profile().has_permission(project, mode='x'):
            project = None

    if request.POST:
        if not 'cancel' in request.POST:
            milestone = Milestone()
            form = MilestoneForm(
                request.user.get_profile(), project_id, request.POST, instance=milestone)
            if form.is_valid():
                milestone = form.save()
                milestone.set_user_from_request(request)
                return HttpResponseRedirect(reverse('projects_milestone_view', args=[milestone.id]))
        else:
            return HttpResponseRedirect(reverse('projects'))
    else:
        form = MilestoneForm(request.user.get_profile(), project_id)

    context = _get_default_context(request)
    context.update({'form': form, 'project': project})

    return render_to_response('projects/milestone_add_typed', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def milestone_view(request, milestone_id, response_format='html'):
    "Single milestone view page"

    milestone = get_object_or_404(Milestone, pk=milestone_id)
    project = milestone.project
    if not request.user.get_profile().has_permission(milestone):
        return user_denied(request, message="You don't have access to this Milestone")

    query = Q(milestone=milestone, parent__isnull=True)
    if request.GET:
        if 'status' in request.GET and request.GET['status']:
            query = query & _get_filter_query(request.GET)
        else:
            query = query & Q(
                status__hidden=False) & _get_filter_query(request.GET)
        tasks = Object.filter_by_request(request, Task.objects.filter(query))
    else:
        tasks = Object.filter_by_request(request,
                                         Task.objects.filter(query & Q(status__hidden=False)))

    filters = FilterForm(request.user.get_profile(), 'milestone', request.GET)

    tasks_progress = float(0)
    tasks_progress_query = Object.filter_by_request(
        request, Task.objects.filter(Q(parent__isnull=True, milestone=milestone)))
    if tasks_progress_query:
        for task in tasks_progress_query:
            if not task.status.active:
                tasks_progress += 1
        tasks_progress = (tasks_progress / len(tasks_progress_query)) * 100
        tasks_progress = round(tasks_progress, ndigits=1)

    context = _get_default_context(request)
    context.update({'milestone': milestone,
                    'tasks': tasks,
                    'tasks_progress': tasks_progress,
                    'filters': filters,
                    'project': project})

    return render_to_response('projects/milestone_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def milestone_edit(request, milestone_id, response_format='html'):
    "Milestone edit page"

    milestone = get_object_or_404(Milestone, pk=milestone_id)
    project = milestone.project
    if not request.user.get_profile().has_permission(milestone, mode='w'):
        return user_denied(request, message="You don't have access to this Milestone")

    if request.POST:
        if not 'cancel' in request.POST:
            form = MilestoneForm(
                request.user.get_profile(), None, request.POST, instance=milestone)
            if form.is_valid():
                milestone = form.save()
                return HttpResponseRedirect(reverse('projects_milestone_view', args=[milestone.id]))
        else:
            return HttpResponseRedirect(reverse('projects_milestone_view', args=[milestone.id]))
    else:
        form = MilestoneForm(
            request.user.get_profile(), None, instance=milestone)

    context = _get_default_context(request)
    context.update({'form': form,
                    'milestone': milestone,
                    'project': project})

    return render_to_response('projects/milestone_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def milestone_delete(request, milestone_id, response_format='html'):
    "Milestone delete"

    milestone = get_object_or_404(Milestone, pk=milestone_id)
    project = milestone.project
    if not request.user.get_profile().has_permission(milestone, mode='w'):
        return user_denied(request, message="You don't have access to this Milestone")

    query = Q(milestone=milestone, parent__isnull=True)
    if request.GET:
        query = query & _get_filter_query(request.GET)
    tasks = Object.filter_by_request(request, Task.objects.filter(query))

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                milestone.trash = True
                milestone.save()
            else:
                milestone.delete()
            return HttpResponseRedirect(reverse('projects_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('projects_milestone_view', args=[milestone.id]))

    context = _get_default_context(request)
    context.update({'milestone': milestone,
                    'tasks': tasks,
                    'project': project})

    return render_to_response('projects/milestone_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def milestone_set_status(request, milestone_id, status_id, response_format='html'):
    "Milestone quick set: Status"

    milestone = get_object_or_404(Milestone, pk=milestone_id)
    if not request.user.get_profile().has_permission(milestone, mode='x'):
        return user_denied(request, message="You don't have access to this Milestone")

    status = get_object_or_404(TaskStatus, pk=status_id)
    if not request.user.get_profile().has_permission(status):
        return user_denied(request, message="You don't have access to this Milestone Status")

    if not milestone.status == status:
        milestone.status = status
        milestone.save()

    return milestone_view(request, milestone_id, response_format)

#
# Tasks
#


@handle_response_format
@treeio_login_required
def task_add(request, response_format='html'):
    "New task form"

    if request.POST:
        if not 'cancel' in request.POST:
            task = Task()
            form = TaskForm(
                request.user.get_profile(), None, None, None, request.POST, instance=task)
            if form.is_valid():
                task = form.save()
                task.set_user_from_request(request)
                return HttpResponseRedirect(reverse('projects_task_view', args=[task.id]))
        else:
            return HttpResponseRedirect(reverse('projects'))
    else:
        form = TaskForm(request.user.get_profile(), None, None, None)

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('projects/task_add', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def task_add_typed(request, project_id=None, response_format='html'):
    "Task add to preselected project"

    project = None
    if project_id:
        project = get_object_or_404(Project, pk=project_id)
        if not request.user.get_profile().has_permission(project, mode='x'):
            project = None

    if request.POST:
        if not 'cancel' in request.POST:
            task = Task()
            form = TaskForm(
                request.user.get_profile(), None, project_id, None, request.POST, instance=task)
            if form.is_valid():
                task = form.save()
                task.set_user_from_request(request)
                return HttpResponseRedirect(reverse('projects_task_view', args=[task.id]))
        else:
            return HttpResponseRedirect(reverse('projects_project_view', args=[project.id]))
    else:
        form = TaskForm(request.user.get_profile(), None, project_id, None)

    context = _get_default_context(request)
    context.update({'form': form,
                    'project': project})

    return render_to_response('projects/task_add_typed', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def task_add_to_milestone(request, milestone_id=None, response_format='html'):
    "Task add to preselected project"

    milestone = None
    if milestone_id:
        milestone = get_object_or_404(Milestone, pk=milestone_id)
        if not request.user.get_profile().has_permission(milestone, mode='x'):
            milestone = None

    project = milestone.project
    project_id = milestone.project.id

    if request.POST:
        if not 'cancel' in request.POST:
            task = Task()
            form = TaskForm(request.user.get_profile(), None,
                            project_id, milestone_id, request.POST, instance=task)
            if form.is_valid():
                task = form.save()
                task.set_user_from_request(request)
                return HttpResponseRedirect(reverse('projects_task_view', args=[task.id]))
        else:
            return HttpResponseRedirect(reverse('projects_milestone_view', args=[milestone.id]))
    else:
        form = TaskForm(
            request.user.get_profile(), None, project_id, milestone_id)

    context = _get_default_context(request)
    context.update({'form': form,
                    'project': project,
                    'milestone': milestone})

    return render_to_response('projects/task_add_to_milestone', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def task_add_subtask(request, task_id=None, response_format='html'):
    "New subtask form"

    parent = None
    if task_id:
        parent = get_object_or_404(Task, pk=task_id)
        if not request.user.get_profile().has_permission(parent, mode='x'):
            parent = None

    if request.POST:
        if not 'cancel' in request.POST:
            task = Task()
            form = TaskForm(
                request.user.get_profile(), parent, None, None, request.POST, instance=task)
            if form.is_valid():
                task = form.save()
                task.set_user_from_request(request)
                return HttpResponseRedirect(reverse('projects_task_view', args=[parent.id]))
        else:
            return HttpResponseRedirect(reverse('projects_task_view', args=[parent.id]))
    else:
        form = TaskForm(request.user.get_profile(), parent, None, None)

    context = _get_default_context(request)
    context.update({'form': form,
                    'task': parent})

    return render_to_response('projects/task_add_subtask', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def task_view(request, task_id, response_format='html'):
    "Single task view page"

    task = get_object_or_404(Task, pk=task_id)
    if not request.user.get_profile().has_permission(task):
        return user_denied(request, message="You don't have access to this Task")

    if request.user.get_profile().has_permission(task, mode='x'):
        if request.POST:
            if 'add-work' in request.POST:
                return HttpResponseRedirect(reverse('projects_task_time_slot_add', args=[task.id]))
            elif 'start-work' in request.POST:
                return HttpResponseRedirect(reverse('projects_task_view', args=[task.id]))
            record = UpdateRecord()
            record.record_type = 'manual'
            form = TaskRecordForm(
                request.user.get_profile(), request.POST, instance=record)
            if form.is_valid():
                record = form.save()
                record.set_user_from_request(request)
                record.save()
                record.about.add(task)
                task.set_last_updated()
                return HttpResponseRedirect(reverse('projects_task_view', args=[task.id]))
        else:
            form = TaskRecordForm(request.user.get_profile())
    else:
        form = None

    subtasks = Object.filter_by_request(
        request, Task.objects.filter(parent=task))
    time_slots = Object.filter_by_request(
        request, TaskTimeSlot.objects.filter(task=task))

    context = _get_default_context(request)
    context.update({'task': task,
                    'subtasks': subtasks,
                    'record_form': form,
                    'time_slots': time_slots})

    if 'massform' in context and 'project' in context['massform'].fields:
        del context['massform'].fields['project']

    return render_to_response('projects/task_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def task_edit(request, task_id, response_format='html'):
    "Task edit page"

    task = get_object_or_404(Task, pk=task_id)
    if not request.user.get_profile().has_permission(task, mode='w'):
        return user_denied(request, message="You don't have access to this Task")

    if request.POST:
        if not 'cancel' in request.POST:
            form = TaskForm(
                request.user.get_profile(), None, None, None, request.POST, instance=task)
            if form.is_valid():
                task = form.save()
                return HttpResponseRedirect(reverse('projects_task_view', args=[task.id]))
        else:
            return HttpResponseRedirect(reverse('projects_task_view', args=[task.id]))
    else:
        form = TaskForm(
            request.user.get_profile(), None, None, None, instance=task)

    context = _get_default_context(request)
    context.update({'form': form,
                    'task': task})

    return render_to_response('projects/task_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def task_delete(request, task_id, response_format='html'):
    "Task delete"

    task = get_object_or_404(Task, pk=task_id)
    if not request.user.get_profile().has_permission(task, mode='w'):
        return user_denied(request, message="You don't have access to this Task")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                task.trash = True
                task.save()
            else:
                task.delete()
            return HttpResponseRedirect(reverse('projects_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('projects_task_view', args=[task.id]))

    subtasks = Object.filter_by_request(
        request, Task.objects.filter(parent=task))
    time_slots = Object.filter_by_request(
        request, TaskTimeSlot.objects.filter(task=task))

    context = _get_default_context(request)
    context.update({'task': task,
                    'subtasks': subtasks,
                    'time_slots': time_slots})

    return render_to_response('projects/task_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def task_set_status(request, task_id, status_id, response_format='html'):
    "Task quick set: Status"

    task = get_object_or_404(Task, pk=task_id)
    if not request.user.get_profile().has_permission(task, mode='x'):
        return user_denied(request, message="You don't have access to this Task")

    status = get_object_or_404(TaskStatus, pk=status_id)
    if not request.user.get_profile().has_permission(status):
        return user_denied(request, message="You don't have access to this Task Status")

    if not task.status == status:
        task.status = status
        task.save()

    return task_view(request, task_id, response_format)


#
# Task Time Slots
#

@handle_response_format
@treeio_login_required
def task_time_slot_start(request, task_id, response_format='html'):
    "Start TaskTimeSlot for preselected Task"

    task = get_object_or_404(Task, pk=task_id)
    if not request.user.get_profile().has_permission(task, mode='x'):
        return user_denied(request, message="You don't have access to this Task")

    if not task.is_being_done_by(request.user.get_profile()):
        task_time_slot = TaskTimeSlot(
            task=task, time_from=datetime.now(), user=request.user.get_profile())
        task_time_slot.save()
        task_time_slot.set_user_from_request(request)

    return HttpResponseRedirect(reverse('projects_task_view', args=[task_id]))


@handle_response_format
@treeio_login_required
def task_time_slot_stop(request, slot_id, response_format='html'):
    "Stop TaskTimeSlot for preselected Task"

    slot = get_object_or_404(TaskTimeSlot, pk=slot_id)
    if not request.user.get_profile().has_permission(slot, mode='w'):
        return user_denied(request, message="You don't have access to this TaskTimeSlot")

    if request.POST and 'stop' in request.POST:
        slot.time_to = datetime.now()
        slot.details = request.POST['details']
        slot.save()

    return HttpResponseRedirect(reverse('projects_task_view', args=[slot.task_id]))


@handle_response_format
@treeio_login_required
def task_time_slot_add(request, task_id, response_format='html'):
    "Time slot add to preselected task"

    task = get_object_or_404(Task, pk=task_id)
    if not request.user.get_profile().has_permission(task, mode='x'):
        return user_denied(request, message="You don't have access to this Task")

    if request.POST:
        task_time_slot = TaskTimeSlot(
            task=task, time_to=datetime.now(), user=request.user.get_profile())
        form = TaskTimeSlotForm(
            request.user.get_profile(), task_id, request.POST, instance=task_time_slot)
        if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('projects_task_view', args=[task.id]))
        elif form.is_valid():
            task_time_slot = form.save()
            task_time_slot.set_user_from_request(request)
            return HttpResponseRedirect(reverse('projects_task_view', args=[task.id]))
    else:
        form = TaskTimeSlotForm(request.user.get_profile(), task_id)

    subtasks = Object.filter_by_request(
        request, Task.objects.filter(parent=task))
    time_slots = Object.filter_by_request(
        request, TaskTimeSlot.objects.filter(task=task))

    context = _get_default_context(request)
    context.update({'form': form,
                    'task': task,
                    'subtasks': subtasks,
                    'time_slots': time_slots})

    return render_to_response('projects/task_time_add', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def task_time_slot_view(request, time_slot_id, response_format='html'):
    "Task time slot edit page"

    task_time_slot = get_object_or_404(TaskTimeSlot, pk=time_slot_id)
    task = task_time_slot.task
    if not request.user.get_profile().has_permission(task_time_slot) \
            and not request.user.get_profile().has_permission(task):
        return user_denied(request, message="You don't have access to this Task Time Slot")

    context = _get_default_context(request)
    context.update({'task_time_slot': task_time_slot,
                    'task': task})

    return render_to_response('projects/task_time_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def task_time_slot_edit(request, time_slot_id, response_format='html'):
    "Task time slot edit page"

    task_time_slot = get_object_or_404(TaskTimeSlot, pk=time_slot_id)
    task = task_time_slot.task

    if not request.user.get_profile().has_permission(task_time_slot, mode='w') \
            and not request.user.get_profile().has_permission(task, mode='w'):
        return user_denied(request, message="You don't have access to this Task Time Slot")

    if request.POST:
        form = TaskTimeSlotForm(
            request.user.get_profile(), None, request.POST, instance=task_time_slot)
        if form.is_valid():
            task_time_slot = form.save()
            return HttpResponseRedirect(reverse('projects_task_view', args=[task.id]))

        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('projects_task_view', args=[task.id]))
    else:
        form = TaskTimeSlotForm(
            request.user.get_profile(), None, instance=task_time_slot)

    context = _get_default_context(request)
    context.update({'form': form,
                    'task_time_slot': task_time_slot,
                    'task': task})

    return render_to_response('projects/task_time_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def task_time_slot_delete(request, time_slot_id, response_format='html'):
    "Task time slot delete"

    task_time_slot = get_object_or_404(TaskTimeSlot, pk=time_slot_id)
    task = task_time_slot.task

    if not request.user.get_profile().has_permission(task_time_slot, mode='w') \
            and not request.user.get_profile().has_permission(task, mode='w'):
        return user_denied(request, message="You don't have access to this Task Time Slot")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                task_time_slot.trash = True
                task_time_slot.save()
            else:
                task_time_slot.delete()
            return HttpResponseRedirect(reverse('projects_task_view', args=[task.id]))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('projects_task_view', args=[task.id]))

    context = _get_default_context(request)
    context.update({'task_time_slot': task_time_slot,
                    'task': task})

    return render_to_response('projects/task_time_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)

#
# Task Statuses
#


@handle_response_format
@treeio_login_required
def task_status_add(request, response_format='html'):
    "TaskStatus add"

    if not request.user.get_profile().is_admin('treeio.projects'):
        return user_denied(request, message="You don't have administrator access to the Projects module")

    if request.POST:
        if not 'cancel' in request.POST:
            status = TaskStatus()
            form = TaskStatusForm(
                request.user.get_profile(), request.POST, instance=status)
            if form.is_valid():
                status = form.save()
                status.set_user_from_request(request)
                return HttpResponseRedirect(reverse('projects_index_by_status', args=[status.id]))
        else:
            return HttpResponseRedirect(reverse('projects_settings_view'))
    else:
        form = TaskStatusForm(request.user.get_profile())

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('projects/status_add', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def task_status_edit(request, status_id, response_format='html'):
    "TaskStatus edit"

    status = get_object_or_404(TaskStatus, pk=status_id)
    if not request.user.get_profile().has_permission(status, mode='w'):
        return user_denied(request, message="You don't have access to this Task Status")

    if request.POST:
        if not 'cancel' in request.POST:
            form = TaskStatusForm(
                request.user.get_profile(), request.POST, instance=status)
            if form.is_valid():
                status = form.save()
                return HttpResponseRedirect(reverse('projects_index_by_status', args=[status.id]))
        else:
            return HttpResponseRedirect(reverse('projects_index_by_status', args=[status.id]))
    else:
        form = TaskStatusForm(request.user.get_profile(), instance=status)

    context = _get_default_context(request)
    context.update({'form': form,
                    'status': status})

    return render_to_response('projects/status_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def task_status_delete(request, status_id, response_format='html'):
    "TaskStatus delete"

    status = get_object_or_404(TaskStatus, pk=status_id)
    if not request.user.get_profile().has_permission(status, mode='w'):
        return user_denied(request, message="You don't have access to this Task Status")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                status.trash = True
                status.save()
            else:
                status.delete()
            return HttpResponseRedirect(reverse('projects_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('projects_index_by_status', args=[status.id]))

    milestones = Object.filter_by_request(request, Milestone.objects)

    context = _get_default_context(request)
    context.update({'status': status,
                    'milestones': milestones})

    return render_to_response('projects/status_delete', context,
                              context_instance=RequestContext(request), response_format=response_format)


#
# Settings
#

@handle_response_format
@treeio_login_required
def settings_view(request, response_format='html'):
    "Settings"

    if not request.user.get_profile().is_admin('treeio.projects'):
        return user_denied(request, message="You don't have administrator access to the Projects module")

    # default task status
    try:
        conf = ModuleSetting.get_for_module(
            'treeio.projects', 'default_task_status')[0]
        default_task_status = TaskStatus.objects.get(
            pk=long(conf.value), trash=False)
    except Exception:
        default_task_status = None

    statuses = TaskStatus.objects.filter(trash=False)
    context = _get_default_context(request)
    context.update({'default_task_status': default_task_status,
                    'statuses': statuses})

    return render_to_response('projects/settings_view', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def settings_edit(request, response_format='html'):
    "Settings"

    if not request.user.get_profile().is_admin('treeio.projects'):
        return user_denied(request, message="You don't have administrator access to the Projects module")

    form = None
    if request.POST:
        if not 'cancel' in request.POST:
            form = SettingsForm(request.user.get_profile(), request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('projects_settings_view'))
        else:
            return HttpResponseRedirect(reverse('projects_settings_view'))
    else:
        form = SettingsForm(request.user.get_profile())

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('projects/settings_edit', context,
                              context_instance=RequestContext(request), response_format=response_format)

#
# AJAX lookups
#


@treeio_login_required
def ajax_task_lookup(request, response_format='html'):
    "Returns a list of matching tasks"

    tasks = []
    if request.GET and 'term' in request.GET:
        tasks = Task.objects.filter(name__icontains=request.GET['term'])[:10]

    return render_to_response('projects/ajax_task_lookup',
                              {'tasks': tasks},
                              context_instance=RequestContext(request),
                              response_format=response_format)


#
# Widgets
#

@treeio_login_required
def widget_tasks_assigned_to_me(request, response_format='html'):
    "A list of tasks assigned to current user"

    query = Q(parent__isnull=True) & Q(status__hidden=False)

    tasks = Object.filter_by_request(request, Task.objects.filter(query))

    return render_to_response('projects/widgets/tasks_assigned_to_me',
                              {'tasks': tasks},
                              context_instance=RequestContext(request), response_format=response_format)

#
# Gantt Chart
#


@treeio_login_required
def gantt_view(request, project_id, response_format='html'):
    projects = Project.objects.filter(trash=False)
    project = projects.filter(pk=project_id)[0]
    if not project:
        raise Http404
    ganttData = []

    # generate json
    milestones = Milestone.objects.filter(project=project).filter(trash=False)
    for milestone in milestones:
        tasks = Task.objects.filter(milestone=milestone).filter(
            start_date__isnull=False).filter(end_date__isnull=False).filter(trash=False)
        series = []
        for task in tasks:
            tlabel = (
                task.name[:30] + '..') if len(task.name) > 30 else task.name
            tn = '<a href="%s" class="popup-link">%s</a>' % (
                reverse('projects_task_view', args=[task.id]), tlabel)
            series.append({'id': task.id,
                           'name': tn,
                           'label': tlabel,
                           'start': task.start_date.date().isoformat(),
                           'end': task.end_date.date().isoformat()})
        mlabel = (
            milestone.name[:30] + '..') if len(milestone.name) > 30 else milestone.name
        mn = '<a href="%s" class="popup-link projects-milestone">%s</a>' % (
            reverse('projects_milestone_view', args=[milestone.id]), mlabel)
        a = {'id': milestone.id, 'name': mn, 'label': mlabel}
        if series:
            a['series'] = series
        else:
            a['series'] = []
        if milestone.start_date and milestone.end_date:
            a['start'] = milestone.start_date.date().isoformat()
            a['end'] = milestone.end_date.date().isoformat()
            a['color'] = '#E3F3D9'
        if series or (milestone.start_date and milestone.end_date):
            ganttData.append(a)
    unclassified = Task.objects.filter(project=project).filter(milestone__isnull=True).filter(
        start_date__isnull=False).filter(end_date__isnull=False).filter(trash=False)
    series = []
    for task in unclassified:
        tlabel = (task.name[:30] + '..') if len(task.name) > 30 else task.name
        tn = '<a href="%s" class="popup-link">%s</a>' % (
            reverse('projects_task_view', args=[task.id]), tlabel)
        series.append({'id': task.id,
                       'name': tn,
                       'label': tlabel,
                       'start': task.start_date.date().isoformat(),
                       'end': task.end_date.date().isoformat()})
    if series:
        ganttData.append(
            {'id': 0, 'name': _('Unclassified Tasks'), 'series': series})
    if ganttData:
        jdata = json.dumps(ganttData)
    else:
        jdata = None

    return render_to_response('projects/gantt_view',
                              {'jdata': jdata,
                               'project': project,
                               'projects': projects},
                              context_instance=RequestContext(request), response_format=response_format)


#@treeio_login_required
def task_ajax(request, response_format='html'):
    "For AJAX"
    print request
    if request.POST:
        print request.POST

    # return HttpResponse(options,
    # mimetype=settings.HARDTREE_RESPONSE_FORMATS['json'])
