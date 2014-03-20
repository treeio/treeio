# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Changes module forms
"""
from django import forms
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from treeio.changes.models import ChangeSet, ChangeSetStatus
from treeio.core.models import Object, ModuleSetting
from treeio.core.decorators import preprocess_form
from jinja2 import filters
from datetime import datetime
preprocess_form()


class MassActionForm(forms.Form):

    """ Mass action form for Reports """

    delete = forms.ChoiceField(label=_("Delete"), choices=(('', '-----'), ('delete', _('Delete Completely')),
                                                           ), required=False)

    instance = None

    def __init__(self, user, *args, **kwargs):
        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            del kwargs['instance']

        super(MassActionForm, self).__init__(*args, **kwargs)
        self.fields['delete'] = forms.ChoiceField(label=_("Delete"), choices=(('', '-----'),
                                                                              ('delete', _(
                                                                                  'Delete Completely')),
                                                                              ('trash', _('Move to Trash'))), required=False)

    def save(self, *args, **kwargs):
        "Process form"

        if self.instance:
            if self.is_valid():
                if self.cleaned_data['delete']:
                    if self.cleaned_data['delete'] == 'delete':
                        self.instance.delete()


class ObjectModelChoiceField(forms.ModelChoiceField):

    "Object Model Choice Field"

    def label_from_instance(self, obj):
        "Label From Instance"
        name = unicode(obj)
        obj_type = obj.get_human_type()
        label = filters.do_truncate(filters.do_striptags(name), 30)
        if obj_type:
            label += " (" + obj_type + ")"
        return label


class ChangeSetStatusForm(forms.ModelForm):

    """ ChangeSetStatus form """

    def __init__(self, user, *args, **kwargs):
        super(ChangeSetStatusForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")
        self.fields['active'].label = _("Active")
        self.fields['hidden'].label = _("Hidden")
        self.fields['details'].label = _("Details")

    class Meta:

        "ChangeSetStatus"
        model = ChangeSetStatus
        fields = ['name', 'active', 'hidden', 'details']


class ChangeSetForm(forms.ModelForm):

    """ ChangeSet form """

    def __init__(self, user, *args, **kwargs):
        super(ChangeSetForm, self).__init__(*args, **kwargs)

        self.user = None
        if user:
            self.user = user

        self.fields['name'].label = _("Name")
        self.fields['name'].widget.attrs.update({'size': 50})

        self.fields['object'].label = _("Object")
        self.fields['object'] = ObjectModelChoiceField(label=_("Object"),
                                                       queryset=Object.filter_permitted(user,
                                                                                        Object.objects))
        self.fields['object'].widget.attrs.update({'class': 'autocomplete',
                                                   'callback': reverse('core_ajax_object_lookup')})
        if 'object_id' in kwargs:
            self.fields['parent'].initial = kwargs['object_id']
            del kwargs['object_id']

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.changes', 'default_changeset_status')[0]
            default_changeset_status = ChangeSetStatus.objects.get(
                pk=long(conf.value))
            if not default_changeset_status.trash:
                self.fields['status'].initial = default_changeset_status.id
        except Exception:
            pass

        self.fields['status'].label = _("Status")
        self.fields['details'].label = _("Details")

    def save(self, *args, **kwargs):
        "Override Save to mark .resolved*"

        instance = getattr(self, 'instance', None)
        user = getattr(self, 'user', None)

        if instance and user:
            try:
                old_changeset = ChangeSet.objects.get(pk=instance.id)
                if not old_changeset.status == instance.status and not instance.status.active and instance.status.hidden:
                    instance.resolved_by = user
                    instance.resolved_on = datetime.now()
            except ChangeSet.DoesNotExist:
                pass

        return super(ChangeSetForm, self).save(*args, **kwargs)

    class Meta:

        "ChangeSet"
        model = ChangeSet
        fields = ['name', 'object', 'status', 'details']

#
# Filters
#


class FilterForm(forms.ModelForm):

    """ FilterForm definition """

    def __init__(self, user, skip=[], *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)

        if 'author' in skip:
            del self.fields['author']
        else:
            self.fields['author'].required = False
            self.fields['author'].widget.attrs.update({'class': 'autocomplete',
                                                       'callback': reverse('identities_ajax_user_lookup')})
            self.fields['author'].label = _("Author")

        if 'object' in skip:
            del self.fields['object']
        else:
            self.fields['object'] = ObjectModelChoiceField(label=_("Object"),
                                                           queryset=Object.filter_permitted(user,
                                                                                            Object.objects))
            self.fields['object'].required = False
            self.fields['object'].widget.attrs.update({'class': 'autocomplete',
                                                       'callback': reverse('core_ajax_object_lookup')})
            self.fields['object'].label = _("Object")

        if 'resolved_by' in skip:
            del self.fields['resolved_by']
        else:
            self.fields['resolved_by'].required = False
            self.fields['resolved_by'].widget.attrs.update({'class': 'autocomplete',
                                                            'callback': reverse('identities_ajax_user_lookup')})
            self.fields['resolved_by'].label = _("Resolved by")

        if 'status' in skip:
            del self.fields['status']
        else:
            self.fields['status'].queryset = Object.filter_permitted(
                user, ChangeSetStatus.objects)
            self.fields['status'].required = False
            self.fields['status'].label = _("Status")

    class Meta:

        "FilterForm"
        model = ChangeSet
        fields = ('author', 'object', 'resolved_by', 'status')


class SettingsForm(forms.Form):

    """ Administration settings form """

    default_changeset_status = forms.ModelChoiceField(
        label='Default Change Set Status', queryset=[])

    def __init__(self, user, *args, **kwargs):
        "Sets choices and initial value"
        super(SettingsForm, self).__init__(*args, **kwargs)

        self.fields['default_changeset_status'].queryset = ChangeSetStatus.objects.filter(
            trash=False)

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.changes', 'default_changeset_status')[0]
            default_changeset_status = ChangeSetStatus.objects.get(
                pk=long(conf.value))
            if not default_changeset_status.trash:
                self.fields[
                    'default_changeset_status'].initial = default_changeset_status.id
        except Exception:
            pass

    def save(self):
        "Form processor"
        try:
            ModuleSetting.set_for_module('default_changeset_status',
                                         self.cleaned_data[
                                             'default_changeset_status'].id,
                                         'treeio.changes')
            return True

        except Exception:
            return False
