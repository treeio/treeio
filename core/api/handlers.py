# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q

from piston.handler import BaseHandler, HandlerMetaClass, typemapper
import base64
from utils import rc
from decorators import module_admin_required
from cStringIO import StringIO


class ObjectHandlerMetaClass(HandlerMetaClass):

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)

        if hasattr(new_cls, 'model'):
            typemapper[new_cls] = (new_cls.model, new_cls.is_anonymous)

        new_cls.__dir = dir(new_cls)
        for field in ('fields', 'model', 'exclude', 'allowed_methods', 'anonymous', 'is_anonymous',
                      'read', 'create', 'update', 'delete'):
            try:
                new_cls.__dir.remove(field)
            except ValueError:
                pass
        new_cls.__class__.__dir__ = lambda x: x.__dir

        return new_cls


class ObjectHandler(BaseHandler):

    # I use metaclass to give a chance to show model's fields with names in
    # tuple
    __metaclass__ = ObjectHandlerMetaClass

    form = None
    exclude = ('object_type', 'object_ptr', 'object_name')

    def has_form(self):
        return hasattr(self, 'form')

    def check_create_permission(self, request, mode):
        return True

    def create_instance(self, request, *args, **kwargs):
        return self.model()

    def check_instance_permission(self, request, inst, mode):
        return request.user.get_profile().has_permission(inst, mode=mode)

    def delete_instance(self, request, inst):
        if not self.check_instance_permission(request, inst, mode='w'):
            return rc.FORBIDDEN
        if 'trash' in request.REQUEST:
            inst.trash = True
            inst.save()
            return inst
        else:
            inst.delete()
            return rc.DELETED

    def flatten_dict(self, request):
        files, data = {}, {}
        for key, value in request.data.items():
            if isinstance(value, dict) and value.get('type') == 'base64':
                content = base64.decodestring(value.get('content', ''))
                files[str(key)] = InMemoryUploadedFile(file=StringIO(content),
                                                       field_name=str(key),
                                                       name=value.get(
                                                           'name', ''),
                                                       content_type=value.get(
                                                           'content_type'),
                                                       size=len(content),
                                                       charset=None)
            else:
                data[str(key)] = value
        return {'data': data,
                'files': files,
                'user': request.user.get_profile()}

    def get_filter_query(self, args):
        query = Q()
        fields = self.model._meta.get_all_field_names()
        for arg in args:
            if hasattr(self.model, arg) and args[arg]:
                kwargs = {str(arg + '__id'): long(args[arg])}
                query = query & Q(**kwargs)
            elif arg in fields:
                kwargs = {arg: args[arg]}
                query = query & Q(**kwargs)
        return query

    def read(self, request, *args, **kwargs):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED

        pkfield = kwargs.get(self.model._meta.pk.name)

        if pkfield:
            try:
                obj = self.model.objects.get(pk=pkfield)
                if not self.check_instance_permission(request, obj, 'r'):
                    return rc.FORBIDDEN
                else:
                    return obj
            except ObjectDoesNotExist:
                return rc.NOT_FOUND
            # should never happen, since we're using a PK
            except MultipleObjectsReturned:
                return rc.BAD_REQUEST
        else:
            query = self.get_filter_query(request.GET)
            return self.model.filter_by_request(request, self.model.objects.filter(query))

    def create(self, request, *args, **kwargs):
        if not self.has_model() or not self.has_form():
            return rc.NOT_IMPLEMENTED

        if request.data is None:
            return rc.BAD_REQUEST

        if not self.check_create_permission(request, "x"):
            return rc.FORBIDDEN

        attrs = self.flatten_dict(request)

        inst = self.create_instance(request, *args, **kwargs)
        form = self.form(instance=inst, **attrs)
        if form.is_valid():
            obj = form.save()
            obj.set_user_from_request(request)
            return obj
        else:
            self.status = 400
            return form.errors

    def update(self, request, *args, **kwargs):
        if not self.has_model() or not self.has_form():
            return rc.NOT_IMPLEMENTED

        pkfield = kwargs.get(self.model._meta.pk.name) or request.data.get(
            self.model._meta.pk.name)

        if not pkfield or request.data is None:
            return rc.BAD_REQUEST

        try:
            obj = self.model.objects.get(pk=pkfield)
        except ObjectDoesNotExist:
            return rc.NOT_FOUND

        if not self.check_instance_permission(request, obj, "w"):
            return rc.FORBIDDEN

        attrs = self.flatten_dict(request)

        form = self.form(instance=obj, **attrs)
        if form.is_valid():
            obj = form.save()
            return obj
        else:
            self.status = 400
            return form.errors

    def delete(self, request, *args, **kwargs):
        if not self.has_model():
            raise NotImplementedError

        if not args and not kwargs:
            return rc.BAD_REQUEST

        pkfield = self.model._meta.pk.name

        try:
            if pkfield in kwargs:
                inst = self.model.objects.get(pk=kwargs.get(pkfield))
            else:
                inst = self.model.objects.get(*args, **kwargs)
            return self.delete_instance(request, inst)
        except self.model.MultipleObjectsReturned:
            return rc.DUPLICATE_ENTRY
        except self.model.DoesNotExist:
            return rc.NOT_HERE


class AccessHandler(BaseHandler):
    form = None

    def has_form(self):
        return hasattr(self, 'form')

    read = module_admin_required()(BaseHandler.read)

    delete = module_admin_required()(BaseHandler.delete)

    @module_admin_required()
    def create(self, request, *args, **kwargs):
        if not self.has_model() or not self.has_form():
            return rc.NOT_IMPLEMENTED

        if request.data is None:
            return rc.BAD_REQUEST

        form = self.form(self.flatten_dict(request.data))
        if form.is_valid():
            obj = form.save()
            return obj
        else:
            self.status = 400
            return form.errors

    @module_admin_required()
    def update(self, request, *args, **kwargs):
        if not self.has_model() or not self.has_form():
            return rc.NOT_IMPLEMENTED

        pkfield = kwargs.get(self.model._meta.pk.name) or request.data.get(
            self.model._meta.pk.name)

        if not pkfield or request.data is None:
            return rc.BAD_REQUEST

        obj = getOrNone(self.model, pk=pkfield)
        if obj is None:
            return rc.NOT_FOUND

        attrs = self.flatten_dict(request.data)

        form = self.form(attrs, instance=obj)
        if form.is_valid():
            obj = form.save()
            return obj
        else:
            self.status = 400
            return form.errors


def getOrNone(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        return None
