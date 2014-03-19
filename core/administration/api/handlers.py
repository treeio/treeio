# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- coding: utf-8 -*-

from __future__ import absolute_import, with_statement

__all__ = ['GroupHandler',
           'UserHandler',
           'ModuleHandler',
           'PerspectiveHandler',
           'PageFolderHandler',
           'PageHandler',
           ]

from django.utils.translation import ugettext as _

from treeio.core.api.utils import rc
from piston.handler import BaseHandler
from django.db.models import Q
from treeio.core.api.handlers import AccessHandler, ObjectHandler
from treeio.core.api.decorators import module_admin_required
from treeio.core.models import User, Group, Perspective, Module, Page, PageFolder
from treeio.core.administration.forms import PerspectiveForm, UserForm, GroupForm, PageForm, PageFolderForm


class GroupHandler(AccessHandler):

    "Entrypoint for Group model."

    model = Group
    form = GroupForm
    fields = ('id', 'name', 'parent', 'perspective', 'details')

    @staticmethod
    def resource_uri():
        return ('api_admin_groups', ['id'])

    @staticmethod
    def perspective(data):
        return data.get_perspective()


class UserHandler(AccessHandler):

    "Entrypoint for User model."

    model = User
    form = UserForm
    allowed_methods = ('GET', 'DELETE')
    fields = ('id', 'name', 'default_group', 'other_groups',
              'disabled', 'last_access', 'perspective')

    @staticmethod
    def resource_uri():
        return ('api_admin_users', ['id'])

    @staticmethod
    def perspective(data):
        return data.get_perspective()

    def create(self, request, *args, **kwargs):
        return rc.NOT_IMPLEMENTED

    def update(self, request, *args, **kwargs):
        return rc.NOT_IMPLEMENTED

    @module_admin_required()
    def delete(self, request, *args, **kwargs):
        pkfield = self.model._meta.pk.name

        if pkfield in kwargs:
            try:
                profile = self.model.objects.get(pk=kwargs.get(pkfield))

                if profile == request.user.get_profile():
                    self.status = 401
                    return _("This is you!")
                else:
                    profile.delete()
                    return rc.DELETED
            except self.model.MultipleObjectsReturned:
                return rc.DUPLICATE_ENTRY
            except self.model.DoesNotExist:
                return rc.NOT_HERE
        else:
            rc.BAD_REQUEST


class ModuleHandler(BaseHandler):

    "Entrypoint for Module model."

    allowed_methods = ('GET',)
    model = Module
    exclude = ('object_type', 'object_ptr', 'object_name')

    read = module_admin_required()(BaseHandler.read)

    @staticmethod
    def resource_uri():
        return ('api_admin_modules', ['id'])


class PerspectiveHandler(ObjectHandler):

    "Entrypoint for Perspective model."

    model = Perspective
    form = PerspectiveForm

    fields = ('id',) + form._meta.fields

    @staticmethod
    def resource_uri():
        return ('api_admin_perspectives', ['id'])

    def check_create_permission(self, request, mode):
        return request.user.get_profile().is_admin('treeio.core')

    def check_instance_permission(self, request, inst, mode):
        return request.user.get_profile().is_admin('treeio.core')

    @module_admin_required()
    def delete_instance(self, request, inst):
        # Don't let users delete their last perspective
        other_perspectives = Perspective.objects.filter(
            trash=False).exclude(id=inst.id)
        admin_module = Module.objects.all().filter(name='treeio.core')[0]
        if not other_perspectives:
            self.status = 401
            return _("This is your only Perspective.")
        elif not other_perspectives.filter(Q(modules=admin_module) | Q(modules__isnull=True)):
            self.status = 401
            return _("This is your only Perspective with Administration module. You would be locked out!")
        elif 'trash' in request.REQUEST:
            inst.trash = True
            inst.save()
            return inst
        else:
            inst.delete()
            return rc.DELETED

    @module_admin_required()
    def update(self, request, *args, **kwargs):
        if request.data is None:
            return rc.BAD_REQUEST

        pkfield = kwargs.get(self.model._meta.pk.name) or request.data.get(
            self.model._meta.pk.name)

        if not pkfield:
            return rc.BAD_REQUEST

        try:
            obj = self.model.objects.get(pk=pkfield)
        except self.model.ObjectDoesNotExist:
            return rc.NOT_FOUND

        attrs = self.flatten_dict(request)

        form = self.form(instance=obj, **attrs)
        if form.is_valid():
            perspective = form.save()

            admin_module = Module.objects.filter(name='treeio.core')[0]
            other_perspectives = Perspective.objects.filter(
                trash=False).exclude(id=perspective.id)
            modules = perspective.modules.all()
            if modules and not admin_module in modules:
                if not other_perspectives.filter(Q(modules=admin_module) | Q(modules__isnull=True)):
                    perspective.modules.add(admin_module)
                    request.session['message'] = _(
                        "This is your only Perspective with Administration module. You would be locked out!")
            return obj
        else:
            self.status = 400
            return form.errors


class PageFolderHandler(ObjectHandler):

    "Entrypoint for PageFolder model."
    model = PageFolder
    form = PageFolderForm

    @staticmethod
    def resource_uri():
        return ('api_admin_folders', ['id'])

    def check_instance_permission(self, request, inst, mode):
        return request.user.get_profile().is_admin('treeio.core')

    def flatten_dict(self, request):
        return {'data': super(ObjectHandler, self).flatten_dict(request.data)}


class PageHandler(ObjectHandler):

    "Entrypoint for Page model."
    model = Page
    form = PageForm

    @staticmethod
    def resource_uri():
        return ('api_admin_pages', ['id'])

    def check_instance_permission(self, request, inst, mode):
        return request.user.get_profile().is_admin('treeio.core')

    def flatten_dict(self, request):
        return {'data': super(ObjectHandler, self).flatten_dict(request.data)}
