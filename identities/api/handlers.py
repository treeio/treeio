# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- coding:utf-8 -*-

from __future__ import absolute_import, with_statement

__all__ = ['ContactFieldHandler', 'ContactTypeHandler', 'ContactHandler']

from treeio.core.api.utils import rc
from treeio.identities.models import ContactField, ContactType, Contact
from treeio.identities.forms import ContactForm, ContactTypeForm, ContactFieldForm
from treeio.core.api.handlers import ObjectHandler, getOrNone


class ContactFieldHandler(ObjectHandler):
    "Entrypoint for ContactField model."

    model = ContactField
    form = ContactFieldForm

    @staticmethod
    def resource_uri():
        return ('api_identities_fields', ['id'])

    def flatten_dict(self, request):
        return {'data': super(ObjectHandler, self).flatten_dict(request.data)}

    def check_create_permission(self, request, mode):
        return request.user.get_profile().is_admin('treeio.identities')


class ContactTypeHandler(ObjectHandler):
    "Entrypoint for ContactType model."

    model = ContactType
    form = ContactTypeForm
    fields = ('id',) + ContactTypeForm._meta.fields

    @staticmethod
    def resource_uri():
        return ('api_identities_types', ['id'])

    def check_create_permission(self, request, mode):
        return request.user.get_profile().is_admin('treeio.identities')


class ContactHandler(ObjectHandler):
    "Entrypoint for Contact model."
    model = Contact
    form = ContactForm
    fields = ['id', ('contactvalue_set', ('name', 'value'))] + \
        [i.name for i in model._meta.local_fields if i.name != 'object_ptr']

    @staticmethod
    def resource_uri():
        return ('api_identities_contacts', ['id'])

    def create_instance(self, request, *args, **kwargs):
        return None

    def check_create_permission(self, request, mode):
        type_pk = request.REQUEST.get('type')
        try:
            request.contact_type = ContactType.objects.get(pk=type_pk)
            return request.user.get_profile().has_permission(request.contact_type, mode='x')
        except ContactType.DoesNotExist:
            return True

    def create(self, request, *args, **kwargs):
        if request.data is None:
            return rc.BAD_REQUEST

        contact_type = getOrNone(ContactType, request.data.get('contact_type'))
        if not contact_type or not request.user.get_profile().has_permission(contact_type, mode='x'):
            return rc.FORBIDDEN

        attrs = self.flatten_dict(request)

        form = ContactForm(contact_type=contact_type, **attrs)
        if form.is_valid():
            contact = form.save(request, contact_type)
            contact.set_user_from_request(request)
            return contact
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

        form = ContactForm(
            contact_type=item.contact_type, instance=item, **attrs)
        if form.is_valid():
            item = form.save(request)
            return item
        else:
            self.status = 400
            return form.errors
