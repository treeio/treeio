# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Project management models
"""
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from treeio.core.models import Object, User
from treeio.identities.models import Contact
from datetime import datetime, timedelta

# Project Model


class Project(Object):

    """ Project model """
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='child_set')
    manager = models.ForeignKey(
        Contact, related_name='manager', null=True, blank=True, on_delete=models.SET_NULL)
    client = models.ForeignKey(
        Contact, related_name='client', null=True, blank=True, on_delete=models.SET_NULL)
    details = models.TextField(max_length=255, null=True, blank=True)

    class Meta:

        "Project"
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        "Returns absolute URL for the Project"
        try:
            return reverse('projects_project_view', args=[self.id])
        except Exception:
            pass


# TaskStatus model
class TaskStatus(Object):

    """ Tasks and milestones have task statuses """
    name = models.CharField(max_length=255)
    details = models.TextField(max_length=255, null=True, blank=True)
    active = models.BooleanField()
    hidden = models.BooleanField()

    class Meta:

        "TaskStatus"
        ordering = ('hidden', '-active', 'name')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        "Returns absolute URL for the Task Status"
        try:
            return reverse('projects_index_by_status', args=[self.id])
        except Exception:
            pass


# Milestone model
class Milestone(Object):

    """ Tasks may have milestones """
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=255)
    status = models.ForeignKey(TaskStatus)
    details = models.TextField(max_length=255, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    access_inherit = ('project', '*module', '*user')

    class Meta:

        "Milestone"
        ordering = ['start_date', 'name']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        "Override save to update all included tickets if Milestone.project changed"

        if self.id:
            original = Milestone.objects.get(pk=self.id)
            super(Milestone, self).save(*args, **kwargs)
            if self.project != original.project:
                for task in self.task_set.all():
                    task.project = self.project
                    task.save()
        else:
            super(Milestone, self).save(*args, **kwargs)

    def get_absolute_url(self):
        "Returns absolute URL for the Milestone"
        try:
            return reverse('projects_milestone_view', args=[self.id])
        except Exception:
            pass


# Task model
class Task(Object):

    """ Single task """
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='child_set')
    project = models.ForeignKey(Project)
    milestone = models.ForeignKey(Milestone, null=True, blank=True)
    status = models.ForeignKey(TaskStatus, default=26)
    name = models.CharField(max_length=255)
    details = models.TextField(max_length=255, null=True, blank=True)
    assigned = models.ManyToManyField(User, blank=True, null=True)
    depends = models.ForeignKey('Task', blank=True, null=True, related_name='blocked_set',
                                limit_choices_to={'status__hidden': False})
    caller = models.ForeignKey(
        Contact, blank=True, null=True, on_delete=models.SET_NULL)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(default=3,
                                   choices=((5, _('Highest')), (4, _('High')), (3, _('Normal')),
                                            (2, _('Low')), (1, _('Lowest'))))
    estimated_time = models.IntegerField(null=True, blank=True)

    access_inherit = ('parent', 'milestone', 'project', '*module', '*user')

    class Meta:

        "Task"
        ordering = ('-priority', 'name')

    def __unicode__(self):
        return self.name

    def priority_human(self):
        "Returns a Human-friendly priority name"
        choices = ((5, _('Highest')), (4, _('High')), (
            3, _('Normal')), (2, _('Low')), (1, _('Lowest')))
        for choice in choices:
            if choice[0] == self.priority:
                return choice[1]

    def get_estimated_time(self):
        "Converts minutes to Human-friendly time format"
        time = timedelta(minutes=self.estimated_time)
        days = time.days
        seconds = time.seconds
        hours = days * 24 + (seconds // (60 * 60))
        seconds %= (60 * 60)
        minutes = seconds // 60
        seconds %= 60

        string = ""
        if hours or minutes:
            if hours:
                string += _("%2i hours ") % (hours)
            if minutes:
                string += _("%2i minutes") % (minutes)
        else:
            string = _("Less than 1 minute")
        return string

    def save(self, *args, **kwargs):
        "Override save method to check for Milestone-Project links and auto-Status child Tasks"

        original = None
        if self.id:
            # Existing task
            original = Task.objects.get(pk=self.id)
            if self.project_id != original.project_id:
                # Project changed, check milestone is within selected Project
                if self.milestone_id and self.milestone.project_id != self.project_id:
                    self.milestone = None
            elif self.milestone_id and self.milestone_id != original.milestone_id:
                # Milestone changed, check if it belongs to the selected
                # Project
                if self.milestone.project_id != self.project_id:
                    self.project_id = self.milestone.project_id

            if self.status_id != original.status_id:
                # Changed status
                if self.status.hidden:
                    # Changed to a 'hidden' status, perform same for subtasks
                    for task in self.child_set.exclude(status=self.status):
                        task.status_id = self.status_id
                        task.save()
                    # Close any open timeslots
                    for slot in self.tasktimeslot_set.filter(time_to__isnull=True):
                        slot.time_to = datetime.now()
                        slot.save()

        else:
            # New task
            if self.milestone_id and self.milestone.project_id != self.project_id:
                self.project_id = self.milestone.project_id

        # Inherit Project and Milestone from parent if present
        if self.parent_id:
            if self.project_id != self.parent.project_id:
                self.project_id = self.parent.project_id
            if self.milestone_id != self.parent.milestone_id:
                self.milestone_id = self.parent.milestone_id

        super(Task, self).save(*args, **kwargs)

    def get_absolute_url(self):
        "Returns absolute URL"
        try:
            return reverse('projects_task_view', args=[self.id])
        except Exception:
            pass

    def get_total_time(self):
        "Returns total time spent on the task, based on assigned TimeSlots"
        total = timedelta()
        for slot in self.tasktimeslot_set.all():
            total += slot.get_time()
        return total

    def get_total_time_tuple(self):
        "Returns total time as a tuple with number of full hours and minutes"
        time = self.get_total_time()
        if not time:
            return None
        days = time.days
        seconds = time.seconds
        hours = days * 24 + (seconds // (60 * 60))
        seconds %= (60 * 60)
        minutes = seconds // 60
        seconds %= 60
        return (hours, minutes, seconds)

    def get_total_time_string(self):
        "Returns total time as a string with number of full hours and minutes"
        time = self.get_total_time_tuple()
        if not time:
            return _("0 minutes")
        hours = time[0]
        minutes = time[1]
        string = ""
        if hours or minutes:
            if hours:
                string += _("%2i hours ") % (hours)
            if minutes:
                string += _("%2i minutes") % (minutes)
        else:
            string = _("Less than 1 minute")
        return string

    def is_being_done_by(self, user):
        "Returns true if the task is in progress"
        if self.tasktimeslot_set.filter(user=user, time_to__isnull=True).exists():
            return True
        else:
            return False


# TaskTimeSlot model
class TaskTimeSlot(Object):

    """ Task time slot """
    task = models.ForeignKey(Task)
    user = models.ForeignKey(User)
    time_from = models.DateTimeField()
    time_to = models.DateTimeField(null=True, blank=True)
    timezone = models.IntegerField(default=0)
    details = models.TextField(max_length=255, null=True, blank=True)

    access_inherit = ('task', '*module', '*user')

    searchable = False
    attached = True

    class Meta:

        "TaskTimeSlot"
        ordering = ['-date_created']

    def __unicode__(self):
        return unicode(self.task)

    def get_absolute_url(self):
        "Returns absolute URL"
        try:
            return reverse('projects_task_view', args=[self.task_id])
        except Exception:
            pass

    def get_time_secs(self):
        "Return time from epoch"
        time = datetime.now() - self.time_from
        seconds = time.days * 24 * 3600 + time.seconds
        return seconds

    def get_time(self):
        "Returns time"
        if self.time_from and self.time_to:
            return self.time_to - self.time_from
        else:
            return timedelta()

    def get_time_tuple(self, time=None):
        "Returns time as a tuple with number of full hours and minutes"
        if not time:
            time = self.get_time()
        if not time:
            return None
        days = time.days
        seconds = time.seconds
        hours = days * 24 + (seconds // (60 * 60))
        seconds %= (60 * 60)
        minutes = seconds // 60
        seconds %= 60
        return (hours, minutes, seconds)

    def get_time_string(self, time=None):
        "Returns time in string format"
        time = self.get_time_tuple(time)
        if not time and self.time_from:
            return self.get_time_string(datetime.now() - self.time_from)
        elif not time:
            return ""
        hours = time[0]
        minutes = time[1]
        string = ""
        if hours or minutes:
            if hours:
                string += _("%2i hours ") % (hours)
            if minutes:
                string += _("%2i minutes") % (minutes)
        else:
            string = _("Less than 1 minute")
        return string

    def is_open(self):
        "If task is open"
        if self.time_from and self.time_to:
            return False
        return True
