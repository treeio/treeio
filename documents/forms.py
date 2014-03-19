# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Documents module forms
"""
from django.forms import ModelForm, CharField, TextInput, ChoiceField, Form
from treeio.documents.models import Folder, Document, File, WebLink
from treeio.core.models import Object
from django.utils.translation import ugettext as _
from treeio.core.decorators import preprocess_form
from django.core.urlresolvers import reverse
preprocess_form()


class MassActionForm(Form):

    """ Mass action form for Reports """

    delete = ChoiceField(label=_("With selected"), choices=(('', '-----'), ('delete', 'Delete Completely'),
                                                            ('trash', 'Move to Trash')), required=False)

    instance = None

    def __init__(self, user, *args, **kwargs):
        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            del kwargs['instance']

        super(MassActionForm, self).__init__(*args, **kwargs)
        self.fields['delete'] = ChoiceField(label=_("With selected"), choices=(('', '-----'),
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


class FolderForm(ModelForm):

    """ Folder form """

    def __init__(self, user, folder_id, *args, **kwargs):
        super(FolderForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")

        self.fields['parent'].label = _("Parent")
        self.fields['parent'].queryset = Object.filter_permitted(
            user, Folder.objects, mode='x')
        if folder_id:
            self.fields['parent'].initial = folder_id

    class Meta:

        "Folder"
        model = Folder
        fields = ('name', 'parent')


class DocumentForm(ModelForm):

    """ Document form """
    title = CharField(widget=TextInput(attrs={'size': '50'}))

    def __init__(self, user, folder_id, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)

        self.fields['title'].label = _("Title")

        self.fields['folder'].label = _("Folder")
        self.fields['folder'].queryset = Object.filter_permitted(
            user, Folder.objects, mode='x')
        self.fields['folder'].widget.attrs.update(
            {'popuplink': reverse('documents_folder_add')})
        if folder_id:
            self.fields['folder'].initial = folder_id
        else:
            try:
                self.fields['folder'].initial = self.fields[
                    'folder'].queryset[0].id
            except:
                pass

        self.fields['body'].label = _("Body")
        self.fields['body'].widget.attrs.update({'class': 'full-editor'})

    class Meta:

        "Document"
        model = Document
        fields = ('title', 'folder', 'body')


class FileForm(ModelForm):

    """ File form """
    name = CharField(widget=TextInput(attrs={'size': '25'}))

    def __init__(self, user, folder_id, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")

        self.fields['folder'].label = _("Folder")
        self.fields['folder'].queryset = Object.filter_permitted(
            user, Folder.objects, mode='x')
        self.fields['folder'].widget.attrs.update(
            {'popuplink': reverse('documents_folder_add')})
        if folder_id:
            self.fields['folder'].initial = folder_id
        else:
            try:
                self.fields['folder'].initial = self.fields[
                    'folder'].queryset[0].id
            except:
                pass

        self.fields['content'].label = _("Content")

    class Meta:

        "File"
        model = File
        fields = ('name', 'folder', 'content')


class WebLinkForm(ModelForm):

    """ WebLink form """

    def __init__(self, user, folder_id, *args, **kwargs):
        super(WebLinkForm, self).__init__(*args, **kwargs)

        self.fields['title'].label = _("Title")
        self.fields['title'].widget = TextInput(attrs={'size': '35'})

        self.fields['url'].label = _("URL")
        self.fields['url'].initial = 'http://'
        self.fields['url'].widget = TextInput(attrs={'size': '50'})

        self.fields['folder'].label = _("Folder")
        self.fields['folder'].queryset = Object.filter_permitted(
            user, Folder.objects, mode='x')
        self.fields['folder'].widget.attrs.update(
            {'popuplink': reverse('documents_folder_add')})

        if folder_id:
            self.fields['folder'].initial = folder_id
        else:
            try:
                self.fields['folder'].initial = self.fields[
                    'folder'].queryset[0].id
            except:
                pass

    class Meta:

        "WebLink"
        model = WebLink
        fields = ('title', 'folder', 'url')


class FilterForm(ModelForm):

    """ Filter form definition """

    def __init__(self, user, skip=[], *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)

        self.fields['title'].label = _("Title")
        self.fields['folder'].label = _("Folder")

        if 'title' in skip:
            del self.fields['title']
        else:
            self.fields['title'].required = False

        if 'folder' in skip:
            del self.fields['folder']
        else:
            self.fields['folder'].queryset = Object.filter_permitted(
                user, Folder.objects, mode='x')
            #self.fields['folder'].required = False
            self.fields['folder'].null = True

    class Meta:

        "Filter"
        model = Document
        fields = ('title', 'folder')
