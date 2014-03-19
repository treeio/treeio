# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Events: test api
"""
import json
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, Perspective, ModuleSetting, Object
from treeio.events.models import Event
from datetime import datetime


class EventsViewsTest(TestCase):

    "Events functional tests for api"

    username = "api_test"
    password = "api_password"
    prepared = False
    authentication_headers = {"CONTENT_TYPE": "application/json",
                              "HTTP_AUTHORIZATION": "Basic YXBpX3Rlc3Q6YXBpX3Bhc3N3b3Jk"}
    content_type = 'application/json'

    def setUp(self):
        "Initial Setup"

        if not self.prepared:
            # Clean up first
            Object.objects.all().delete()

            # Create objects
            try:
                self.group = Group.objects.get(name='test')
            except Group.DoesNotExist:
                Group.objects.all().delete()
                self.group = Group(name='test')
                self.group.save()

            try:
                self.user = DjangoUser.objects.get(username=self.username)
                self.user.set_password(self.password)
                try:
                    self.profile = self.user.get_profile()
                except Exception:
                    User.objects.all().delete()
                    self.user = DjangoUser(username=self.username, password='')
                    self.user.set_password(self.password)
                    self.user.save()
            except DjangoUser.DoesNotExist:
                User.objects.all().delete()
                self.user = DjangoUser(username=self.username, password='')
                self.user.set_password(self.password)
                self.user.save()

            try:
                perspective = Perspective.objects.get(name='default')
            except Perspective.DoesNotExist:
                Perspective.objects.all().delete()
                perspective = Perspective(name='default')
                perspective.set_default_user()
                perspective.save()

            ModuleSetting.set('default_perspective', perspective.id)

            self.event = Event(name='TestStatus', end=datetime.now())
            self.event.set_default_user()
            self.event.save()

            self.client = Client()

            self.prepared = True

    def test_unauthenticated_access(self):
        "Test index page at /api/calendar/events"
        response = self.client.get('/api/calendar/events')
        # Redirects as unauthenticated
        self.assertEquals(response.status_code, 401)

    def test_get_events_list(self):
        """ Test index page api/infrastructure/types """
        response = self.client.get(
            path=reverse('api_events'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_field(self):
        response = self.client.get(path=reverse(
            'api_events', kwargs={'object_ptr': self.event.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_field(self):
        updates = {"name": "Api_name", "details": "Api details",
                   "start": "2011-03-01 01:12:09", "end": "2011-03-09 13:05:09"}
        response = self.client.put(path=reverse('api_events', kwargs={'object_ptr': self.event.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], updates['name'])
        self.assertEquals(data['details'], updates['details'])
        self.assertEquals(data['start'], updates['start'])
        self.assertEquals(data['end'], updates['end'])
