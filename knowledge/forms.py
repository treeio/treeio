# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Knowledge base model forms
"""
from django.forms import ModelForm, Form, ChoiceField
from treeio.knowledge.models import KnowledgeFolder, KnowledgeItem, KnowledgeCategory
from treeio.core.models import Object
from treeio.core.decorators import preprocess_form
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
preprocess_form()


class MassActionForm(Form):

    """ Mass action form for Reports """

    delete = ChoiceField(label=_("Delete"), choices=(('', '-----'), ('delete', _('Delete Completely')),
                                                     ('trash', _('Move to Trash'))), required=False)

    instance = None

    def __init__(self, user, *args, **kwargs):
        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            del kwargs['instance']

        super(MassActionForm, self).__init__(*args, **kwargs)
        self.fields['delete'] = ChoiceField(label=_("Delete"), choices=(('', '-----'),
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


class KnowledgeFolderForm(ModelForm):

    """ Knowledge folder form """

    def __init__(self, user, knowledgeType_id, *args, **kwargs):
        super(KnowledgeFolderForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")

        self.fields['parent'].label = _("Parent")
        self.fields['parent'].queryset = KnowledgeFolder.objects

        self.fields['parent'].queryset = Object.filter_permitted(
            user, KnowledgeFolder.objects, mode='x')
        if knowledgeType_id:
            self.fields['parent'].initial = knowledgeType_id

        self.fields['details'].label = _("Details")

    class Meta:

        "KnowledgeFolder"
        model = KnowledgeFolder
        fields = ('name', 'parent', 'details')


class KnowledgeItemForm(ModelForm):

    """ Knowledge item form """

    def __init__(self, user, knowledgeType_id, *args, **kwargs):
        super(KnowledgeItemForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")

        self.fields['folder'].label = _("Folder")
        self.fields['folder'].queryset = Object.filter_permitted(
            user, KnowledgeFolder.objects, mode='x')
        self.fields['folder'].widget.attrs.update(
            {'popuplink': reverse('knowledge_folder_add')})
        if knowledgeType_id:
            self.fields['folder'].initial = knowledgeType_id

        self.fields['category'].label = _("Category")
        self.fields['category'].queryset = Object.filter_permitted(
            user, KnowledgeCategory.objects, mode='x')
        self.fields['category'].widget.attrs.update(
            {'popuplink': reverse('knowledge_category_add')})

        self.fields['body'].label = _("Body")
        self.fields['body'].widget.attrs.update({'class': 'full-editor'})

    class Meta:

        "KnowledgeItem"
        model = KnowledgeItem
        fields = ('name', 'folder', 'category', 'body')


class KnowledgeCategoryForm(ModelForm):

    """ Knowledge category form """

    def __init__(self, *args, **kwargs):
        super(KnowledgeCategoryForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")
        self.fields['details'].label = _("Details")

    class Meta:

        "KnowledgeCategory"
        model = KnowledgeCategory
        fields = ('name', 'details')


class FilterForm(ModelForm):

    """ Filter form definition """

    def __init__(self, user, skip=[], *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)

        if 'folder' in skip:
            del self.fields['folder']
        else:
            self.fields['folder'].queryset = Object.filter_permitted(
                user, KnowledgeFolder.objects, mode='x')
            #self.fields['folder'].required = False
            self.fields['folder'].label = _("Folder")

        if 'category' in skip:
            del self.fields['category']
        else:
            self.fields['category'].queryset = Object.filter_permitted(user,
                                                                       KnowledgeCategory.objects, mode='x')
            self.fields['category'].required = False
            self.fields['category'].label = _("Category")

    class Meta:

        "Filter"
        model = KnowledgeItem
        fields = ('folder', 'category')
