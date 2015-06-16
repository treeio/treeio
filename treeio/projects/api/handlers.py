# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

# -*- coding: utf-8 -*-

from __future__ import absolute_import, with_statement

__all__ = ['ProjectHandler', 'TaskStatusHandler', 'MilestoneHandler',
           'TaskHandler', 'StartTaskTimeHandler', 'StopTaskTimeHandler',
           'TaskTimeHandler']

from datetime import datetime
from treeio.core.api.utils import rc
from piston3.handler import BaseHandler
from treeio.core.api.handlers import ObjectHandler
from treeio.projects.models import Task, Project, Milestone, TaskStatus, TaskTimeSlot
from treeio.projects.forms import ProjectForm, TaskForm, MilestoneForm, TaskStatusForm, TaskTimeSlotForm


def check_parent_perm(request, model, pk, mode):
    try:
        parent_obj = model.objects.get(pk=pk)
        return request.user.profile.has_permission(parent_obj, mode=mode)
    except model.DoesNotExist:
        pass
    return True


class ProjectHandler(ObjectHandler):
    "Entrypoint for Project model."

    model = Project
    form = ProjectForm

    def flatten_dict(self, dct):
        dct = super(ProjectHandler, self).flatten_dict(dct)
        dct['project_id'] = None
        return dct

    def check_create_permission(self, request, mode):
        if 'parent' in request.data:
            return check_parent_perm(request, Project, request.data['parent'], mode)
        return True

    @classmethod
    def resource_uri(cls, obj=None):
        object_id = "id"
        if obj is not None:
            object_id = obj.id
        return ('api_projects', [object_id])


class TaskStatusHandler(ObjectHandler):
    "Entrypoint for TaskStatus model."

    model = TaskStatus
    form = TaskStatusForm

    def check_create_permission(self, request, mode):
        return request.user.profile.is_admin('treeio.projects')

    @classmethod
    def resource_uri(cls, obj=None):
        object_id = "id"
        if obj is not None:
            object_id = obj.id
        return ('api_projects_status', [object_id])


class MilestoneHandler(ObjectHandler):
    "Entrypoint for Milestone model."

    model = Milestone
    form = MilestoneForm

    def flatten_dict(self, dct):
        dct = super(MilestoneHandler, self).flatten_dict(dct)
        dct['project_id'] = None
        return dct

    def check_create_permission(self, request, mode):
        if 'project' in request.data:
            return check_parent_perm(request, Project, request.data['project'], mode)
        return True

    @classmethod
    def resource_uri(cls, obj=None):
        object_id = "id"
        if obj is not None:
            object_id = obj.id
        return ('api_projects_milestones', [object_id])


class TaskHandler(ObjectHandler):
    "Entrypoint for Task model."

    model = Task
    form = TaskForm

    def flatten_dict(self, dct):
        dct = super(TaskHandler, self).flatten_dict(dct)
        dct['parent'] = None
        dct['project_id'] = None
        dct['milestone_id'] = None
        return dct

    def check_create_permission(self, request, mode):
        if 'project' in request.data and not check_parent_perm(request, Project, request.data['project'], mode):
            return False
        if 'milestone' in request.data and not check_parent_perm(request, Milestone, request.data['milestone'], mode):
            return False
        if 'parent' in request.data and not check_parent_perm(request, Task, request.data['parent'], mode):
            return False
        else:
            request.data.setdefault('parent', None)
        return True

    @classmethod
    def resource_uri(cls, obj=None):
        object_id = "id"
        if obj is not None:
            object_id = obj.id
        return ('api_projects_tasks', [object_id])


class StartTaskTimeHandler(BaseHandler):
    "Start TaskTimeSlot for preselected Task"

    # model = True  # for auto documentation
    allowed_methods = ('GET',)

    def read(self, request, task_id, *args, **kwargs):
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return rc.NOT_FOUND

        if not request.user.profile.has_permission(task, mode='x'):
            return rc.FORBIDDEN

        if not task.is_being_done_by(request.user.profile):
            task_time_slot = TaskTimeSlot(
                task=task, time_from=datetime.now(), user=request.user.profile)
            task_time_slot.save()
            task_time_slot.set_user_from_request(request)
            return task_time_slot
        return ("The task isn't in progress", 401)

    @classmethod
    def resource_uri(cls, obj=None):
        object_id = "task_id"
        if obj is not None:
            object_id = obj.id
        return ('api_projects_tasktime_start', [object_id])


class StopTaskTimeHandler(BaseHandler):
    "Stop TaskTimeSlot for preselected Task"

    # model = True  # for auto documentation
    allowed_methods = ('POST',)

    def create(self, request, slot_id, *args, **kwargs):
        try:
            slot = TaskTimeSlot.objects.get(pk=slot_id)
        except Task.DoesNotExist:
            return rc.NOT_FOUND

        if not request.user.profile.has_permission(slot, mode='x'):
            return rc.FORBIDDEN

        slot.time_to = datetime.now()
        slot.details = request.data.get('details', '')
        slot.save()

        return rc.ALL_OK

    @classmethod
    def resource_uri(cls, obj=None):
        object_id = "slot_id"
        if obj is not None:
            object_id = obj.id
        return ('api_projects_tasktime_stop', [object_id])


class TaskTimeHandler(ObjectHandler):
    "Entrypoint for TaskTime model."

    model = TaskTimeSlot
    form = TaskTimeSlotForm

    def flatten_dict(self, dct):
        dct = super(TaskTimeHandler, self).flatten_dict(dct)
        dct['task_id'] = None
        return dct

    def create_instance(self, request, *args, **kwargs):
        return TaskTimeSlot(task=request.task, time_to=datetime.now(), user=request.user.profile)

    def check_create_permission(self, request, mode):
        if "task" in request.data:
            try:
                parent_obj = Task.objects.get(pk=request.data["task"])
                request.task = parent_obj
                return request.user.profile.has_permission(parent_obj, mode=mode)
            except Task.DoesNotExist:
                pass
        return False

    def check_instance_permission(self, request, task_time_slot, mode):
        if not request.user.profile.has_permission(task_time_slot, mode=mode) \
                and not request.user.profile.has_permission(task_time_slot.task, mode=mode):
            return False
        return True

    @classmethod
    def resource_uri(cls, obj=None):
        object_id = "id"
        if obj is not None:
            object_id = obj.id
        return ('api_projects_tasktimes', [object_id])
