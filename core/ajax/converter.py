# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Converter for AJAX response

Takes HTML rendered response from Django and return JSON-serializable dict
"""
from django.forms import BaseForm, TextInput, CharField, HiddenInput, MultiValueField, MultiWidget
from django.utils.safestring import mark_safe

from treeio.core.ajax.rules import apply_rules


class MultiHiddenWidget(MultiWidget):

    "Renders multiple hidden widgets for initial values to use in autocomplete"

    def __init__(self, initial=[], choices=[], attrs={}):
        widgets = []
        if initial:
            for i in initial:
                if i:
                    initial_label = ''
                    for choice in choices:
                        if choice[0] == i:
                            initial_label = choice[1]
                            break
                    widgets.append(
                        HiddenInput(attrs=dict(attrs, label=initial_label)))
        super(MultiHiddenWidget, self).__init__(widgets=widgets, attrs=attrs)

    def render(self, name, value, attrs=None):
        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = [u'<span id="%s_%s">' % (u'multi', name)]
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id=id_)
            output.append(widget.render(name, widget_value, final_attrs))
        output.append(u'</span>')
        return mark_safe(self.format_output(output))

    def decompress(self, value):
        if not value:
            value = []
        else:
            value = [value]
        return value


class MultiHiddenField(MultiValueField):

    "Multiple choice hidden field"
    widget = MultiHiddenWidget

    def __init__(self, required=False, widget=None, initial=None, choices=[], fields=[]):
        widget = MultiHiddenWidget(initial=initial, choices=choices)
        super(MultiHiddenField, self).__init__(fields=fields, widget=widget, initial=initial,
                                               required=required, label='', help_text='')

    def compress(self, data_list):
        return data_list


def convert_to_ajax(page, context_instance):
    "Converts Django HTML response into AJAX response represented by a dict()"

    response = apply_rules(page)

    # The following is Deprecated for Django 1.3
    # if 'module_content' in response:
    #    module_content = HttpResponse(response['module_content'], mimetype='text/html')
    #    response['module_content'] = csrf().process_response(context_instance['request'], module_content).content

    return response


def preprocess_context(context):
    "Prepares context to be rendered for AJAX"

    # Process autocomplete-multiple fields
    for key in context:
        if isinstance(context[key], BaseForm):
            form = context[key]
            for fname in form.fields:
                # skip newly added fields to avoid looping infinitely
                if not "autocomplete" in fname:
                    field = form.fields[fname]
                    try:
                        # find autocomplete fields
                        if field.widget.attrs and 'callback' in field.widget.attrs and 'autocomplete' in field.widget.attrs['class']:

                            # save existing attributes
                            old_attrs = field.widget.attrs

                            # replace current widget with hidden input
                            field.widget = HiddenInput()

                            # get the current field value
                            if not field.initial and fname in form.initial:
                                field.initial = form.initial[fname]

                            # if the field has choices replace value with it's
                            # actual label
                            initial_name = field.initial
                            if field.initial and field.choices:
                                for choice in field.choices:
                                    if choice[0] == field.initial:
                                        initial_name = choice[1]
                                        break

                            # create new field
                            new_field = CharField(widget=TextInput(attrs=old_attrs),
                                                  label=field.label,
                                                  required=field.required,
                                                  help_text=field.help_text,
                                                  initial=initial_name)

                            # update fields in context
                            form.fields.update(
                                {fname: field, "autocomplete_" + fname: new_field})
                            if fname in form.errors:
                                form.errors[
                                    "autocomplete_" + fname] = form.errors[fname]
                                del form.errors[fname]

                            # restore original field order
                            order = form.fields.keyOrder
                            order.insert(order.index(fname),
                                         order.pop(order.index("autocomplete_" + fname)))

                    except:
                        pass

    # Process autocomplete fields
    for key in context:
        if isinstance(context[key], BaseForm):
            form = context[key]
            for fname in form.fields:
                # skip newly added fields to avoid looping infinitely
                if not "autocomplete" in fname:
                    field = form.fields[fname]
                    try:
                        # find autocomplete fields
                        if field.widget.attrs and 'callback' in field.widget.attrs and 'multicomplete' in field.widget.attrs['class']:

                            # save existing attributes
                            old_attrs = field.widget.attrs

                            # replace current widget with hidden input
                            field.widget = HiddenInput()

                            # get the current field value
                            if not field.initial and fname in form.initial:
                                field.initial = form.initial[fname]

                            # if the field has choices replace value with it's
                            # actual label
                            initial_name = ''
                            if field.initial and field.choices:
                                for choice in field.choices:
                                    if choice[0] in field.initial:
                                        initial_name += choice[1] + u', '

                            # create new field
                            new_field = CharField(widget=TextInput(attrs=old_attrs),
                                                  label=field.label,
                                                  required=field.required,
                                                  help_text=field.help_text,
                                                  initial=initial_name)

                            # hidden fields
                            hidden_field = MultiHiddenField(fields=[field],
                                                            required=field.required,
                                                            initial=field.initial,
                                                            choices=field.choices)

                            # update fields in context
                            form.fields.update(
                                {fname: hidden_field, "multicomplete_" + fname: new_field})
                            if fname in form.errors:
                                form.errors[
                                    "multicomplete_" + fname] = form.errors[fname]
                                del form.errors[fname]

                            # restore original field order
                            order = form.fields.keyOrder
                            order.insert(order.index(fname),
                                         order.pop(order.index("multicomplete_" + fname)))

                    except:
                        raise

    return context
