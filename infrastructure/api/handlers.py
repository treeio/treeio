# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- coding: utf-8 -*-

from __future__ import absolute_import, with_statement

__all__ = ['ItemFieldHandler',
           'ItemTypeHandler',
           'ItemTypeHandler',
           'ItemStatusHandler',
           'ItemServicingHandler',
           'ItemHandler',
           'LocationHandler',
           ]

from treeio.core.api.utils import rc
from treeio.core.api.handlers import ObjectHandler, getOrNone
from treeio.core.models import Location
from treeio.infrastructure.models import Item, ItemField, ItemType, ItemStatus, ItemServicing
from treeio.core.forms import LocationForm
from treeio.infrastructure.forms import ItemForm, ItemTypeForm, ItemStatusForm, ItemFieldForm, ServiceRecordForm


class InfrastructureCommonHandler(ObjectHandler):

    def check_create_permission(self, request, mode):
        return request.user.get_profile().is_admin('treeio.infrastructure')


class ItemFieldHandler(InfrastructureCommonHandler):

    "Entrypoint for ItemField model."
    model = ItemField
    form = ItemFieldForm

    @staticmethod
    def resource_uri():
        return ('api_infrastructure_fields', ['id'])

    def flatten_dict(self, request):
        return {'data': super(ObjectHandler, self).flatten_dict(request.data)}


class ItemTypeHandler(InfrastructureCommonHandler):

    "Entrypoint for ItemType model."

    model = ItemType
    form = ItemTypeForm

    fields = ('id',) + ItemTypeForm._meta.fields

    @staticmethod
    def resource_uri():
        return ('api_infrastructure_types', ['id'])


class ItemStatusHandler(InfrastructureCommonHandler):

    "Entrypoint for ItemStatus model."

    model = ItemStatus
    form = ItemStatusForm

    @staticmethod
    def resource_uri():
        return ('api_infrastructure_statuses', ['id'])

    def flatten_dict(self, request):
        return {'data': super(ObjectHandler, self).flatten_dict(request.data)}


class ItemServicingHandler(InfrastructureCommonHandler):

    "Entrypoint for ItemServicing model."
    model = ItemServicing
    form = ServiceRecordForm
    fields = ('id',) + form._meta.fields

    @staticmethod
    def resource_uri():
        return ('api_infrastructure_service_records', ['id'])


class ItemHandler(ObjectHandler):

    "Entrypoint for Item model."

    model = Item
    form = ItemForm

    fields = ['id', ('itemvalue_set', ('name', 'value'))] + \
        [i.name for i in Item._meta.local_fields if i.name != 'object_ptr']

    @staticmethod
    def resource_uri():
        return ('api_infrastructure_items', ['id'])

    def create(self, request, *args, **kwargs):
        if request.data is None:
            return rc.BAD_REQUEST

        item_type = getOrNone(ItemType, request.data.get('type'))
        if not item_type or not request.user.get_profile().has_permission(item_type, mode='x'):
            return rc.FORBIDDEN

        attrs = self.flatten_dict(request)

        form = ItemForm(item_type=item_type, **attrs)
        if form.is_valid():
            item = form.save(request)
            return item
        else:
            self.status = 400
            return form.errors

    def update(self, request, *args, **kwargs):
        if request.data is None:
            return rc.BAD_REQUEST

        pkfield = kwargs.get(self.model._meta.pk.name) or request.data.get(
            self.model._meta.pk.name)

        if not pkfield:
            return rc.BAD_REQUEST

        item = getOrNone(self.model, pkfield)
        if not item:
            return rc.NOT_FOUND

        if not request.user.get_profile().has_permission(item, mode="w"):
            return rc.FORBIDDEN

        attrs = self.flatten_dict(request)

        form = ItemForm(item_type=item.item_type, instance=item, **attrs)
        if form.is_valid():
            item = form.save(request)
            return item
        else:
            self.status = 400
            return form.errors


class LocationHandler(ObjectHandler):

    "Entrypoint for Location model."

    model = Location
    form = LocationForm

    @staticmethod
    def resource_uri():
        return ('api_infrastructure_locations', ['id'])

    def flatten_dict(self, request):
        dct = super(LocationHandler, self).flatten_dict(request)
        dct['location_id'] = None
        return dct
