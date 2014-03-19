# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Messaging: test api
"""

import json
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, Perspective, ModuleSetting, Object
from treeio.messaging.models import Message, MessageStream, MailingList
from treeio.identities.models import Contact, ContactType


class MessagingApiTest(TestCase):

    "Messaging functional tests for api"

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

            self.contact_type = ContactType(name='test')
            self.contact_type.set_default_user()
            self.contact_type.save()

            self.contact = Contact(name='test', contact_type=self.contact_type)
            self.contact.set_default_user()
            self.contact.save()

            self.user_contact = Contact(
                name='test', related_user=self.user.get_profile(), contact_type=self.contact_type)
            self.user_contact.set_user(self.user)
            self.user_contact.save()

            self.stream = MessageStream(name='test')
            self.stream.set_default_user()
            self.stream.save()

            self.mlist = MailingList(name='test', from_contact=self.contact)
            self.mlist.set_default_user()
            self.mlist.save()

            self.message = Message(
                title='test', body='test', author=self.contact, stream=self.stream)
            self.message.set_default_user()
            self.message.save()

            self.client = Client()

            self.prepared = True

    def test_unauthenticated_access(self):
        "Test index page at /api/messaging/mlist"
        response = self.client.get('/api/messaging/mlist')
        # Redirects as unauthenticated
        self.assertEquals(response.status_code, 401)

    def test_get_mlist(self):
        """ Test index page api/messaging/mlist """
        response = self.client.get(
            path=reverse('api_messaging_mlist'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_one_mlist(self):
        response = self.client.get(path=reverse('api_messaging_mlist', kwargs={
                                   'object_ptr': self.mlist.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_mlist(self):
        updates = {"name": "API mailing list", "description": "API description update", "from_contact": self.contact.id,
                   "members": [self.contact.id, ]}
        response = self.client.put(path=reverse('api_messaging_mlist', kwargs={'object_ptr': self.mlist.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], updates['name'])
        self.assertEquals(data['description'], updates['description'])
        self.assertEquals(data['from_contact']['id'], updates['from_contact'])
        for i, member in enumerate(data['members']):
            self.assertEquals(member['id'], updates['members'][i])

    def test_get_streams(self):
        """ Test index page api/messaging/streams """
        response = self.client.get(
            path=reverse('api_messaging_streams'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_stream(self):
        response = self.client.get(path=reverse('api_messaging_streams', kwargs={
                                   'object_ptr': self.stream.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_stream(self):
        updates = {"name": "API stream", }
        response = self.client.put(path=reverse('api_messaging_streams', kwargs={'object_ptr': self.stream.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], updates['name'])

    def test_get_messages(self):
        """ Test index page api/messaging/messages """
        response = self.client.get(
            path=reverse('api_messaging_messages'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_message(self):
        response = self.client.get(path=reverse('api_messaging_messages', kwargs={
                                   'object_ptr': self.message.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_send_message(self):
        updates = {"title": "API message title", "body": "Test body", "stream": self.stream.id,
                   "multicomplete_recipients": u'test@test.com'}
        response = self.client.post(path=reverse('api_messaging_messages'), content_type=self.content_type,
                                    data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['title'], updates['title'])
        self.assertEquals(data['body'], updates['body'])
        self.assertEquals(data['stream']['id'], updates['stream'])

    def test_reply_to_message(self):
        updates = {"title": "API test", "body": "Test body", "stream": self.stream.id,
                   "multicomplete_recipients": u'test@test.com'}
        response = self.client.put(path=reverse('api_messaging_messages', kwargs={'object_ptr': self.message.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertNotEquals(data['title'], updates['title'])
        self.assertEquals(data['body'], updates['body'])
        self.assertEquals(data['stream']['id'], updates['stream'])
