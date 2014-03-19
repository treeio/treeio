# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
User middleware: performs user-specific request pre-processing
"""
import urllib
import urlparse

from django.db.models import signals
from django.utils.functional import curry
from django.core.urlresolvers import resolve
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import translation
from treeio.core.models import Object, ModuleSetting, UpdateRecord
from treeio.core.views import ajax_popup
from treeio.core.conf import settings
from django.db import models
from django.core.cache import cache
import json
import time


class CommonMiddleware():

    "Set up Object notifications"

    objects = {}

    def process_request(self, request):
        "Process request"

        # check mobile:
        if getattr(request, 'mobile', False) and \
                not request.POST and \
                not '/m' in request.path[:2] and \
                not '/static' in request.path[:7]:

            if request.GET.get('nomobile', False):
                request.session['nomobile'] = True
            elif not 'nomobile' in request.session:
                return HttpResponseRedirect('/m' + request.path)

        if hasattr(request, 'user') and request.user.is_authenticated():

            domain = getattr(settings, 'CURRENT_DOMAIN', 'default')
            cache.set('treeio_%s_last' % (domain), time.time())
            if getattr(settings, 'HARDTREE_SUBSCRIPTION_BLOCKED', False) and not '/accounts' in request.path:
                return HttpResponseRedirect('/accounts/logout')

            user = None
            try:
                user = request.user.get_profile()
                self.objects[unicode(user.id)] = {}
            except Exception:
                pass

            if not user:
                logout(request)
                return HttpResponseRedirect('/')

            do_fresh_subscribers = curry(
                self.do_fresh_subscribers, user, request)
            send_notifications_on_save = curry(
                self.send_notifications_on_save, user, request)
            send_notifications_on_delete = curry(
                self.send_notifications_on_delete, user, request)
            send_notifications_on_m2m = curry(
                self.send_notifcations_on_m2m, user, request)

            signals.pre_save.connect(
                send_notifications_on_save, dispatch_uid=request, weak=False)
            signals.post_save.connect(
                do_fresh_subscribers, dispatch_uid=request, weak=False)
            signals.pre_delete.connect(
                send_notifications_on_delete, dispatch_uid=request, weak=False)
            signals.m2m_changed.connect(
                send_notifications_on_m2m, dispatch_uid=request, weak=False)

    def do_fresh_subscribers(self, user, request, sender, instance, created, **kwargs):
        "Adds current user to Subscribers of an Object on creation"
        auto_notify = getattr(instance, 'auto_notify', True)
        if auto_notify and created:
            if isinstance(instance, Object) and instance.is_searchable():
                instance.subscribers.add(user)
                try:
                    instance.create_notification('create', user)
                except:
                    pass

    def send_notifications_on_save(self, user, request, sender, instance, **kwargs):
        "Send notifications to subscribers of an Object on Object change"
        auto_notify = getattr(instance, 'auto_notify', True)
        if auto_notify and isinstance(instance, Object) and instance.id:
            try:
                instance.create_notification('update', user)
            except:
                pass
        if isinstance(instance, Object):
            process_timezone_field(user, instance)

    def send_notifications_on_delete(self, user, request, sender, instance, **kwargs):
        "Send notifications to subscribers of an Object on Object delete"
        auto_notify = getattr(instance, 'auto_notify', True)
        if auto_notify and isinstance(instance, Object) and instance.get_related_object():
            try:
                instance.create_notification('delete', user)
            except:
                pass
            instance.subscribers.clear()

    def send_notifcations_on_m2m(self, user, request, sender, instance, action, reverse, model, pk_set, **kwargs):
        "Send notification on changes ManyToMany field (needs to be handled separately due to Django design)"

        if isinstance(instance, Object):
            attr = sender._meta.object_name.split('_', 1)[1]
            if attr in settings.HARDTREE_OBJECT_BLACKLIST:
                return

            if action == "pre_clear" or action == "pre_remove":
                original = list(getattr(instance, attr).all())
                self.objects[unicode(user.id)].update(
                    {unicode(instance.id): original})
            elif action == "post_add" or action == "post_remove":
                updated = list(getattr(instance, attr).all())
                if unicode(user.id) in self.objects and unicode(instance.id) in self.objects[unicode(user.id)]:
                    original = self.objects[
                        unicode(user.id)][unicode(instance.id)]
                    if not original == updated:
                        try:
                            instance.create_notification(
                                'm2m', user, field=attr, original=original, updated=updated)
                        except:
                            pass
                    del self.objects[unicode(user.id)][unicode(instance.id)]
        elif isinstance(instance, UpdateRecord):
            attr = sender._meta.object_name.split('_', 1)[1]
            if action == "post_add" and attr == 'about':
                obj_query = model.objects.filter(pk__in=pk_set)
                subscribers = set()
                # Send notifications to author Contact's subscribers too
                if instance.author:
                    contact = instance.author.get_contact()
                    if contact:
                        subscribers.update(contact.subscribers.all())
                    subscribers.add(instance.author)
                for obj in obj_query:
                    # add object's subscribes to update record
                    subscribers.update(obj.subscribers.all())
                for subscriber in subscribers:
                    instance.recipients.add(subscriber)
                for obj in obj_query:
                    instance.notify_subscribers(obj, request=request)

    def process_response(self, request, response):
        "Process response"
        signals.pre_save.disconnect(dispatch_uid=request)
        signals.post_save.disconnect(dispatch_uid=request)
        signals.m2m_changed.disconnect(dispatch_uid=request)
        signals.pre_delete.disconnect(dispatch_uid=request)

        try:
            user = request.user.get_profile()
            self.objects[unicode[user.id]] = {}
        except:
            pass

        return response


class PopupMiddleware():

    "Tracks Object creation for popups"

    objects = {}

    def __init__(self):
        "Initialize objects"
        self.objects = {}

    def process_request(self, request):
        "Process request"

        view = None
        try:
            view, args, kwargs = resolve(request.path)
        except Exception:
            pass

        if view == ajax_popup:
            process_created_object = curry(
                self.process_created_object, request)
            signals.post_save.connect(
                process_created_object, dispatch_uid=request.user, weak=False)

    def process_created_object(self, request, sender, instance, created, **kwargs):
        "Store a newly created object and request during which it was created"
        if isinstance(instance, Object) and created and not instance.is_attached():
            self.objects.update(
                {unicode(instance.id): {'object': instance, 'request': request}})

    def process_response(self, request, response):
        "Process response"
        if not getattr(request, 'user', None) or not request.user.username:
            return response

        try:
            signals.post_save.disconnect(dispatch_uid=request.user)
        except AttributeError:
            pass

        view = None
        try:
            view, args, kwargs = resolve(request.path)
        except Exception:
            pass

        if view == ajax_popup and response.status_code == 302:
            for obj in self.objects:
                if self.objects[obj]['request'] == request:
                    hobject = self.objects[obj]['object']
                    content = json.loads(response.content)
                    content['popup'].update({'object': {'name': unicode(hobject),
                                                        'id': obj}})
                    response = HttpResponse(json.dumps(content),
                                            mimetype=settings.HARDTREE_RESPONSE_FORMATS['json'])
                    break

            content = json.loads(response.content)
            content['popup'].update({'redirect': True})
            response = HttpResponse(json.dumps(content),
                                    mimetype=settings.HARDTREE_RESPONSE_FORMATS['json'])

        return response


class LanguageMiddleware():

    "Automatically set chosen language"

    def process_request(self, request):
        "Set language for the current user"

        lang = getattr(settings, 'HARDTREE_LANGUAGES_DEFAULT', 'en')

        if request.user.username:
            try:
                user = request.user.get_profile()
                conf = ModuleSetting.get('language', user=user)[0]
                lang = conf.value
            except IndexError:
                pass
            except AttributeError:
                pass
        else:
            try:
                conf = ModuleSetting.get(
                    'language', user__isnull=True, strict=True)[0]
                lang = conf.value
            except IndexError:
                pass
        translation.activate(lang)
        request.session['django_language'] = lang


def process_timezone_field(user, instance):
    "Processes date and datetime fields according to the selected time zone"
    from datetime import date, datetime, timedelta

    default_timezone = settings.HARDTREE_SERVER_DEFAULT_TIMEZONE
    try:
        conf = ModuleSetting.get('default_timezone')[0]
        default_timezone = conf.value
    except Exception:
        pass

    try:
        conf = ModuleSetting.get('default_timezone', user=user)[0]
        default_timezone = conf.value
    except Exception:
        default_timezone = getattr(
            settings, 'HARDTREE_SERVER_TIMEZONE')[default_timezone][0]

    all_timezones = getattr(settings, 'HARDTREE_SERVER_TIMEZONE', [
                            (1, '(GMT-11:00) International Date Line West')])
    title = all_timezones[int(default_timezone)][1]
    GMT = title[4:10]  # with sign e.g. +06:00
    sign = GMT[0:1]  # + or -
    hours = int(GMT[1:3])  # e.g. 06
    mins = int(GMT[4:6])

    for field in instance.get_fields():
        if field.name not in getattr(settings, 'HARDTREE_TIMEZONE_BLACKLIST', []):
            if isinstance(field, models.DateTimeField) or \
                    isinstance(field, models.DateField):
                if getattr(instance, field.name):
                    cur_date = getattr(instance, field.name)
                    if sign == "-":
                        new_date = cur_date + \
                            timedelta(hours=hours, minutes=mins)
                    else:
                        new_date = cur_date - \
                            timedelta(hours=hours, minutes=mins)
                    setattr(instance, field.name, new_date)
            elif isinstance(field, models.TimeField):
                if getattr(instance, field.name):
                    datetime.combine(date.today(), getattr(
                        instance, field.name)) + timedelta(hours=hours, minutes=mins)


class SSLMiddleware(object):

    """ Keep protocol the same on redirects """

    def process_request(self, request):
        """ Revert to SSL/no SSL depending on settings """
        if getattr(settings, 'HARDTREE_SUBSCRIPTION_SSL_ENABLED', True):
            if getattr(settings, 'HARDTREE_SUBSCRIPTION_SSL_ENFORCE', False) and not request.is_secure():
                redirect_url = request.build_absolute_uri()
                return HttpResponseRedirect(redirect_url.replace('https://', 'http://'))
        else:
            if request.is_secure():
                redirect_url = request.build_absolute_uri()
                return HttpResponseRedirect(redirect_url.replace('https://', 'http://'))

    def process_response(self, request, response):
        """ Keep protocol """
        if getattr(settings, 'HARDTREE_SUBSCRIPTION_SSL_ENABLED', True):
            if response.status_code == 302:
                redirect_url = request.build_absolute_uri(response['Location'])
                if request.is_secure() or getattr(settings, 'HARDTREE_SUBSCRIPTION_SSL_ENFORCE', False):
                    response['Location'] = redirect_url.replace(
                        'http://', 'https://')
        return response


class AuthMiddleware(object):

    """ Log in by hash """

    def process_request(self, request):
        authkey = request.GET.get('authkey', '')
        user = authenticate(authkey=authkey)

        if user:
            login(request, user)
            url = request.build_absolute_uri()
            p = urlparse.urlparse(url)
            params = urlparse.parse_qs(p.query)
            del params['authkey']
            url = urlparse.urlunparse(
                (p.scheme, p.netloc, p.path, p.params, urllib.urlencode(params, doseq=True), p.fragment))
            return HttpResponseRedirect(url)
