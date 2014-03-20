# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Project management forms
"""
from django.forms import ModelForm, CharField, TextInput, Form, ModelChoiceField, IntegerField, ChoiceField
from treeio.projects.models import Project, Milestone, Task, TaskTimeSlot, TaskStatus
from treeio.core.models import Object, ModuleSetting, UpdateRecord
from treeio.identities.models import Contact
from datetime import timedelta
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from treeio.core.decorators import preprocess_form
preprocess_form()


class SettingsForm(Form):

    """ Administration settings form """

    default_task_status = ModelChoiceField(
        label='Default Task Status', queryset=[])

    def __init__(self, user, *args, **kwargs):
        "Sets choices and initial value"
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['default_task_status'].queryset = Object.filter_permitted(user,
                                                                              TaskStatus.objects, mode='x')

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.projects', 'default_task_status')[0]
            default_task_status = TaskStatus.objects.get(pk=long(conf.value))
            self.fields['default_task_status'].initial = default_task_status.id
        except Exception:
            pass

    def save(self):
        "Form processor"
        try:
            ModuleSetting.set_for_module('default_task_status',
                                         self.cleaned_data[
                                             'default_task_status'].id,
                                         'treeio.projects')

        except Exception:
            return False


class MassActionForm(Form):

    """ Mass action form for Tasks and Milestones """

    status = ModelChoiceField(queryset=[], required=False)
    project = ModelChoiceField(queryset=[], required=False)
    milestone = ModelChoiceField(queryset=[], required=False)
    delete = ChoiceField(label=_("Delete"), choices=(('', '-----'), ('delete', _('Delete Completely')),
                                                     ('trash', _('Move to Trash'))), required=False)
    instance = None

    def __init__(self, user, *args, **kwargs):
        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            del kwargs['instance']

        super(MassActionForm, self).__init__(*args, **kwargs)

        self.fields['status'].queryset = Object.filter_permitted(
            user, TaskStatus.objects, mode='x')
        self.fields['status'].label = _("Mark as")
        self.fields['project'].queryset = Object.filter_permitted(
            user, Project.objects, mode='x')
        self.fields['project'].label = _("Move to Project")
        self.fields['milestone'].queryset = Object.filter_permitted(
            user, Milestone.objects, mode='x')
        self.fields['milestone'].label = _("Move to Milestone")
        self.fields['delete'] = ChoiceField(label=_("Delete"), choices=(('', '-----'),
                                                                        ('delete', _(
                                                                            'Delete Completely')),
                                                                        ('trash', _('Move to Trash'))), required=False)

    def save(self, *args, **kwargs):
        "Save override to omit empty fields"
        if self.instance:
            if self.is_valid():
                if self.cleaned_data['project']:
                    self.instance.project = self.cleaned_data['project']
                if self.cleaned_data['status']:
                    self.instance.status = self.cleaned_data['status']
                if self.cleaned_data['milestone']:
                    self.instance.milestone = self.cleaned_data['milestone']
                self.instance.save()
                if self.cleaned_data['delete']:
                    if self.cleaned_data['delete'] == 'delete':
                        self.instance.delete()
                    if self.cleaned_data['delete'] == 'trash':
                        self.instance.trash = True
                        self.instance.save()


class ProjectForm(ModelForm):

    """ Project form """
    name = CharField(widget=TextInput(attrs={'size': '50'}))

    def __init__(self, user, project_id, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")

        self.fields['parent'].queryset = Object.filter_permitted(
            user, Project.objects, mode='x')
        self.fields['parent'].label = _("Parent")
        if project_id:
            self.fields['parent'].initial = project_id

        self.fields['manager'].queryset = Object.filter_permitted(
            user, Contact.objects, mode='x')
        self.fields['manager'].label = _("Manager")
        self.fields['manager'].widget.attrs.update({'class': 'autocomplete',
                                                    'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['manager'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})

        self.fields['client'].label = _("Client")
        self.fields['client'].queryset = Object.filter_permitted(
            user, Contact.objects, mode='x')
        self.fields['client'].widget.attrs.update({'class': 'autocomplete',
                                                   'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['client'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})

        self.fields['details'].label = _("Details")

    class Meta:

        "Project"
        model = Project
        fields = ('name', 'parent', 'manager', 'client', 'details')


class MilestoneForm(ModelForm):

    """ Milestone form """
    name = CharField(widget=TextInput(attrs={'size': '50'}))

    def __init__(self, user, project_id, *args, **kwargs):
        super(MilestoneForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")

        self.fields['project'].label = _("Project")
        self.fields['project'].queryset = Object.filter_permitted(
            user, Project.objects, mode='x')
        if project_id:
            self.fields['project'].initial = project_id

        self.fields['status'].label = _("Status")
        self.fields['status'].queryset = Object.filter_permitted(
            user, TaskStatus.objects, mode='x')
        try:
            conf = ModuleSetting.get_for_module(
                'treeio.projects', 'default_task_status')[0]
            self.fields['status'].initial = long(conf.value)
        except Exception:
            pass

        # Set datepicker
        self.fields['start_date'].label = _("Start date")
        self.fields['start_date'].widget.attrs.update(
            {'class': 'datetimepicker'})
        self.fields['end_date'].label = _("End date")
        self.fields['end_date'].widget.attrs.update(
            {'class': 'datetimepicker'})

        if 'instance' in kwargs:
            instance = kwargs['instance']
            if instance.start_date:
                self.fields['start_date'].widget.attrs.update(
                    {'initial': instance.start_date.strftime('%s')})
            if instance.end_date:
                self.fields['end_date'].widget.attrs.update(
                    {'initial': instance.end_date.strftime('%s')})

        self.fields['details'].label = _("Details")

    class Meta:

        "Milestone"
        model = Milestone
        fields = (
            'name', 'project', 'status', 'start_date', 'end_date', 'details')


class TaskForm(ModelForm):

    """ Task form """
    name = CharField(widget=TextInput(attrs={'size': '50'}))

    def __init__(self, user, parent, project_id, milestone_id, *args, **kwargs):
        "Populates form with fields from given Project"
        super(TaskForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")
        self.fields['name'].widget.attrs.update({'class': 'duplicates',
                                                 'callback': reverse('projects_ajax_task_lookup')})

        self.fields['status'].label = _("Status")
        self.fields['status'].queryset = Object.filter_permitted(
            user, TaskStatus.objects, mode='x')
        try:
            conf = ModuleSetting.get_for_module(
                'treeio.projects', 'default_task_status')[0]
            self.fields['status'].initial = long(conf.value)
        except Exception:
            pass

        self.user = user

        self.fields['assigned'].label = _("Assigned")
        self.fields['assigned'].help_text = ""
        self.fields['assigned'].widget.attrs.update({'class': 'multicomplete',
                                                     'callback': reverse('identities_ajax_user_lookup')})

        self.fields['caller'].label = _("Caller")
        self.fields['caller'].queryset = Object.filter_permitted(
            user, Contact.objects, mode='x')

        if not self.instance.id:
            contact = user.get_contact()
            if contact:
                self.fields['caller'].initial = contact.id
                self.instance.caller = contact

        self.fields['caller'].widget.attrs.update({'class': 'autocomplete',
                                                   'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['caller'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})

        self.fields['project'].label = _("Project")
        self.fields['project'].queryset = Object.filter_permitted(
            user, Project.objects, mode='x')
        if project_id:
            self.fields['project'].initial = project_id

        self.fields['milestone'].label = _("Milestone")
        self.fields['milestone'].queryset = Object.filter_permitted(
            user, Milestone.objects, mode='x')
        if milestone_id:
            self.fields['milestone'].initial = milestone_id

        self.fields['parent'].label = _("Parent")
        self.fields['parent'].widget.attrs.update({'class': 'autocomplete',
                                                   'callback': reverse('projects_ajax_task_lookup')})

        self.fields['depends'].label = _("Depends on")
        self.fields['depends'].widget.attrs.update({'class': 'autocomplete',
                                                   'callback': reverse('projects_ajax_task_lookup')})

        self.fields['milestone'].queryset = Object.filter_permitted(
            user, Milestone.objects, mode='x')
        self.fields['parent'].queryset = Object.filter_permitted(
            user, Task.objects, mode='x')

        self.fields['priority'].label = _("Priority")
        self.fields['priority'].initial = 3
        self.fields['priority'].choices = ((5, _('Highest')), (
            4, _('High')), (3, _('Normal')), (2, _('Low')), (1, _('Lowest')))

        self.fields['parent'].queryset = Object.filter_permitted(
            user, Task.objects, mode='x')
        if parent:
            self.fields['parent'].initial = parent.id
            self.fields['project'].initial = parent.project_id
            if parent.milestone_id:
                self.fields['milestone'].initial = parent.milestone_id

        # Set datepicker
        self.fields['start_date'].label = _("Start date")
        self.fields['start_date'].widget.attrs.update(
            {'class': 'datetimepicker'})
        self.fields['end_date'].label = _("End date")
        self.fields['end_date'].widget.attrs.update(
            {'class': 'datetimepicker'})

        if 'instance' in kwargs:
            instance = kwargs['instance']
            if instance.start_date:
                self.fields['start_date'].widget.attrs.update(
                    {'initial': instance.start_date.strftime('%s')})
            if instance.end_date:
                self.fields['end_date'].widget.attrs.update(
                    {'initial': instance.end_date.strftime('%s')})

        self.fields['details'].label = _("Details")
        self.fields['estimated_time'].label = _("Estimated time")
        self.fields['estimated_time'].help_text = _("minutes")

    def old_save(self, *args, **kwargs):
        "Override save to set Subscribers and send Notifications"
        original = None
        original_assigned = []
        if hasattr(self, 'instance'):
            try:
                original = Task.objects.get(pk=self.instance.id)
                original_assigned = list(original.assigned.all())
            except Task.DoesNotExist:
                pass

        instance = super(TaskForm, self).save(*args, **kwargs)

        if original:
            new_assigned = list(self.cleaned_data['assigned'])
            if original_assigned != new_assigned:
                for assignee in new_assigned:
                    self.instance.subscribers.add(assignee)

        return instance

    class Meta:

        "Task"
        model = Task
        fields = ('name', 'parent', 'depends', 'assigned', 'project', 'milestone', 'caller',
                  'priority', 'status', 'start_date', 'end_date', 'estimated_time', 'details')


class TaskTimeSlotForm(ModelForm):

    """ Task time slot form """
    minutes = IntegerField(widget=TextInput(attrs={'size': '5'}))

    def __init__(self, user, task_id, *args, **kwargs):
        super(TaskTimeSlotForm, self).__init__(*args, **kwargs)

        self.fields['time_from'].label = _("Started")
        self.fields['time_to'].label = _("Finished")

        # Set datepicker
        self.fields['time_from'].widget.attrs.update(
            {'class': 'datetimepicker'})
        self.fields['time_to'].widget.attrs.update({'class': 'datetimepicker'})

        if 'instance' in kwargs:
            instance = kwargs['instance']
            if instance.time_from:
                self.fields['time_from'].widget.attrs.update(
                    {'initial': instance.time_from.strftime('%s')})
            if instance.time_to:
                self.fields['time_to'].widget.attrs.update(
                    {'initial': instance.time_to.strftime('%s')})

        self.fields['minutes'].label = _("Minutes")
        self.fields['details'].label = _("Details")
        self.fields['details'].widget.attrs.update({'class': 'no-editor'})

        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            if self.instance.id:
                del self.fields['minutes']
            else:
                del self.fields['time_from']
                del self.fields['time_to']
        else:
            del self.fields['time_from']
            del self.fields['time_to']

    def save(self, *args, **kwargs):
        "Override to auto-set time_from and time_to"
        if hasattr(self, 'instance') and self.instance.time_to and not self.instance.time_from:
            minutes = long(self.cleaned_data['minutes'])
            hours = 0L
            days = 0L
            if minutes >= 1440:
                hours = minutes // 60
                minutes %= 60
            if hours >= 24:
                days = hours // 24
                hours %= 24
            delta = timedelta(days=days, hours=hours, minutes=minutes)
            self.instance.time_from = self.instance.time_to - delta

        return super(TaskTimeSlotForm, self).save(*args, **kwargs)

    class Meta:

        "TaskTimeSlot"
        model = TaskTimeSlot
        fields = ('time_from', 'time_to', 'minutes', 'details')


class TaskStatusForm(ModelForm):

    """ TaskStatus form """
    name = CharField(widget=TextInput(attrs={'size': '30'}))

    def __init__(self, user, *args, **kwargs):
        super(TaskStatusForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")
        self.fields['active'].label = _("Active")
        self.fields['hidden'].label = _("Hidden")
        self.fields['details'].label = _("Details")

    class Meta:

        "TaskStatus"
        model = TaskStatus
        fields = ('name', 'active', 'hidden', 'details')


class FilterForm(ModelForm):

    """ Filter form definition """

    def __init__(self, user, skip=[], *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)

        self.fields['caller'].label = _("Caller")
        if 'caller' in skip:
            del self.fields['caller']
        else:
            self.fields['caller'].queryset = Object.filter_permitted(
                user, Contact.objects, mode='x')
            self.fields['caller'].required = False
            self.fields['caller'].widget.attrs.update({'class': 'autocomplete',
                                                       'callback': reverse('identities_ajax_contact_lookup')})

        self.fields['status'].label = _("Status")
        if 'status' in skip:
            del self.fields['status']
        else:
            self.fields['status'].queryset = Object.filter_permitted(
                user, TaskStatus.objects, mode='x')
            self.fields['status'].required = False

        self.fields['assigned'].label = _("Assigned")
        self.fields['assigned'].widget.attrs.update({'class': 'multicomplete',
                                                     'callback': reverse('identities_ajax_user_lookup')})
        if 'assigned' in skip:
            del self.fields['assigned']
        else:
            self.fields['assigned'].help_text = ""

        self.fields['project'].label = _("Project")
        if 'project' in skip:
            del self.fields['project']
        else:
            self.fields['project'].queryset = Object.filter_permitted(
                user, Project.objects, mode='x')
            self.fields['project'].required = False

        self.fields['milestone'].label = _("Milestone")
        if 'milestone' in skip:
            del self.fields['milestone']
        else:
            self.fields['milestone'].queryset = Object.filter_permitted(
                user, Milestone.objects, mode='x')

    class Meta:

        "FilterForm"
        model = Task
        fields = ('caller', 'status', 'project', 'milestone', 'assigned')


class TaskRecordForm(ModelForm):

    """ TaskRecord form """

    def __init__(self, user, *args, **kwargs):
        super(TaskRecordForm, self).__init__(*args, **kwargs)

        self.fields['body'].required = True
        self.fields['body'].label = _("Details")

    class Meta:

        "TaskRecordForm"
        model = UpdateRecord
        fields = ['body']
