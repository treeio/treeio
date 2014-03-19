# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core Trash module forms
"""
from django import forms
from django.utils.translation import ugettext as _


class MassActionForm(forms.Form):

    """ Mass action form for Tickets """

    action = forms.ChoiceField(label=_("Action"),
                               choices=(('', '------'),
                                        ('delete', 'Delete Completely'),
                                        ('delete_all', 'Delete All'),
                                        ('untrash', 'Untrash')),
                               required=False)

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            del kwargs['instance']

        super(MassActionForm, self).__init__(*args, **kwargs)

    def save(self):
        "Process form"
        if self.instance and self.is_valid():
            if self.cleaned_data['action']:
                if self.cleaned_data['action'] == 'delete':
                    self.instance.delete()
                elif self.cleaned_data['action'] == 'untrash':
                    self.instance.trash = False
                    self.instance.save()
        if self.instance and self.cleaned_data['action'] == 'delete_all' and self.is_valid:
            self.instance.delete()
