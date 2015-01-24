# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Project management: admin page
"""
from treeio.projects.models import Project, Milestone, Task, TaskTimeSlot, TaskStatus
from django.contrib import admin


class ProjectAdmin(admin.ModelAdmin):

    """ Project admin """
    list_display = ('name', 'details', 'parent', 'manager', 'client')
    search_fields = ['name']


class MilestoneAdmin(admin.ModelAdmin):

    """ Milestone admin """
    list_display = ('name', 'details', 'project')
    search_fields = ['name']


class TaskAdmin(admin.ModelAdmin):

    """ Task admin """
    list_display = (
        'name', 'details', 'project', 'priority', 'parent', 'milestone', 'caller')
    search_fields = ['name']


class TaskStatusAdmin(admin.ModelAdmin):

    """ Task status admin """
    list_display = ('name', 'details')
    search_fields = ['name']


class TaskTimeSlotAdmin(admin.ModelAdmin):

    """ Task time slot admin """
    list_display = ('task', 'time_from', 'time_to', 'timezone', 'details')
    date_hierarchy = 'time_from'
    search_fields = ['task']


class TaskRecordAdmin(admin.ModelAdmin):

    """ Task record admin """
    list_display = ('task', 'record_type')
    list_filter = ['record_type']

admin.site.register(Project, ProjectAdmin)
admin.site.register(Milestone, MilestoneAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskStatus, TaskStatusAdmin)
admin.site.register(TaskTimeSlot, TaskTimeSlotAdmin)
