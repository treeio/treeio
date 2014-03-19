# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Hardtree Core system objects
"""

from django.contrib import messages
from django.http import HttpRequest
from django.contrib.messages.storage import default_storage
from django.contrib.messages.storage.base import Message

from django.db import models
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.sites.models import RequestSite
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils.html import strip_tags
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import date as djangodate
import django.contrib.auth.models as django_auth

from treeio.core.conf import settings
from treeio.core.mail import SystemEmail

from datetime import datetime
import re
import os
import pickle
import base64
import random
import hashlib
import string


class AccessEntity(models.Model):

    "Generic model for both User and Group"
    last_updated = models.DateTimeField(auto_now=True)

    def get_entity(self):
        try:
            return self.group
        except:
            try:
                return self.user
            except:
                return None

    def is_user(self):
        try:
            user = self.user
            return user is not None
        except:
            return False

    def __unicode__(self):
        try:
            return self.get_entity().__unicode__()
        except:
            return unicode(self.id)

    def get_absolute_url(self):
        try:
            return self.get_entity().get_absolute_url()
        except:
            return ''


class Group(AccessEntity):

    "Group record"
    name = models.CharField(max_length=256)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='child_set')
    details = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self, module='identities'):
        "Returns absolute URL of the Group"
        if not module or module == 'identities':
            try:
                return reverse('identities_group_view', args=[self.id])
            except Exception:
                return ""
        else:
            try:
                return reverse('core_administration_group_view', args=[self.id])
            except Exception:
                return ""

    def get_root(self):
        "Get the root Group"

        root = self
        # keep track of items we've looked at to avoid infinite looping
        stack = [self]
        while getattr(root, 'parent', None):
            root = getattr(root, 'parent')
            if root in stack:
                break
            stack.append(root)
        return root

    def get_tree_path(self, skipself=False):
        "Get tree path as a list() starting with root Group"

        if skipself:
            path = []
        else:
            path = [self]

        current = self
        while getattr(current, 'parent', None):
            parent = getattr(current, 'parent')
            if parent in path:
                # To avoid infinite looping, check that we don't add existing
                # parent on the path again
                break
            else:
                path.insert(0, parent)
            current = parent

        return path

    def get_contact(self):
        "Returns first available Contact"
        try:
            contact = self.contact_set.all()[:1][0]
            return contact
        except Exception:
            return None

    def has_contact(self):
        "Returns true if any Contacts exist for this Group"
        try:
            if self.contact_set.count() > 0:
                return True
            else:
                return False
        except Exception:
            return False

    def get_fullname(self, save=True):
        "Returns the full name with parent(s) separated by slashes"
        current = self
        fullname = self.name
        while current.parent:
            current = current.parent
            fullname = current.name + " / " + fullname
        return fullname

    def get_perspective(self):
        "Returns currently set Perspective for the Group"
        ids = []
        try:
            for setting in ModuleSetting.get_for_module('treeio.core', name='default_perspective', group=self):
                ids.append(long(setting.value))
            id = ids[0]
            perspective = get_object_or_404(Perspective, pk=id)
        except:
            try:
                conf = ModuleSetting.get_for_module(
                    'treeio.core', 'default_perspective')[0]
                perspective = Perspective.objects.get(pk=long(conf.value))
            except:
                try:
                    perspective = Perspective.objects.all()[0]
                    ModuleSetting.set_for_module(
                        'default_perspective', perspective.id, 'treeio.core', group=self)
                except:
                    raise Perspective.DoesNotExist('No Perspective exists')
        return perspective

    def set_perspective(self, perspective):
        "Sets the Perspective for the Group"
        ModuleSetting.set_for_module(
            'default_perspective', perspective.id, 'treeio.core', group=self)

        # Ensure the Group has access to the modules in the Perspective
        modules = perspective.modules.all() or Module.objects.all()
        try:
            for module in modules:
                full_access = not module.full_access.exists() or module.full_access.filter(
                    pk=self.id).exists()
                read_access = not module.read_access.exists() or module.read_access.filter(
                    pk=self.id).exists()
                if not (read_access or full_access):
                    module.read_access.add(self)
        except:
            pass

    class Meta:

        "Group"
        ordering = ['name']


class User(AccessEntity):

    "A record about a user registered within the system"
    name = models.CharField(max_length=256)
    user = models.ForeignKey(django_auth.User)
    default_group = models.ForeignKey(
        Group, related_name='default_user_set', blank=True, null=True)
    other_groups = models.ManyToManyField(Group, blank=True, null=True)
    disabled = models.BooleanField(default=False)
    last_access = models.DateTimeField(default=datetime.now)

    class Meta:

        "User"
        ordering = ['name']

    def __unicode__(self):
        "Returns Contact name if available, username otherwise"
        contact = self.get_contact()
        if contact:
            return unicode(contact)
        else:
            return unicode(self.name)

    def save(self, *args, **kwargs):
        "Override to automatically set User.name from attached Django User"
        if not self.name and self.user:
            self.name = self.user.username
        if not self.default_group:
            try:
                self.default_group = Group.objects.all()[:1][0]
            except Exception:
                pass

        super(User, self).save(*args, **kwargs)
        # Check Hardtree Subscription user limit
        if not self.id:
            user_limit = getattr(
                settings, 'HARDTREE_SUBSCRIPTION_USER_LIMIT', 0)
            if user_limit > 0:
                user_number = User.objects.all().count()
                if user_number >= user_limit:
                    self.delete()

    def delete(self, *args, **kwargs):
        user = self.user
        super(User, self).delete(*args, **kwargs)
        try:
            user.delete()
        except:
            pass

    def get_absolute_url(self, module='identities'):
        "Returns absolute URL of the User"
        if not module or module == 'identities':
            try:
                return reverse('identities_user_view', args=[self.id])
            except Exception:
                return ""
        else:
            try:
                return reverse('core_administration_user_view', args=[self.id])
            except Exception:
                return ""

    def generate_new_password(self, size=8):
        "Generates a new password and sets it to the user"

        password = ''.join(
            [random.choice(string.letters + string.digits) for i in range(size)])

        self.user.set_password(password)
        self.user.save()

        return password

    def get_groups(self):
        "Returns the list of all groups the user belongs to"
        groups = list(self.other_groups.all())
        groups.append(self.default_group)

        return groups

    def _check_permission(self, object, mode='r'):
        "Helper for User.has_permissions(), accepts only one character for mode"

        query = models.Q(pk=self.id)
        for group in self.get_groups():
            if group:
                query = query | models.Q(pk=group.id)

        if object.full_access.filter(query).exists():
            return True

        if mode == 'r' or mode == 'x':
            if object.read_access.filter(query).exists():
                return True

        if not object.full_access.exists():
            # if no one can have full access, then allow everyone
            return True

        return False

    def has_permission(self, object, mode="r"):
        "Checks permissions on a given object for a given mode"
        if self.is_admin() or not object:
            return True

        for imode in mode:
            if not self._check_permission(object, imode):
                return False

        return True

    def is_admin(self, module_name=''):
        "True if the user has write permissions on the given module"
        access = False
        if not module_name:
            module_name = 'treeio.core'

        try:
            module = Module.objects.get(name=module_name)
            access = self._check_permission(module, mode='w')
        except Module.DoesNotExist:
            pass
        if access or module_name == 'treeio.core':
            return access
        else:
            return self.is_admin(module_name='treeio.core')

    def get_username(self):
        "String username, picked up from attached Django User or self.name string otherwise"
        if self.user:
            return self.user.username
        else:
            return self.name

    def get_perspective(self):
        "Returns currently set Perspective for the User"

        ids = []
        try:
            for setting in ModuleSetting.get_for_module('treeio.core', name='default_perspective', user=self):
                ids.append(long(setting.value))
            id = ids[0]
            perspective = get_object_or_404(Perspective, pk=id)
        except:
            try:
                perspective = self.default_group.get_perspective()
            except:
                try:
                    conf = ModuleSetting.get_for_module(
                        'treeio.core', 'default_perspective')[0]
                    perspective = Perspective.objects.get(pk=long(conf.value))
                except Exception:
                    try:
                        perspective = Perspective.objects.all()[0]
                    except:
                        perspective = Perspective(name='Default')
                        perspective.save()
                    ModuleSetting.set_for_module(
                        'default_perspective', perspective.id, 'treeio.core', user=self)
        return perspective

    def set_perspective(self, perspective):
        "Sets the Perspective for the User"
        ModuleSetting.set_for_module(
            'default_perspective', perspective.id, 'treeio.core', user=self)

        # Ensure the User has access to the modules in the Perspective
        modules = perspective.modules.all() or Module.objects.all()
        for module in modules:
            if not self.has_permission(module):
                module.read_access.add(self)

    def get_contact(self):
        "Returns first available Contact"
        try:
            contact = self.contact_set.all()[:1][0]
            return contact
        except Exception:
            return None

    def has_contact(self):
        "Returns true if any Contacts exist for this User"
        try:
            if self.contact_set.count() > 0:
                return True
            else:
                return False
        except Exception:
            return False

# User signals


def user_autocreate_handler(sender, instance, created, **kwargs):
    "When a Django User is created, automatically create a Hardtree User"
    if created:
        try:
            profile = instance.get_profile()
        except:
            profile = User(user=instance)
            profile.save()

# Autocreate a Hardtree user when Django user is created
if getattr(settings, 'HARDTREE_SIGNALS_AUTOCREATE_USER', False):
    models.signals.post_save.connect(
        user_autocreate_handler, sender=django_auth.User)


class Invitation(models.Model):

    "Invitation to register on Hardtree"
    email = models.EmailField()
    key = models.CharField(max_length=256)
    sender = models.ForeignKey(User, blank=True, null=True)
    default_group = models.ForeignKey(Group, blank=True, null=True)
    date_created = models.DateTimeField(default=datetime.now)

    def __init__(self, *args, **kwargs):
        "Create a hash automatically"
        super(Invitation, self).__init__(*args, **kwargs)
        if self.email and not self.key:
            hasher = hashlib.sha256()
            hasher.update(str(random.random()) + str(self.email))
            self.key = hasher.hexdigest()


class Tag(models.Model):

    "Model for Global Tagging"
    name = models.CharField(max_length=512)
    date_created = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Comment(models.Model):

    "Comment on any Object"
    author = models.ForeignKey(User, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    likes = models.ManyToManyField(
        User, blank=True, null=True, related_name='comments_liked')
    dislikes = models.ManyToManyField(
        User, blank=True, null=True, related_name='comments_disliked')
    date_created = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.body


class Object(models.Model):

    "Generic Hardtree object"
    creator = models.ForeignKey(
        User, blank=True, null=True, related_name='objects_created', on_delete=models.SET_NULL)
    read_access = models.ManyToManyField(
        AccessEntity, blank=True, null=True, related_name='objects_read_access')
    full_access = models.ManyToManyField(
        AccessEntity, blank=True, null=True, related_name='objects_full_access')

    object_name = models.CharField(max_length=512, blank=True, null=True)
    object_type = models.CharField(max_length=512, blank=True, null=True)
    trash = models.BooleanField(default=False)

    links = models.ManyToManyField('self', blank=True, null=True)
    subscribers = models.ManyToManyField(
        User, blank=True, null=True, related_name='subscriptions')
    #subscribers_outside = models.ManyToManyField(Contact, blank=True, null=True, related_name='subscriptions_outside')
    tags = models.ManyToManyField(Tag, blank=True, null=True)

    comments = models.ManyToManyField(
        Comment, blank=True, null=True, related_name='comments')
    likes = models.ManyToManyField(
        User, blank=True, null=True, related_name='objects_liked')
    dislikes = models.ManyToManyField(
        User, blank=True, null=True, related_name='objects_disliked')

    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(default=datetime.now)

    nuvius_resource = models.TextField(blank=True, null=True)

    # What to inherit permissions from:
    #    default: Object's module first, then the user who created it.
    access_inherit = ('*module', '*user')

    def _get_query_filter_permitted(user, mode='r', filter_trash=True):
        "Helper for filter_permitted(), accepts one character per mode"

        query = models.Q()
        if not user.is_admin():
            query = models.Q(full_access=user) | models.Q(
                full_access__isnull=True)
            query = query | models.Q(full_access=user.default_group) | models.Q(
                full_access__in=user.other_groups.all())

            if mode == 'r' or mode == 'x':
                query = query | models.Q(read_access=user)
                query = query | models.Q(read_access=user.default_group) | models.Q(
                    read_access__in=user.other_groups.all())

        if filter_trash:
            query = query & models.Q(trash=False)

        return query
    _get_query_filter_permitted = staticmethod(_get_query_filter_permitted)

    def filter_permitted(user, manager, mode="r", filter_trash=True):
        "Returns Objects the given user is allowed to access, depending on mode - read(r), write(w) or execute(x)"
        if not user:
            return []

        query = models.Q()
        for imode in mode:
            query = query & Object._get_query_filter_permitted(
                user, imode, filter_trash)

        objects = manager.filter(query).distinct()
        return objects
    filter_permitted = staticmethod(filter_permitted)

    def filter_by_request(request, manager, mode="r", filter_trash=True):
        "Returns Objects the current user is allowed to access, depending on mode - read(r), write(w) or execute(x)"
        user = None
        if request.user.username:
            try:
                user = request.user.get_profile()
            except MultipleObjectsReturned:
                user = User.objects.filter(user__id=request.user.id)[0]
        if user:
            return Object.filter_permitted(user, manager, mode, filter_trash)
        return []
    filter_by_request = staticmethod(filter_by_request)

    def __unicode__(self):
        "String representation"
        try:
            return unicode(self.get_related_object())
        except Exception:
            return unicode(self.object_type) + " [" + unicode(self.id) + "]"

    def save(self, *args, **kwargs):
        "Override to auto-detect object type and set default user if unset"

        try:
            name = self.__unicode__()
            if not name == self.object_name:
                self.object_name = name[0:510]
        except:
            pass

        types = re.findall('\'(.+)\'', str(self.__class__))
        if types:
            self.object_type = types[0]

        object = super(Object, self).save(*args, **kwargs)

        return object

    def get_object_module(self):
        "Returns the module for this object, e.g. 'projects'"

        return getattr(self._meta, 'app_label', None)

    def get_nuvius_resources(self):
        """Returns a list of items generated from self.nuvius_resource

        The convention used is:
        Each item is specified as '#id.key#' separated by commas
        Returns items as tuples (id, key) from self.nuvius_resource
        """
        resources = []
        if self.nuvius_resource:
            text = unicode(self.nuvius_resource)
            splits = text.split(',')
            for bit in splits:
                res = bit.strip('#').split('.', 1)
                resources.append(res)
        return resources

    def add_nuvius_resource(self, resource_id, key=None):
        "Add a Nuvius resource to self.nuvius_resource"
        existing = [res[0] for res in self.get_nuvius_resources()]
        if not unicode(resource_id) in existing:
            new = "#" + unicode(resource_id)
            if key:
                new += "." + unicode(key)
            new += "#"
            if self.nuvius_resource:
                self.nuvius_resource += "," + new
            else:
                self.nuvius_resource = new
        return self

    def get_root(self):
        "Get the root element, for objects implementing a tree-like structure via .parent"

        root = self
        # keep track of items we've looked at to avoid infinite looping
        stack = [self]
        while getattr(root, 'parent', None):
            root = getattr(root, 'parent')
            if root in stack:
                break
            stack.append(root)
        return root

    def get_tree_path(self, skipself=False):
        """Get tree path as a list() starting with root element,
        for objects implementing a tree-like structure via .parent"""

        if skipself:
            path = []
        else:
            path = [self]

        current = self
        while getattr(current, 'parent', None):
            parent = getattr(current, 'parent')
            if parent in path:
                # To avoid infinite looping, check that we don't add existing
                # parent on the path again
                break
            else:
                path.insert(0, parent)
            current = parent

        return path

    def get_related_object(self):
        "Returns a child object which inherits from self, if exists"
        try:
            obj_name = re.match(
                ".*\.(?P<name>\w+)$", self.object_type).group('name')
            return getattr(self, obj_name.lower())
        except Exception:
            return None

    def get_human_type(self, translate=True):
        "Returns prettified name of the object type"
        try:
            obj_name = re.match(
                ".*\.(?P<name>\w+)$", self.object_type).group('name')
            pattern = re.compile('([A-Z][A-Z][a-z])|([a-z][A-Z])')
            human_type = pattern.sub(
                lambda m: m.group()[:1] + " " + m.group()[1:], obj_name)
            if translate:
                human_type = _(human_type)
            return human_type
        except Exception:
            return self.object_type

    def get_absolute_url(self):
        "Returns a URL to the child object, if available"
        try:
            return self.get_related_object().get_absolute_url()
        except Exception:
            return ""

    def is_searchable(self):
        "Returns True if the item should be included in Search index"
        return getattr(self, 'searchable', True)

    def is_attached(self):
        "Returns True if item is attached to some other Object and serves as a part of it"
        return getattr(self, 'attached', False)

    def get_search_item(self):
        "Constucts a search item as a dictionary with title, content and URL"

        object = self.get_related_object()
        if not object:
            object = self

        item = {
            'id': u'',
            'name': u'',
            'type': unicode(object.get_human_type()),
            'content': u'',
            'url': unicode(object.get_absolute_url())
        }

        if object.id:
            item['id'] = unicode(object.id)

        if hasattr(object, 'title'):
            item['name'] = unicode(object.title)
        elif hasattr(object, 'name'):
            item['name'] = unicode(object.name)
        else:
            item['name'] = unicode(object)

        if hasattr(self, 'body'):
            item['content'] = unicode(self.body)
        elif hasattr(self, 'details'):
            item['content'] = unicode(self.details)
        else:
            for field in self.get_fields():
                try:
                    value = self.get_field_value(field.name)
                    item['content'] += ' ' + unicode(value)
                except:
                    pass

        if hasattr(self, 'tags'):
            for tag in self.tags.all():
                item['content'] += ' ' + unicode(tag)

        return item

    def create_notification(self, action='update', author=None, *args, **kwargs):
        "Creates an UpdateRecord to be submitted to all subscribers of an Object"

        if not (self.subscribers.all().count() or author):
            return None

        notification = UpdateRecord()
        updated = False

        if action == 'delete':
            notification.format_message = "%s \"%s\" deleted."
            notification.set_format_strings(
                [unicode(self.get_human_type(translate=False)), unicode(self)])
            notification.record_type = 'delete'
            updated = True

        elif action == 'm2m':
            notification.record_type = 'update'
            if 'field' in kwargs and 'original' in kwargs and 'updated' in kwargs:
                if kwargs['updated']:
                    updated_text = ""
                    for obj in kwargs['updated']:
                        updated_text += '<a href="%s" class="popup-link">%s</a>' % (
                            obj.get_absolute_url(), unicode(obj))
                        if kwargs['updated'].index(obj) < len(kwargs['updated']) - 1:
                            updated_text += ', '
                else:
                    updated_text = "None"

                field = unicode(kwargs['field'])

                if field == 'assigned':
                    notification.format_message = "%s assigned to %s.<br />"
                    notification.set_format_strings(
                        [self.get_human_type(translate=False), updated_text])
                    notification.save()
                    for obj in kwargs['updated']:
                        if isinstance(obj, AccessEntity) or isinstance(obj, User):
                            notification.recipients.add(obj)
                            self.subscribers.add(obj)
                            try:
                                if not obj.has_permission(self, mode='w'):
                                    self.full_access.add(obj)
                            except:
                                pass
                        else:
                            try:
                                notification.recipients.add(obj.related_user)
                                self.subscribers.add(obj.related_user)
                            except:
                                pass
                            try:
                                if not obj.related_user.has_permission(self, mode='w'):
                                    self.full_access.add(obj.related_user)
                            except:
                                pass
                else:
                    notification.format_message = "%s changed to \"%s\".<br />"
                    notification.set_format_strings(
                        [field.replace('_', ' ').capitalize(), updated_text])

                updated = True

        elif action == 'create':
            notification.format_message = "%s created."
            notification.set_format_strings(
                [unicode(self.get_human_type(translate=False))])
            notification.record_type = 'create'
            updated = True

        else:
            notification.record_type = 'update'

            fields = self.get_field_names()
            original = self.get_related_object()

            notification.format_message = ""
            strings = []

            for field in fields:
                if hasattr(getattr(self, field), 'all'):
                    # Skip ManyToMany fields - they handled differently
                    continue

                if field in getattr(settings, 'HARDTREE_UPDATE_BLACKLIST', []):
                    # Skip blacklisted items
                    continue

                if 'password' in field:
                    # Skip password fields - it's not nice to give them away in
                    # plain-text
                    continue

                current = self.get_field_value(field)
                before = original.get_field_value(field)
                if current != before:
                    # cut out '_display' from some fields
                    if '_display' in field:
                        field = field.replace('_display', '')
                    if isinstance(self._meta.get_field(field), models.TextField):
                        notification.format_message += "%s changed.<br />"
                        strings.extend(
                            [unicode(field).replace('_', ' ').capitalize()])
                    elif isinstance(self._meta.get_field(field), models.DateTimeField):
                        notification.format_message += "%s changed from \"%s\" to \"%s\".<br />"
                        # this needs to be done properly, via getting current
                        # locale's format
                        localeformat = "j F Y, H:i"
                        strings.extend([unicode(field).replace('_', ' ').capitalize(),
                                        unicode(
                                            djangodate(before, localeformat)),
                                        unicode(djangodate(current, localeformat))])
                    else:
                        notification.format_message += "%s changed from \"%s\" to \"%s\".<br />"
                        strings.extend([unicode(field).replace('_', ' ').capitalize(),
                                        unicode(before), unicode(current)])
                    updated = True

            notification.set_format_strings(strings)

        if self.trash:
            try:
                old_object = Object.objects.get(pk=self.id)
                if not old_object.trash:
                    notification.format_message += " %s moved to <a href=\"%s\">%s</a>"
                    strings = notification.get_format_strings()
                    strings.extend([unicode(self.get_human_type(translate=False)),
                                    reverse('core_trash'), "Trash"])
                    notification.set_format_strings(strings)
                    notification.record_type = 'delete'
                    updated = True
            except Exception:
                pass

        if 'body' in kwargs:
            notification.body = kwargs['body']
            updated = True

        if not updated:
            return None

        notification.url = self.get_absolute_url()
        notification.author = author

        if action != 'delete':
            notification.sender = self

        notification.save()
        notification.about.add(self)
        return notification

    def set_user(self, user):
        "Sets owner of the Object to the given user"

        # get default permissions from settings
        try:
            conf = ModuleSetting.get_for_module(
                'treeio.core', 'default_permissions')[0]
            default_permissions = conf.value
        except:
            default_permissions = settings.HARDTREE_DEFAULT_PERMISSIONS

        if hasattr(user, 'get_profile'):
            user = user.get_profile()

        if not self.creator:
            self.creator = user
            self.save()

        if default_permissions == 'everyone':
            return self

        if 'force' in default_permissions:
            # Don't do automatic inheritance
            do_user = True

        else:
            # try to inherit permissions first from any parent objects as
            # specified in models.py
            cascade = getattr(self, 'access_inherit', [])
            do_user = False
            if cascade:
                for attr in cascade:
                    if attr == '*user':
                        do_user = True
                        break
                    elif attr == '*module':
                        if not 'nomodule' in default_permissions:
                            modules = Module.objects.filter(
                                name__contains=self.get_object_module())
                            if modules:
                                for module in modules:
                                    self.copy_permissions(module)
                                if not user.has_permission(self, 'w'):
                                    do_user = True
                                break
                        else:
                            do_user = True
                            break
                    else:
                        try:
                            obj = getattr(self, attr)
                            if obj:
                                self.copy_permissions(obj)
                                if not user.has_permission(self, 'w'):
                                    do_user = True
                                break
                        except:
                            pass
        if do_user:
        # if we can't inherit set permissions to the user as specified in the
        # settings

            if 'readonly' in default_permissions:
                access_container = self.read_access
            else:
                access_container = self.full_access

            if 'user' in default_permissions:
                access_container.add(user)

            if 'usergroup' in default_permissions and user.default_group:
                access_container.add(user.default_group)

            if 'userallgroups' in default_permissions:
                if user.default_group:
                    access_container.add(user.default_group)
                for group in user.other_groups.all():
                    access_container.add(group)

        # process assigned fields to give auto-permissions to assignees
        if hasattr(self, 'assigned'):
            for obj in self.assigned.all():
                if isinstance(obj, AccessEntity) or isinstance(obj, User):
                    try:
                        if not obj.has_permission(self, mode='w'):
                            self.full_access.add(obj)
                    except:
                        pass
                else:
                    try:
                        if not obj.related_user.has_permission(self, mode='w'):
                            self.full_access.add(obj.related_user)
                    except:
                        pass

        return self

    def set_default_user(self):
        "Sets the user defined in settings.HARDTREE_DEFAULT_USER_ID and default mode"
        try:
            user = User.objects.get(pk=settings.HARDTREE_DEFAULT_USER_ID)
        except:
            try:
                user = User.objects.all()[0]
            except IndexError:
                user = None
        self.set_user(user)
        return self

    def set_user_from_request(self, request, mode=None):
        "Sets the user to the current in request and default mode for the user"
        user = request.user.get_profile()
        self.set_user(user)
        return self

    def copy_permissions(self, object):
        "Copies all permissions from object. Existing permissions will NOT be removed or dropped"
        read_access = object.read_access.all()
        for entity in read_access:
            self.read_access.add(entity)

        full_access = object.full_access.all()
        for entity in full_access:
            self.full_access.add(entity)

        return self

    def get_fields(self):
        "Returns list of fields for given object"
        return filter(lambda f: f.name not in settings.HARDTREE_OBJECT_BLACKLIST, self._meta.fields)

    def get_field_names(self):
        "Returns list of field names for given object"
        x = []
        for f in self._meta.fields:
            if f.name not in settings.HARDTREE_OBJECT_BLACKLIST:
                x.append(f.name)
        for f in self._meta.many_to_many:
            if f.name not in settings.HARDTREE_OBJECT_BLACKLIST:
                x.append(f.name)
        return x

    def get_field_value(self, field_name, default=None):
        "Returns the value of a given field"
        value = getattr(self, field_name, default)
        if hasattr(value, 'all'):
            # Returns value for ManyToMany fields
            value = value.all()
        if hasattr(self, 'get_%s_display' % field_name):
            # Handle choices to ChoiceFields
            try:
                value = getattr(self, 'get_%s_display' % field_name)()
            except:
                pass
        return value

    def set_field_value(self, field_name, value):
        "Sets the value of a given field"
        return setattr(self, field_name)

    def set_last_updated(self, last_updated=datetime.now()):
        self.last_updated = last_updated
        self.save()


class Revision(models.Model):
    previous = models.OneToOneField(
        'self', blank=True, null=True, related_name='next')
    object = models.ForeignKey(Object)
    change_type = models.CharField(max_length=512, null=True, blank=True)
    date_created = models.DateTimeField(default=datetime.now)


class RevisionField(models.Model):
    revision = models.ForeignKey(Revision)
    field_type = models.CharField(max_length=512, null=True, blank=True)
    field = models.CharField(max_length=512, null=True, blank=True)
    value = models.TextField(null=True, blank=True)
    value_key = models.ForeignKey(
        Object, null=True, blank=True, related_name='revisionfield_key', on_delete=models.SET_NULL)
    value_m2m = models.ManyToManyField(
        Object, related_name='revisionfield_m2m')
    value_key_acc = models.ForeignKey(
        AccessEntity, null=True, blank=True, related_name='revisionfield_key_acc', on_delete=models.SET_NULL)
    value_m2m_acc = models.ManyToManyField(
        AccessEntity, related_name='revisionfield_m2m_acc')


class UpdateRecord(models.Model):

    "Update of an Object"
    author = models.ForeignKey(
        User, blank=True, null=True, related_name="sent_updates")
    sender = models.ForeignKey(
        Object, blank=True, null=True, related_name="sent_updates", on_delete=models.SET_NULL)
    about = models.ManyToManyField(
        Object, blank=True, null=True, related_name="updates")
    recipients = models.ManyToManyField(
        AccessEntity, blank=True, null=True, related_name="received_updates")
    #recipients_outside = models.ManyToManyField(Contact, blank=True, null=True, related_name="outside_received_updates")
    record_type = models.CharField(max_length=32,
                                   choices=(('create', 'create'), ('update', 'update'),
                                            ('delete', 'delete'), (
                                                'trash', 'trash'),
                                            ('message', 'message'),
                                            ('manual', 'manual'), ('share', 'share')))
    url = models.CharField(max_length=512, blank=True, null=True)
    body = models.TextField(default='', blank=True, null=True)
    score = models.IntegerField(default=0)
    format_message = models.TextField(blank=True, null=True)
    format_strings = models.TextField(blank=True, null=True)
    comments = models.ManyToManyField(
        Comment, blank=True, null=True, related_name='comments_on_updates')
    likes = models.ManyToManyField(
        User, blank=True, null=True, related_name='updates_liked')
    dislikes = models.ManyToManyField(
        User, blank=True, null=True, related_name='updates_disliked')
    date_created = models.DateTimeField(default=datetime.now)

    class Meta:

        "UpdateRecord"
        ordering = ['-date_created']

    def __unicode__(self):
        return self.body

    def set_user_from_request(self, request):
        "Sets .author to current user and .sender to user's Contact (if available)"
        user = request.user.get_profile()
        self.author = user
        self.recipients.add(user)
        contact = user.get_contact()
        if contact:
            self.sender = contact
        self.save()

    def set_format_strings(self, strings):
        "Sets format_strings to the list of strings"
        self.format_strings = base64.b64encode(
            pickle.dumps(strings, pickle.HIGHEST_PROTOCOL))
        return self

    def extend_format_strings(self, strings):
        "Extends existing format strings"
        existing = self.get_format_strings()
        if existing:
            existing.extend(strings)
        else:
            existing = strings
        self.set_format_strings(existing)
        return self

    def get_format_strings(self):
        "Gets format_strings as a list of strings"
        result = None
        if self.format_strings:
            try:
                result = pickle.loads(base64.b64decode(self.format_strings))
            except pickle.PickleError:
                pass
        return result

    def get_format_message(self):
        "Returns translatable message in the current language with all attributes applied"
        strings = self.get_format_strings()
        result = ''
        if self.format_message:
            result = self.format_message
        if result and strings:
            try:
                # first, try to translate
                translated = []
                for item in strings:
                    if item:
                        translated.append(_(item))
                    else:
                        translated.append(_("None"))
                result = _(self.format_message) % tuple(translated)
            except TypeError:
                # then try untranslated
                try:
                    result = self.format_message % tuple(strings)
                except TypeError:
                    # give up
                    pass
        return result

    def get_full_message(self):
        "Return full message"
        result = ''
        format_message = self.get_format_message()
        if format_message:
            result += format_message
        if self.body:
            result += '<p>' + self.body + '</p>'
        if result.endswith('<br />'):
            result = result[:len(result) - 6]
        return result
    full_message = property(get_full_message)

    def notify_subscribers(self, obj, *args, **kwargs):
        if obj not in self.about.all():
            return
        author = self.author
        if author:
            # E-mail contents for e-mail notifications
            full_message = self.get_full_message()
            html = '%s:<br /><br />\n\n<a href="%s">%s</a> (%s):<br /><br />\n\n%s<br /><br />\n\n' % \
                (unicode(author), obj.get_absolute_url(), unicode(obj),
                 unicode(obj.get_human_type()), full_message)
            grittertext = '%s:<br />\n\n<a href="#%s">%s</a> (%s):<br />\n\n%s<br />\n\n' % \
                (unicode(author), obj.get_absolute_url(), unicode(obj),
                 unicode(obj.get_human_type()), full_message)
            if 'request' in kwargs:
                domain = RequestSite(kwargs['request']).domain
                html = html.replace('href="', 'href="http://' + domain)
            body = strip_tags(html)
            signature = "This is an automated message from Tree.io service (http://tree.io). Please do not reply to this e-mail."
            subject = "[Tree.io%s] %s: %s - %s" % (' #%d' % obj.id if self.record_type != 'delete' else '', unicode(author),
                                                   unicode(obj.get_human_type()), unicode(strip_tags(full_message)[:100]))

            for recipient in self.recipients.all():
                if author and author.id == recipient.id:
                    continue
                email_notifications = getattr(
                    settings, 'HARDTREE_ALLOW_EMAIL_NOTIFICATIONS', False)
                gritter_notifications = getattr(
                    settings, 'HARDTREE_ALLOW_GRITTER_NOTIFICATIONS', False)
                try:
                    conf = ModuleSetting.get(
                        'email_notifications', user=recipient)[0]
                    email_notifications = conf.value
                except:
                    pass

                if email_notifications == 'True':
                    try:
                        toaddr = recipient.get_entity(
                        ).get_contact().get_email()
                    except:
                        toaddr = None
                    if toaddr:
                        SystemEmail(
                            toaddr, subject, body, signature, html + signature).send_email()

                if gritter_notifications:
                    try:
                        request = HttpRequest()
                        request.user = recipient.user.user
                        storage = default_storage(request)
                        storage._add(
                            Message(messages.constants.INFO, "%s" % grittertext))
                    except:
                        pass


class Module(Object):

    "Record of a module (application) existing within the system"
    name = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    details = models.TextField(blank=True)
    url = models.CharField(max_length=512)
    display = models.BooleanField(default=True)
    system = models.BooleanField(default=True)

    searcheable = False

    class Meta:

        "Module"
        ordering = ['name']

    def get_absolute_url(self):
        "Returns absolute URL"
        try:
            return reverse('core_admin_module_view', args=[self.id])
        except Exception:
            pass

    def __unicode__(self):
        return self.title


class Perspective(Object):

    "Defines a set of modules enabled for a given user"
    name = models.CharField(max_length=256)
    details = models.TextField(blank=True)
    modules = models.ManyToManyField(Module, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        "Returns absolute URL"
        try:
            return reverse('core_admin_perspective_view', args=[self.id])
        except Exception:
            pass

    def get_modules(self):
        "Get Modules"
        modules = self.modules.all()
        if not modules:
            modules = Module.objects.all()
        return modules


class ModuleSetting(models.Model):

    "Free-type Module setting"
    name = models.CharField(max_length=512)
    label = models.CharField(max_length=512)
    perspective = models.ForeignKey(Perspective, blank=True, null=True)
    module = models.ForeignKey(Module, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    group = models.ForeignKey(Group, blank=True, null=True)
    value = models.TextField()

    def loads(self):
        "Unpickle a ModuleSetting value"
        result = None
        if self.value:
            try:
                result = pickle.loads(base64.b64decode((self.value)))
            except pickle.PickleError:
                pass
        return result

    def dumps(self, value):
        "Pickle a ModuleSetting value"
        self.value = base64.b64encode(
            pickle.dumps(value, pickle.HIGHEST_PROTOCOL))
        return self

    def get(name='', strict=False, **kwargs):
        "Setting getter"
        if name:
            settings = ModuleSetting.objects.filter(name=name)
        else:
            settings = ModuleSetting.objects.all()
        if strict:
            settings = settings.filter(**kwargs)
        elif settings:
            new_settings = settings
            for arg in kwargs:
                new_settings = new_settings.filter(**{arg: kwargs[arg]})
                if new_settings:
                    settings = new_settings
                else:
                    new_settings = settings

        return settings
    get = staticmethod(get)

    def get_for_module(module_name, name='', strict=False, **kwargs):
        "Get a setting per module"
        try:
            module = Module.objects.get(name=module_name)
            return ModuleSetting.get(name=name, module=module, strict=strict, **kwargs)
        except Exception:
            return None
    get_for_module = staticmethod(get_for_module)

    def set(name, value, **kwargs):
        "Define a ModuleSetting"
        existing = ModuleSetting.objects.filter(name=name, **kwargs)
        if existing:
            for setting in existing:
                setting.value = value
                setting.save()
        else:
            setting = ModuleSetting(name=name, value=value, **kwargs)
            setting.save()
        return setting
    set = staticmethod(set)

    def add(name, value, **kwargs):
        "Add a ModuleSetting"
        setting = ModuleSetting(name=name, value=value, **kwargs)
        setting.save()
        return setting
    add = staticmethod(add)

    def set_for_module(name, value, module_name, **kwargs):
        "Define a ModuleSetting per module"
        try:
            module = Module.objects.get(name=module_name)
            return ModuleSetting.set(name=name, value=value, module=module, **kwargs)
        except Exception:
            return None
    set_for_module = staticmethod(set_for_module)

    def add_for_module(name, value, module_name, **kwargs):
        "Add a ModuleSetting per module"
        try:
            module = Module.objects.get(name=module_name)
            return ModuleSetting.add(name=name, value=value, module=module, **kwargs)
        except Exception:
            return None
    add_for_module = staticmethod(add_for_module)

    def __unicode__(self):
        return unicode(self.name) + ": " + unicode(self.value)

    def save(self, *args, **kwargs):
        "Override to set label from name if undefined"
        if not self.label:
            self.label = self.name
        super(ModuleSetting, self).save(*args, **kwargs)


class ConfigSetting(models.Model):

    "Config setting to be activated dynamically from the database on request"
    name = models.CharField(max_length=255, unique=True)
    value = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.loads())

    def loads(self):
        "Unpickle a ModuleSetting value"
        result = None
        try:
            result = pickle.loads(base64.b64decode((self.value)))
        except:
            result = self.value
        return result

    def dumps(self, value):
        "Pickle a ModuleSetting value"
        self.value = base64.b64encode(
            pickle.dumps(value, pickle.HIGHEST_PROTOCOL))
        return self

    def save(self, *args, **kwargs):
        self.dumps(self.value)
        super(ConfigSetting, self).save(*args, **kwargs)


class IntegrationResource:

    """ Resource set for integration via Nuvius

    nuvius_id     = <ID of the user on Nuvius (may be obtained via JSONP call>
    resource_id   = <Application ID, i.e. 1 for Facebook>
    resource_name = <Application name, i.e. Google Contacts>
    services      = <Data points ID on Nuvius, e.g. for /services/news/ ID is 37rw to read/write>
    role          = <Usually master or slave>

    """

    nuvius_id = 0
    resource_id = 0
    resource_name = ''
    service = ''
    role = 'slave'

    def __init__(self, nuvius_id, resource_id, resource_name, services='', role='slave'):
        "Initialize an Integration Resource"

        self.nuvius_id = nuvius_id
        self.resource_id = resource_id
        self.resource_name = resource_name
        self.services = services
        if not self.service:
            self.service = getattr(settings, 'NUVIUS_SERVICES', '')
        self.role = role


class Location(Object):

    "Location for users, assets, etc."
    name = models.CharField(max_length=512)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='child_set')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        "Returns absolute URL"
        try:
            return reverse('identities_location_view', args=[self.id])
        except Exception:
            pass


class PageFolder(Object):

    "Folder for static Pages"
    name = models.CharField(max_length=256)
    details = models.TextField(blank=True)

    searchable = False

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        "Returns absolute URL"
        try:
            return reverse('core_admin_pagefolder_view', args=[self.id])
        except Exception:
            pass


class Page(Object):

    "Static page"
    name = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    folder = models.ForeignKey(PageFolder)
    body = models.TextField(blank=True)
    published = models.BooleanField(default=True)

    searchable = False

    class Meta:

        "Page"
        ordering = ['name']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        "Returns absolute URL"
        try:
            return reverse('core_admin_page_view', args=[self.id])
        except Exception:
            pass


class Widget(models.Model):

    "Widget object to remember the set and order of Widget for a user"
    user = models.ForeignKey(User)
    perspective = models.ForeignKey(Perspective)
    module_name = models.CharField(max_length=256)
    widget_name = models.CharField(max_length=256)
    weight = models.IntegerField(default=0)

    def __unicode__(self):
        return self.widget_name

    class Meta:

        "Widget"
        ordering = ['weight']


class Attachment(models.Model):

    "Attachment object to upload and reference a file"
    filename = models.CharField(max_length=64)
    attached_object = models.ForeignKey(Object, blank=True, null=True)
    attached_record = models.ForeignKey(UpdateRecord, blank=True, null=True)
    attached_file = models.FileField(upload_to='attachments')
    mimetype = models.CharField(max_length=64, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    uploaded_by = models.ForeignKey(User)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return unicode(self.filename)

    def get_file_type(self):
        match = re.match(
            '.*\.(?P<extension>[a-zA-Z0-9]+)$', unicode(self.filename))
        if match:
            return unicode(match.group('extension')).upper()
        else:
            return ''

    def can_preview(self):
        filetype = self.get_file_type()
        exts = ('PNG', 'JPG', 'JPEG', 'BMP', 'GIF', 'SVG')
        if filetype.upper() in exts:
            return True
        return False

    def get_icon(self):
        if self.get_file_type() == 'PDF':
            # PDF
            return 'pdf'
        elif self.get_file_type() in ['DOCX', 'DOC', 'TXT']:
            # Documents
            return 'blue-document-word'
        elif self.get_file_type() in ['JPG', 'JPEG', 'GIF', 'PNG', 'TIFF', 'PSD', 'BMP']:
            # Images
            return 'image'
        else:
            # Other
            return 'blue-document'

    def delete(self, *args, **kwargs):
        filepath = os.path.join(
            getattr(settings, 'MEDIA_ROOT'), 'attachments', self.attached_file.name)
        try:
            self.attached_file.delete()
            os.remove(filepath)
        except:
            pass
        super(Attachment, self).delete(*args, **kwargs)
