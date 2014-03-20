# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core Dashboard module forms
"""
from django import forms
from treeio.core.models import Object, Widget, Perspective
from django.utils.translation import ugettext as _
from treeio.core.decorators import preprocess_form
preprocess_form()


class WidgetForm(forms.ModelForm):

    """ Perspective form """

    def __init__(self, user, *args, **kwargs):
        super(WidgetForm, self).__init__(*args, **kwargs)

        self.fields['perspective'].queryset = Object.filter_permitted(
            user, Perspective.objects)
        self.fields['perspective'].label = _("Perspective")
        self.fields['weight'].label = _("Weight")

    class Meta:

        "Widget Form"
        model = Widget
        fields = ('perspective', 'weight')
