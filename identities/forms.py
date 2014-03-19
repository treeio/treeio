# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Identities module forms
"""
from django import forms
from django.core.files.storage import default_storage
from django.template import defaultfilters
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from treeio.core.conf import settings
from treeio.core.models import AccessEntity, Object, ModuleSetting
from treeio.core.decorators import preprocess_form
from treeio.identities.models import Contact, ContactValue, ContactType, ContactField
from unidecode import unidecode
from PIL import Image
import re

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

        self.fields['delete'] = forms.ChoiceField(label=_("With selected"), choices=(('', '-----'), ('delete', _('Delete Completely')),
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


class ContactFieldForm(forms.ModelForm):

    "Contact Field Form"

    def clean_name(self):
        "Ensure the name of the field only contains alphanumeric"
        name = self.cleaned_data['name']
        if not re.match(r'^[a-zA-Z0-9-_]+$', name):
            raise forms.ValidationError(
                _("Sorry, field names can only contain letters, numbers, hyphens (-) and underscores (_)"))
        return name

    def __init__(self, *args, **kwargs):
        super(ContactFieldForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")
        self.fields['label'].label = _("Label")
        self.fields['field_type'].label = _("Field type")
        self.fields['required'].label = _("Required")
        self.fields['details'].label = _("Details")

    class Meta:

        "Fields Form"
        model = ContactField
        fields = ('name', 'label', 'field_type', 'required', 'details')


class ContactTypeForm(forms.ModelForm):

    "Contact Type Form"

    def __init__(self, user, *args, **kwargs):

        super(ContactTypeForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")

        self.fields['fields'].queryset = Object.filter_permitted(
            user, ContactField.objects.all())
        self.fields['fields'].help_text = ''
        self.fields['fields'].label = _("Fields")

        self.fields['details'].label = _("Details")

    def clean_name(self):
        "Ensures a contact with the same name doesn't already exists"
        instance = getattr(self, 'instance', None)
        name = self.cleaned_data['name']
        if instance and not instance.id:
            slug = unicode(name).replace(" ", "-")
            slug = defaultfilters.slugify(unidecode(slug))
            if ContactType.objects.filter(slug=slug).exists():
                raise forms.ValidationError(
                    _("Contact Type with such name already exists."))
        return name

    class Meta:

        "Contact Type Form"
        model = ContactType
        fields = ('name', 'fields', 'details')


class ContactForm(forms.Form):

    """ ContactForm """

    name = forms.CharField(
        max_length=256, widget=forms.TextInput(attrs={'size': '50'}))
    instance = None
    files = {}

    def _get_form_field(self, field, value=None):
        "Generate a Django-friendly field from Hardtree spec in DB"
        form_field = None
        if field.field_type == 'text':
            form_field = forms.CharField(label=field.label, max_length=512,
                                         widget=forms.TextInput(attrs={'size': '30'}))
        elif field.field_type == 'textarea':
            form_field = forms.CharField(label=field.label,
                                         widget=forms.Textarea(attrs={'class': 'no-editor'}))
        elif field.field_type == 'details':
            form_field = forms.CharField(
                label=field.label, widget=forms.Textarea())
        elif field.field_type == 'email':
            form_field = forms.EmailField(
                label=field.label, widget=forms.TextInput(attrs={'size': '30'}))
        elif field.field_type == 'url':
            form_field = forms.URLField(
                label=field.label, widget=forms.TextInput(attrs={'size': '50'}))
        elif field.field_type == 'phone':
            form_field = forms.CharField(label=field.label, max_length=256,
                                         widget=forms.TextInput(attrs={'size': '30'}))
        elif field.field_type == 'picture':
            form_field = forms.ImageField(
                label=field.label, widget=forms.FileInput)
        elif field.field_type == 'date':
            form_field = forms.DateTimeField(label=field.label)
            form_field.widget.attrs.update({'class': 'datetimepicker'})
        form_field.required = field.required

        if value:
            if isinstance(form_field, forms.FileField) and value.value:
                form_field = forms.ChoiceField(
                    label=field.label, widget=forms.RadioSelect())
                filename = full_filename = value.value
                match = re.match('.*[a-z0-9]{32}__(?P<filename>.+)$', filename)
                if match:
                    filename = match.group('filename')
                form_field.choices = ((full_filename, _("Keep existing: ") + unicode(filename)),
                                      ('delete', _("Delete ")))
                form_field.initial = full_filename
                form_field.required = False
            else:
                form_field.initial = value.value

        return form_field

    def _get_free_field_name(self, field):
        "Generate an available name for a field"
        num = 0
        field_name = unicode(field.name) + u"___" + unicode(num)
        while field_name in self.fields:
            num = num + 1
            field_name = unicode(field.name) + u"___" + unicode(num)
        return field_name

    def _get_upload_name(self, filename):
        "Returns an upload_to path to a new file"
        import hashlib
        import random
        while True:
            hasher = hashlib.md5()
            hasher.update(str(random.random()))
            filepath = u"identities/" + hasher.hexdigest() + u"__" + filename
            fullpath = settings.MEDIA_ROOT + filepath
            if not default_storage.exists(fullpath):
                return filepath

    def _handle_uploaded_file(self, field_name):
        "Process an uploaded file"
        try:
            file = self.files[field_name]
            filepath = self._get_upload_name(file.name)
        except KeyError:
            return ''
        destination = open(settings.MEDIA_ROOT + filepath, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        return settings.MEDIA_URL + filepath

    def _image_resize(self, filepath):
        "Resizes Image if it's over the maximum dimension"
        filepath = filepath.replace(settings.MEDIA_URL, '')
        filepath = settings.MEDIA_ROOT + filepath
        try:
            img = Image.open(filepath)
            expected_size = getattr(
                settings, 'HARDTREE_IMAGE_MAX_SIZE', [400, 300])
            if img.size[0] > expected_size[0] or img.size[1] > expected_size[1]:
                filter_name = getattr(
                    settings, 'HARDTREE_IMAGE_RESIZE_FILTER', 'ANTIALIAS')
                filter = getattr(Image, filter_name, Image.ANTIALIAS)
                aspect = img.size[0] / float(img.size[1])
                newsize = list(expected_size)
                if img.size[0] > expected_size[0]:
                    newsize[0] = expected_size[0]
                    newsize[1] = round(newsize[0] / aspect)
                if newsize[1] > expected_size[1]:
                    newsize[1] = expected_size[1]
                    newsize[0] = round(newsize[1] * aspect)
                img = img.resize(newsize, filter)
                img.save(filepath)
        except Exception:
            pass

    def __init__(self, user=None, contact_type=None, *args, **kwargs):
        "Populates form with fields from given ContactType"

        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            values = self.instance.contactvalue_set.all()
            del kwargs['instance']

        super(ContactForm, self).__init__(*args, **kwargs)

        self.fields['parent'] = forms.ModelChoiceField(
            label='Parent', queryset=[], required=False)
        self.fields['parent'].queryset = Object.filter_permitted(
            user, Contact.objects)
        self.fields['parent'].widget.attrs.update({'class': 'autocomplete',
                                                   'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['parent'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})
        self.fields['parent'].label = _('Parent')
        self.fields['name'].label = _('Name')

        if 'files' in kwargs:
            self.files = kwargs['files']

        for field in contact_type.fields.all():
            if self.instance:
                initial_field_name = self._get_free_field_name(field)
                self.fields[initial_field_name] = self._get_form_field(field)
                for value in values:
                    if value.field == field:
                        field_name = self._get_free_field_name(field)
                        self.fields[field_name] = self._get_form_field(
                            field, value)
                        if initial_field_name in self.fields:
                            del self.fields[initial_field_name]
            else:
                field_name = self._get_free_field_name(field)
                self.fields[field_name] = self._get_form_field(field)

        if user.is_admin('treeio.identities'):
            self.fields['related_user'] = forms.ModelChoiceField(label=_('Attach to User'),
                                                                 queryset=[], required=False)
            self.fields['related_user'].queryset = AccessEntity.objects.all()
            self.fields['related_user'].widget.attrs.update({'class': 'autocomplete',
                                                             'callback': reverse('identities_ajax_access_lookup')})
            self.fields['related_user'].label = _('Related user')

        if self.instance:
            self.fields['name'].initial = self.instance.name
            self.fields['parent'].initial = self.instance.parent_id
            if 'related_user' in self.fields:
                self.fields[
                    'related_user'].initial = self.instance.related_user_id

    def save(self, request, contact_type=None):
        "Process form and create DB objects as required"
        if self.instance:
            contact = self.instance
        else:
            contact = Contact()
            contact.contact_type = contact_type

        contact.name = unicode(self.cleaned_data['name'])

        if 'parent' in self.cleaned_data:
            contact.parent = self.cleaned_data['parent']

        if 'related_user' in self.cleaned_data:
            contact.related_user = self.cleaned_data['related_user']

        contact.save()

        if self.instance:
            contact.contactvalue_set.all().delete()
        for field in contact.contact_type.fields.all():
            for form_name in self.cleaned_data:
                if re.match(str("^" + field.name + "___\d+$"), form_name):
                    if isinstance(self.fields[form_name], forms.FileField):
                        value = ContactValue(field=field, contact=contact,
                                             value=self._handle_uploaded_file(form_name))
                        if isinstance(self.fields[form_name], forms.ImageField):
                            self._image_resize(value.value)
                    else:
                        if field.field_type == 'picture' and isinstance(self.fields[form_name],
                                                                        forms.ChoiceField):
                            if self.cleaned_data[form_name] != 'delete':
                                value = ContactValue(field=field, contact=contact,
                                                     value=self.cleaned_data[form_name])
                        else:
                            value = ContactValue(field=field, contact=contact,
                                                 value=self.cleaned_data[form_name])
                    value.save()
        return contact


class FilterForm(forms.ModelForm):

    """ Filter form definition """

    def __init__(self, user, skip=[], *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)

        if 'name' in skip:
            del self.fields['name']
        else:
            self.fields['name'].required = False
            self.fields['name'].label = _("Name")

        if 'contact_type' in skip:
            del self.fields['contact_type']
        else:
            self.fields['contact_type'].queryset = Object.filter_permitted(
                user, ContactType.objects)
            self.fields['contact_type'].required = True
            self.fields['contact_type'].label = _("Contact type")

    class Meta:

        "Filter"
        model = Contact
        fields = ('name', 'contact_type')


class SettingsForm(forms.Form):

    """ Administration settings form """

    default_contact_type = forms.ModelChoiceField(
        label=_('Default Contact Type'), queryset=[])

    def __init__(self, user, *args, **kwargs):
        "Sets choices and initial value"
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['default_contact_type'].queryset = Object.filter_permitted(
            user, ContactType.objects)

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.identities', 'default_contact_type')[0]
            default_task_status = ContactType.objects.get(pk=long(conf.value))
            self.fields[
                'default_contact_type'].initial = default_task_status.id
        except Exception:
            pass

    def save(self):
        "Form processor"
        try:
            ModuleSetting.set_for_module('default_contact_type',
                                         self.cleaned_data[
                                             'default_contact_type'].id,
                                         'treeio.identities')

        except Exception:
            return False
