# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Events module forms
"""
from django import forms
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from treeio.events.models import Event
from treeio.core.models import Object, Location
from treeio.core.decorators import preprocess_form
import datetime
preprocess_form()


class MassActionForm(forms.Form):

    """ Mass action form for Reports """

    delete = forms.ChoiceField(label=_("Delete"), choices=(('', '-----'), ('delete', _('Delete Completely')),
                                                           ('trash', _('Move to Trash'))), required=False)

    instance = None

    def __init__(self, user, *args, **kwargs):
        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            del kwargs['instance']

        super(MassActionForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        "Process form"

        if self.instance:
            if self.is_valid():
                if self.cleaned_data['delete']:
                    if self.cleaned_data['delete'] == 'delete':
                        self.instance.delete()
                    if self.cleaned_data['delete'] == 'trash':
                        self.instance.trash = True
                        self.instance.save()


class EventForm(forms.ModelForm):

    """ Event form """

    def _set_initial(self, field, value):
        "Sets initial value"

    def __init__(self, user=None, date=None, hour=None, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _('Title')
        self.fields['name'].widget = forms.TextInput(attrs={'size': '30'})
        self.fields['location'].queryset = Object.filter_permitted(
            user, Location.objects, mode='x')
        self.fields['location'].widget.attrs.update(
            {'popuplink': reverse('identities_location_add')})
        self.fields['location'].widget.attrs.update({'class': 'autocomplete',
                                                     'callback': reverse('identities_ajax_location_lookup')})

        self.fields['location'].label = _("Location")
        self.fields['start'].label = _("Start")
        self.fields['end'].label = _("End")
        self.fields['details'].label = _("Details")

        if date:
            rdate = None
            try:
                rdate = datetime.datetime.strptime(date, "%Y-%m-%d")
                if hour:
                    hour = int(hour)
                else:
                    hour = 12
                rdate = datetime.datetime(year=rdate.year,
                                          month=rdate.month,
                                          day=rdate.day,
                                          hour=hour)
                self.fields['end'].initial = rdate
            except ValueError:
                pass

        # Set datepicker
        self.fields['start'].widget.attrs.update({'class': 'datetimepicker'})
        self.fields['end'].widget.attrs.update({'class': 'datetimepicker'})

        if self.fields['start'].initial:
            self.fields['start'].widget.attrs.update(
                {'initial': self.fields['start'].initial.strftime('%s')})

        if self.fields['end'].initial:
            self.fields['end'].widget.attrs.update(
                {'initial': self.fields['end'].initial.strftime('%s')})

        if 'instance' in kwargs:
            instance = kwargs['instance']
            if instance.start:
                self.fields['start'].widget.attrs.update(
                    {'initial': instance.start.strftime('%s')})
            if instance.end:
                self.fields['end'].widget.attrs.update(
                    {'initial': instance.end.strftime('%s')})

    def clean_end(self):
        "Make sure end date is greater than start date, when specified"
        try:
            start = self.cleaned_data['start']
            if start:
                end = self.cleaned_data['end']
                if end < start:
                    raise forms.ValidationError(
                        _("End date can not be before the start date"))
        except:
            pass
        return self.cleaned_data['end']

    class Meta:

        "Event"
        model = Event
        fields = ('name', 'location', 'start', 'end', 'details')


class GoToDateForm(forms.Form):

    """ Go to date form definition """

    def __init__(self, date, *args, **kwargs):
        super(GoToDateForm, self).__init__(*args, **kwargs)

        self.fields['goto'] = forms.DateField(
            label=_("Go to date"), required=False)
        self.fields['goto'].widget.attrs.update({'class': 'datepicker'})


class FilterForm(forms.Form):

    """ Filters for Events """

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)

        self.fields['datefrom'] = forms.DateField(label=_("Date From"))
        self.fields['datefrom'].widget.attrs.update({'class': 'datepicker'})

        self.fields['dateto'] = forms.DateField(label=_("Date To"))
        self.fields['dateto'].widget.attrs.update({'class': 'datepicker'})

    def clean_dateto(self):
        "Clean date_to"
        if not self.cleaned_data['dateto'] >= self.cleaned_data['datefrom']:
            raise forms.ValidationError(
                "From date can not be greater than To date.")
