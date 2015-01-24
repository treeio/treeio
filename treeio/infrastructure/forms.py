# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Infrastructure module forms
"""
from django import forms
from treeio.core.conf import settings
from django.core.files.storage import default_storage
from treeio.infrastructure.models import Item, ItemValue, ItemField, ItemType, ItemStatus, ItemServicing
from treeio.finance.models import Asset, Transaction
from treeio.identities.models import Contact
from treeio.core.models import Object, Location, ModuleSetting
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
import re
from PIL import Image
from treeio.core.decorators import preprocess_form
preprocess_form()


class ItemForm(forms.Form):

    "Item Form"
    instance = None
    files = {}

    def _get_form_field(self, field, value=None):
        "Generate a Django-friendly field from Hardtree spec in DB"
        form_field = None
        if field.field_type == 'text':
            form_field = forms.CharField(label=field.label, max_length=512,
                                         widget=forms.TextInput(attrs={'size': '30'}))
        elif field.field_type == 'details':
            form_field = forms.CharField(
                label=field.label, widget=forms.Textarea())
        elif field.field_type == 'url':
            form_field = forms.URLField(
                label=field.label, widget=forms.TextInput(attrs={'size': '50'}))
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
            filepath = u"infrastructure/" + \
                hasher.hexdigest() + u"__" + filename
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

    def __init__(self, user, item_type, *args, **kwargs):
        "Populates form with fields from given AssetType"

        self.item_type = item_type
        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            values = self.instance.itemvalue_set.all()
            del kwargs['instance']

        super(ItemForm, self).__init__(*args, **kwargs)

        if 'files' in kwargs:
            self.files = kwargs['files']

        # Model fields
        self.fields['name'] = forms.CharField(max_length=512,
                                              widget=forms.TextInput(attrs={'size': '50'}))
        self.fields['name'].label = _("Name")
        self.fields['parent'] = forms.ModelChoiceField(
            label=_('Parent'), queryset=[], required=False)
        self.fields['status'] = forms.ModelChoiceField(
            label=_('Status'), queryset=[], required=True)
        self.fields['manufacturer'] = forms.ModelChoiceField(label=_('Manufacturer'),
                                                             queryset=[], required=False)
        self.fields['supplier'] = forms.ModelChoiceField(
            label=_('Supplier'), queryset=[], required=False)
        self.fields['owner'] = forms.ModelChoiceField(
            label=_('Owner'), queryset=[], required=False)
        self.fields['location'] = forms.ModelChoiceField(
            label=_('Location'), queryset=[], required=False)
        self.fields['asset'] = forms.ModelChoiceField(label=_('Asset Record'),
                                                      queryset=[], required=False)

        self.fields['parent'].queryset = Object.filter_permitted(
            user, Item.objects, mode='x')
        self.fields['status'].queryset = Object.filter_permitted(
            user, ItemStatus.objects, mode='x')
        self.fields['manufacturer'].queryset = Object.filter_permitted(
            user, Contact.objects, mode='x')
        self.fields['supplier'].queryset = Object.filter_permitted(
            user, Contact.objects, mode='x')
        self.fields['owner'].queryset = Object.filter_permitted(
            user, Contact.objects, mode='x')
        self.fields['location'].queryset = Object.filter_permitted(
            user, Location.objects, mode='x')
        self.fields['asset'].queryset = Object.filter_permitted(
            user, Asset.objects, mode='x')

        self.fields['manufacturer'].widget.attrs.update({'class': 'autocomplete',
                                                         'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['manufacturer'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})
        self.fields['supplier'].widget.attrs.update({'class': 'autocomplete',
                                                     'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['supplier'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})
        self.fields['owner'].widget.attrs.update({'class': 'autocomplete',
                                                  'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['owner'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})
        #self.fields['asset'].widget.attrs.update({'class': 'autocomplete', 'callback': reverse('finance_ajax_asset_lookup')})

        self.fields['location'].widget.attrs.update(
            {'popuplink': reverse('infrastructure_location_add')})
        self.fields['location'].widget.attrs.update({'class': 'autocomplete',
                                                     'callback': reverse('identities_ajax_location_lookup')})
        self.fields['asset'].widget.attrs.update(
            {'popuplink': reverse('finance_asset_add')})

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.infrastructure', 'default_item_status')[0]
            default_item_status = ItemStatus.objects.get(
                pk=long(conf.value), trash=False)
            self.fields['status'].initial = default_item_status.id
        except Exception:
            pass

        if self.instance:
            self.fields['name'].initial = self.instance.name
            self.fields['status'].initial = self.instance.status_id
            self.fields['parent'].initial = self.instance.parent_id
            self.fields['manufacturer'].initial = self.instance.manufacturer_id
            self.fields['supplier'].initial = self.instance.supplier_id
            self.fields['owner'].initial = self.instance.owner_id
            self.fields['location'].initial = self.instance.location_id
            self.fields['asset'].initial = self.instance.asset_id

        # AssetField <-> AssetValue fields
        for field in item_type.fields.all():
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

    def save(self, request):
        "Process form and create DB objects as required"

        if self.instance:
            item = self.instance
        else:
            item = Item()
            item.item_type = self.item_type

        item.name = unicode(self.cleaned_data['name'])
        item.parent = self.cleaned_data['parent']
        item.status = self.cleaned_data['status']
        item.manufacturer = self.cleaned_data['manufacturer']
        item.supplier = self.cleaned_data['supplier']
        item.owner = self.cleaned_data['owner']
        item.location = self.cleaned_data['location']
        item.asset = self.cleaned_data['asset']

        if not item.id:
            item.set_user_from_request(request)
        item.save()
        if self.instance:
            item.itemvalue_set.all().delete()
        for field in item.item_type.fields.all():
            for form_name in self.cleaned_data:
                if re.match(str("^" + field.name + "___\d+$"), form_name):
                    value = None
                    if isinstance(self.fields[form_name], forms.FileField):
                        value = ItemValue(field=field, item=item,
                                          value=self._handle_uploaded_file(form_name))
                        if isinstance(self.fields[form_name], forms.ImageField):
                            self._image_resize(value.value)
                    else:
                        if field.field_type == 'picture' and isinstance(self.fields[form_name],
                                                                        forms.ChoiceField):
                            if self.cleaned_data[form_name] != 'delete':
                                value = ItemValue(field=field, item=item,
                                                  value=self.cleaned_data[form_name])
                        else:
                            value = ItemValue(
                                field=field, item=item, value=self.cleaned_data[form_name])
                    if value:
                        if not value.value:
                            value.value = ''
                        value.save()

        return item


class ItemFieldForm(forms.ModelForm):

    """ ItemField add/edit form """

    def clean_name(self):
        "Ensure the name of the field only contains alphanumeric"
        name = self.cleaned_data['name']
        if not re.match(r'^[a-zA-Z0-9-_]+$', name):
            raise forms.ValidationError(
                _("Sorry, field names can only contain letters, numbers, hyphens (-) and underscores (_)"))
        return name

    def __init__(self, *args, **kwargs):
        super(ItemFieldForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")
        self.fields['label'].label = _("Label")
        self.fields['field_type'].label = _("Field type")
        self.fields['required'].label = _("Required")
        self.fields['details'].label = _("Details")

    class Meta:

        "Fields Form"
        model = ItemField
        fields = ('name', 'label', 'field_type', 'required', 'details')


class ItemTypeForm(forms.ModelForm):

    """ ItemType add/edit form """

    def __init__(self, user, *args, **kwargs):

        super(ItemTypeForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")
        self.fields['parent'].label = _("Parent")
        self.fields['fields'].label = _("Fields")
        self.fields['details'].label = _("Details")

        self.fields['fields'].queryset = Object.filter_permitted(
            user, ItemField.objects.all(), mode='x')
        self.fields['fields'].help_text = ''
        self.fields['parent'].queryset = Object.filter_permitted(user,
                                                                 ItemType.objects.all().exclude(
                                                                     pk=self.instance.id),
                                                                 mode='x')

    class Meta:

        "Item Type"
        model = ItemType
        fields = ('name', 'parent', 'fields', 'details')


class ItemStatusForm(forms.ModelForm):

    """ ItemStatus add/edit form """

    class Meta:

        "Item Status Form"
        model = ItemStatus
        fields = ('name', 'active', 'hidden', 'details')


class ServiceRecordForm(forms.ModelForm):

    """ ServiceRecord add/edit form """

    def __init__(self, user, service_record=None, *args, **kwargs):
        super(ServiceRecordForm, self).__init__(*args, **kwargs)

        self.fields['items'].queryset = Object.filter_permitted(
            user, Item.objects.all(), mode='x')
        self.fields['items'].help_text = ""
        self.fields['supplier'].queryset = Object.filter_permitted(
            user, Contact.objects.all(), mode='x')
        self.fields['payments'].queryset = Object.filter_permitted(
            user, Transaction.objects.all(), mode='x')
        self.fields['payments'].help_text = ""
        self.fields['payments'].widget.attrs.update(
            {'popuplink': reverse('finance_transaction_add')})

        self.fields['start_date'].widget.attrs.update({'class': 'datepicker'})
        self.fields['expiry_date'].widget.attrs.update({'class': 'datepicker'})

        self.fields['name'].label = _("Name")
        self.fields['items'].label = _("Items")
        self.fields['supplier'].label = _("Supplier")
        self.fields['start_date'].label = _("Start date")
        self.fields['expiry_date'].label = _("Expiry date")
        self.fields['payments'].label = _("Payments")
        self.fields['details'].label = _("Details")

    class Meta:

        "Service Record Form"
        model = ItemServicing
        fields = ('name', 'items', 'supplier', 'start_date',
                  'expiry_date', 'payments', 'details')


class FilterForm(forms.ModelForm):

    """ Item Filters definition """

    def __init__(self, user, skip=[], *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)

        if 'item_type' in skip:
            del self.fields['item_type']
        else:
            self.fields['item_type'].required = False
            self.fields['item_type'].label = _("Item type")

        if 'status' in skip:
            del self.fields['status']
        else:
            self.fields['status'].required = False
            self.fields['status'].label = _("Status")

        if 'owner' in skip:
            del self.fields['owner']
        else:
            self.fields['owner'].widget.attrs.update({'class': 'autocomplete',
                                                      'callback': reverse('identities_ajax_contact_lookup')})
            self.fields['owner'].label = _("Owner")

        self.fields['manufacturer'].widget.attrs.update({'class': 'autocomplete',
                                                         'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['manufacturer'].label = _("Manufacturer")

        self.fields['supplier'].widget.attrs.update({'class': 'autocomplete',
                                                     'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['supplier'].label = _("Supplier")

        self.fields['location'].label = _("Location")

    class Meta:

        "Filter Form"
        model = Item
        fields = ('item_type', 'status', 'manufacturer',
                  'supplier', 'owner', 'location')


class MassActionForm(forms.Form):

    """ Mass action form for Tickets """

    status = forms.ModelChoiceField(queryset=[], required=False)
    location = forms.ModelChoiceField(queryset=[], required=False)
    delete = forms.ChoiceField(label=_("Delete"), choices=(('', '-----'), ('delete', _('Delete Completely')),
                                                           ('trash', _('Move to Trash'))), required=False)
    instance = None

    def __init__(self, user, *args, **kwargs):
        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            del kwargs['instance']

        super(MassActionForm, self).__init__(*args, **kwargs)

        self.fields['status'].queryset = Object.filter_permitted(
            user, ItemStatus.objects, mode='x')
        self.fields['location'].queryset = Object.filter_permitted(
            user, Location.objects, mode='x')

        self.fields['status'].label = _('Status')
        self.fields['location'].label = _('Location')

        self.fields['delete'] = forms.ChoiceField(label=_("Delete"), choices=(('', '-----'),
                                                                              ('delete', _(
                                                                                  'Delete Completely')),
                                                                              ('trash', _('Move to Trash'))), required=False)

    def save(self, *args, **kwargs):
        "Process form"
        if self.instance:
            if self.is_valid():
                if self.cleaned_data['location']:
                    self.instance.location = self.cleaned_data['location']
                if self.cleaned_data['status']:
                    self.instance.status = self.cleaned_data['status']
                self.instance.save()
                if self.cleaned_data['delete']:
                    if self.cleaned_data['delete'] == 'delete':
                        self.instance.delete()
                    if self.cleaned_data['delete'] == 'trash':
                        self.instance.trash = True
                        self.instance.save()


class SettingsForm(forms.Form):

    """ Administration settings form """

    default_item_status = forms.ModelChoiceField(
        label='Default Item Status', queryset=[])

    def __init__(self, user, *args, **kwargs):
        "Sets choices and initial value"
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['default_item_status'].queryset = ItemStatus.objects.filter(
            trash=False)

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.infrastructure', 'default_item_status')[0]
            default_item_status = ItemStatus.objects.get(
                pk=long(conf.value), trash=False)
            self.fields['default_item_status'].initial = default_item_status.id
        except Exception:
            pass

    def save(self):
        "Form processor"
        try:
            ModuleSetting.set_for_module('default_item_status',
                                         self.cleaned_data[
                                             'default_item_status'].id,
                                         'treeio.infrastructure')

        except Exception:
            return False
