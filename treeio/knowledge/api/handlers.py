# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- coding: utf-8 -*-

from __future__ import absolute_import, with_statement

__all__ = ['KnowledgeFolderHandler', 'KnowledgeCategoryHandler',
           'KnowledgeItemHandler']

from treeio.core.api.handlers import ObjectHandler, getOrNone
from treeio.knowledge.models import KnowledgeFolder, KnowledgeCategory, KnowledgeItem
from treeio.knowledge.forms import KnowledgeFolderForm, KnowledgeItemForm, KnowledgeCategoryForm, \
    FilterForm, MassActionForm


class KnowledgeFolderHandler(ObjectHandler):
    "Entrypoint for KnowledgeFolder model."
    model = KnowledgeFolder
    form = KnowledgeFolderForm

    @classmethod
    def resource_uri(cls, obj=None):
        object_id = "id"
        if obj is not None:
            object_id = obj.id
        return ('api_knowledge_folders', [object_id])

    def check_create_permission(self, request, mode):
        return True

    def flatten_dict(self, request):
        dct = super(KnowledgeFolderHandler, self).flatten_dict(request)
        dct['knowledgeType_id'] = None
        parent = request.data.get('parent')
        if parent:
            parent = getOrNone(KnowledgeFolder, pk=parent)
            if not parent or not request.user.get_profile().has_permission(parent, mode='x'):
                request.data['parent'] = None
        return dct


class KnowledgeCategoryHandler(ObjectHandler):
    "Entrypoint for KnowledgeCategory model."
    model = KnowledgeCategory
    form = KnowledgeCategoryForm

    @classmethod
    def resource_uri(cls, obj=None):
        object_id = "id"
        if obj is not None:
            object_id = obj.id
        return ('api_knowledge_categories', [object_id])

    def flatten_dict(self, request):
        return {'data': request.data}

    def check_create_permission(self, request, mode):
        return True


class KnowledgeItemHandler(ObjectHandler):
    "Entrypoint for KnowledgeItem model."
    model = KnowledgeItem
    form = KnowledgeItemForm

    @classmethod
    def resource_uri(cls, obj=None):
        object_id = "id"
        if obj is not None:
            object_id = obj.id
        return ('api_knowledge_items', [object_id])

    def flatten_dict(self, request):
        return {'data': request.data}

    def check_create_permission(self, request, mode):
        return True

    def flatten_dict(self, request):
        dct = super(KnowledgeFolderHandler, self).flatten_dict(request)
        dct['knowledgeType_id'] = None
        return dct
