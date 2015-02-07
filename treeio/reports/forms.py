# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Hardtree Reporting forms
"""

from django import forms
from django.shortcuts import get_object_or_404
from treeio.core.models import Object
from treeio.reports.models import Report, Chart
from django.utils.translation import ugettext as _
from treeio.core.decorators import preprocess_form
from treeio.reports.helpers import loads, dumps

preprocess_form()


class MassActionForm(forms.Form):
    """ Mass action form for Reports """

    delete = forms.ChoiceField(label=_("With selected"), choices=(('', '-----'), ('delete', _('Delete Completely')),
                                                                  ('trash', _('Move to Trash'))), required=False)

    instance = None

    def __init__(self, user, *args, **kwargs):
        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            del kwargs['instance']

        super(MassActionForm, self).__init__(*args, **kwargs)
        self.fields['delete'] = forms.ChoiceField(label=_("With selected"), choices=(('', '-----'),
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
                    if self.cleaned_data['delete'] == 'trash':
                        self.instance.trash = True
                        self.instance.save()


class ObjChoiceForm(forms.Form):
    """ Choose an Object to Report On """

    def __init__(self, user, *args, **kwargs):

        object_types = kwargs.pop('object_types')
        object_names = kwargs.pop('object_names')

        x = ((object_types[i], object_names[i])
             for i in range(0, len(object_types)))

        super(ObjChoiceForm, self).__init__(*args, **kwargs)
        self.fields['choice'] = forms.ChoiceField(
            label=_("Choose an Object to Report on"), choices=(x))


class ReportForm(forms.ModelForm):
    "New report Form"

    def __init__(self, user, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)

    class Meta:

        "Report"
        model = Report
        fields = ('model',)


class SetForm(forms.Form):
    """ Report Set Form """

    def __init__(self, user, *args, **kwargs):
        names = kwargs.pop('names')
        obj = kwargs.pop('obj')
        super(SetForm, self).__init__(*args, **kwargs)

        for i, name in enumerate(names):
            self.fields[names[i]] = forms.BooleanField(
                label=_(names[i].title().replace('_', ' ')), required=False)
            self.fields['obj'] = forms.CharField(
                initial=str(obj), widget=forms.widgets.HiddenInput())


class ChartForm(forms.Form):
    "Google Chart Form"
    CHART_TYPES = (
        ('line', 'line'),
        ('spline', 'spline'),
        ('area', 'area'),
        ('areaspline', 'areaspline'),
        ('column', 'column'),
        ('bar', 'bar'),
        ('pie', 'pie'),
        ('scatter', 'scatter')
    )

    title = forms.CharField(required=False)
    type = forms.ChoiceField(choices=CHART_TYPES)
    grouping = forms.ChoiceField(required=True, label="Grouping")

    def clean_grouping(self):
        data = self.cleaned_data['grouping']
        if not data:
            raise forms.ValidationError(
                _("Please enter a field to group your data by."))
        return data

    def __init__(self, user, *args, **kwargs):
        self.report_id = None
        if 'report_id' in kwargs:
            self.report_id = kwargs.pop('report_id')
        if 'chart_id' in kwargs:
            self.chart_id = kwargs.pop('chart_id')
            chart = get_object_or_404(Chart, pk=self.chart_id)
            self.report_id = chart.report_id

        super(ChartForm, self).__init__(*args, **kwargs)
        if not self.report_id:
            return

        report = get_object_or_404(Report, pk=self.report_id)
        chart = None
        if hasattr(self, 'chart_id'):
            chart = get_object_or_404(Chart, pk=self.chart_id)

        model = loads(report.model)

        object = model.name
        object = object.split('.')

        module_name = object[0] + '.' + object[1] + '.' + object[2]
        import_name = object[3]

        module = __import__(
            module_name, globals(), locals(), [import_name], -1)
        classobj = getattr(module, import_name)

        unfiltered_set = classobj.objects.exclude(trash=True)

        set = []
        for s in unfiltered_set:
            filtered = False
            for field in model.fields:
                if field.filters and str(getattr(s, field.name)) not in field.filters:
                    filtered = True
            if not filtered:
                set.append(s)

        # perhaps do type checking on a setting list of types (for each type)
        self.fields['grouping'].choices = [('', '--------')]

        # Check for group
        groupname = None
        groups = None
        for field in model.fields:
            self.fields['grouping'].choices.append(
                (str(field.name), str(field.name).replace('_', ' ').title()))
            if field.groupby == 1:
                self.fields['grouping'].initial = str(field.name)

        if chart:
            options = loads(chart.options)
            for f in options:
                if f in self.fields:
                    self.fields[f].initial = options[f]

    def save(self):
        if hasattr(self, 'chart_id'):
            chart = get_object_or_404(Chart, pk=self.chart_id)
        else:
            chart = Chart()
            report = get_object_or_404(Report, pk=self.report_id)
            chart.report = report
        chart.name = self.data['title']
        chart.options = dumps(self.data)
        chart.save()
        return chart


class QueryForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        kwargs.pop('names')
        super(QueryForm, self).__init__(*args, **kwargs)


class FilterForm(forms.Form):
    "Filter Form"

    fields = {}

    def __init__(self, user, *args, **kwargs):
        if not (kwargs.has_key('report') and kwargs.has_key('field_name')):
            return
        report = kwargs.pop('report')
        field_name = kwargs.pop('field_name')
        super(FilterForm, self).__init__(*args, **kwargs)

        model = loads(report.model)

        self.report = report
        self.field_name = field_name

        classobj = model.get_class_object()
        field = classobj._meta.get_field_by_name(field_name)[0]
        # TODO: Provisions for ManyToMany fields
        self.fields['operand'] = forms.ChoiceField()
        if field.get_internal_type() == 'ForeignKey':
            self.fields['choice'] = forms.ModelChoiceField(queryset=Object.filter_permitted(user,
                                                                                            field.related.parent_model.objects.all(), mode='x'))
            fc = (('is', 'is'), ('not', 'is not'))
        elif field.get_internal_type() == 'DateTimeField':
            self.fields['choice'] = forms.DateTimeField()
            self.fields['choice'].widget.attrs.update(
                {'class': 'datetimepicker'})
            fc = (('beforedatetime', 'before'), ('afterdatetime', 'after'))
        elif field.get_internal_type() == 'DateField':
            self.fields['choice'] = forms.DateField()
            self.fields['choice'].widget.attrs.update({'class': 'datepicker'})
            fc = (('beforedate', 'before'), (
                'afterdate', 'after'), ('on', 'on'))
        else:
            self.fields['choice'] = field.formfield()
            fc = (('is', 'is'), ('not', 'is not'))

        self.fields['operand'].choices = fc
        self.fields['operand'].label = ""
        self.fields['choice'].label = ""
        self.fields['choice'].help_text = ""

    def save(self):
        # add filter to field
        if not self.data['choice']:
            return
        t = self.report
        model = loads(t.model)
        classobj = model.get_class_object()
        xfield = classobj._meta.get_field_by_name(self.field_name)[0]

        field = model.get_field(self.field_name)
        if not field.filters:
            field.filters = []

        c = self.data['choice']

        type = xfield.get_internal_type()
        if type == 'ManyToManyField':
            c = xfield.related.parent_model.objects.filter(pk=c)[0]
        if type == 'ForeignKey':
            c = xfield.related.parent_model.objects.filter(pk=c)[0]

        display_choice = c
        if hasattr(self.fields['choice'], 'choices'):
            for choice, dc in self.fields['choice'].choices:
                if unicode(c) == unicode(choice):
                    display_choice = dc
                    break

        for choice, dc in self.fields['operand'].choices:
            if unicode(self.data['operand']) == unicode(choice):
                display_operand = dc
                break

        display = "%s %s %s" % (
            field.get_human_name(), display_operand, unicode(display_choice))
        field.filters.append({'choice': c,
                              'operand': self.data['operand'],
                              'display': display
                              })
        t.model = dumps(model)
        t.save()
