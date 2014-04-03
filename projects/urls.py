# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Projects module URLs
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('treeio.projects.views',
    url(r'^(\.(?P<response_format>\w+))?$',
        'index', name='projects'),
    url(r'^index(\.(?P<response_format>\w+))?/?$',
        'index', name='projects_index'),
    url(r'^task/owned(\.(?P<response_format>\w+))?/?$',
        'index_owned', name='projects_index_owned'),
    url(r'^task/assigned(\.(?P<response_format>\w+))?/?$',
        'index_assigned', name='projects_index_assigned'),
    url(r'^task/in_progress(\.(?P<response_format>\w+))?/?$',
        'index_in_progress', name='projects_tasks_in_progress'),

    # Projects
    url(r'^add(\.(?P<response_format>\w+))?/?$',
        'project_add', name='project_add'),
    url(r'^add/project/(?P<project_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'project_add_typed', name='projects_project_add_typed'),
    url(r'^view/(?P<project_id>\w+)(\.(?P<response_format>\w+))?/?$',
        'project_view', name='projects_project_view'),
    url(r'^edit/(?P<project_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'project_edit', name='projects_project_edit'),
    url(r'^delete/(?P<project_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'project_delete', name='projects_project_delete'),
    url(r'^gantt/(?P<project_id>\w+)(\.(?P<response_format>\w+))?/?$',
        'gantt_view', name='projects_gantt_view'),

    # Milestones
    url(r'^milestone/add(\.(?P<response_format>\w+))?/?$',
        'milestone_add', name='projects_milestone_add'),
    url(r'^milestone/add/project/(?P<project_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'milestone_add_typed', name='projects_milestone_add_typed'),
    url(r'^milestone/view/(?P<milestone_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'milestone_view', name='projects_milestone_view'),
    url(r'^milestone/edit/(?P<milestone_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'milestone_edit', name='projects_milestone_edit'),
    url(r'^milestone/set/(?P<milestone_id>\d+)/status/(?P<status_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'milestone_set_status', name='projects_milestone_set_status'),
    url(r'^milestone/delete/(?P<milestone_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'milestone_delete', name='projects_milestone_delete'),

    # Tasks
    url(r'^task/add(\.(?P<response_format>\w+))?/?$',
        'task_add', name='projects_task_add'),
    url(r'^task/add/project/(?P<project_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'task_add_typed', name='projects_task_add_typed'),
    url(r'^task/add/milestone/(?P<milestone_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'task_add_to_milestone', name='projects_task_add_to_milestone'),
    url(r'^task/view/(?P<task_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'task_view', name='projects_task_view'),
    url(r'^task/edit/(?P<task_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'task_edit', name='projects_task_edit'),
    url(r'^task/set/(?P<task_id>\d+)/status/(?P<status_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'task_set_status', name='projects_task_set_status'),
    url(r'^task/delete/(?P<task_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'task_delete', name='projects_task_delete'),

    # Subtask
    url(r'^task/add/subtask/(?P<task_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'task_add_subtask', name='projects_task_add_subtask'),

    # Times Slots
    url(r'^task/time/(?P<task_id>\w+)/add(\.(?P<response_format>\w+))?/?$',
        'task_time_slot_add', name='projects_task_time_slot_add'),
    url(r'^task/time/(?P<task_id>\w+)/start(\.(?P<response_format>\w+))?/?$',
        'task_time_slot_start', name='projects_task_time_slot_start'),

    url(r'^task/time/stop/(?P<slot_id>\w+)(\.(?P<response_format>\w+))?/?$',
        'task_time_slot_stop', name='projects_task_time_slot_stop'),
    url(r'^task/time/view/(?P<time_slot_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'task_time_slot_view', name='projects_task_time_slot_view'),
    url(r'^task/time/edit/(?P<time_slot_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'task_time_slot_edit', name='projects_task_time_slot_edit'),
    url(r'^task/delete/time/(?P<time_slot_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'task_time_slot_delete', name='projects_task_time_slot_delete'),

    # Task Statuses
    url(r'^task/status/add(\.(?P<response_format>\w+))?/?$',
        'task_status_add', name='projects_task_status_add'),
    url(r'^task/status/view/(?P<status_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'index_by_status', name='projects_index_by_status'),
    url(r'^task/status/edit/(?P<status_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'task_status_edit', name='projects_task_status_edit'),
    url(r'^task/status/delete/(?P<status_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'task_status_delete', name='projects_task_status_delete'),

    # Settings
    url(r'^settings/view(\.(?P<response_format>\w+))?/?$',
        'settings_view', name='projects_settings_view'),
    url(r'^settings/edit(\.(?P<response_format>\w+))?/?$',
        'settings_edit', name='projects_settings_edit'),

    # AJAX lookups
    url(r'^ajax/tasks(\.(?P<response_format>\w+))?/?$',
        'ajax_task_lookup', name='projects_ajax_task_lookup'),
)
