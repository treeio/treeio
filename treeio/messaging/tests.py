# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Messaging: test suites
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, Perspective, ModuleSetting
from treeio.messaging.models import Message, MessageStream
from treeio.identities.models import Contact, ContactType


class MessagingModelsTest(TestCase):

    " Messaging models tests"

    username = "test"
    password = "password"

    def test_model_message(self):
        "Test message"

        contact_type = ContactType(name='test')
        contact_type.save()

        contact = Contact(name='test', contact_type=contact_type)
        contact.save()

        self.user = DjangoUser(username=self.username, password='')
        self.user.set_password(self.password)
        self.user.save()

        user = User(name='test', user=self.user)
        user.save()

        stream = MessageStream(name='test')
        stream.save()

        obj = Message(title='test', body='test', author=contact, stream=stream)
        obj.save()
        self.assertEquals('test', obj.title)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_message_stream(self):
        "Test message"

        obj = MessageStream(name='test')
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()


class MessagingViewsTest(TestCase):

    "Messaging functional tests for views"

    username = "test"
    password = "password"
    prepared = False

    def setUp(self):
        "Initial Setup"

        if not self.prepared:
            self.group, created = Group.objects.get_or_create(name='test')
            duser, created = DjangoUser.objects.get_or_create(
                username=self.username)
            duser.set_password(self.password)
            duser.save()
            self.user, created = User.objects.get_or_create(user=duser)
            self.user.save()
            perspective, created = Perspective.objects.get_or_create(
                name='default')
            perspective.set_default_user()
            perspective.save()
            ModuleSetting.set('default_perspective', perspective.id)

            self.contact_type = ContactType(name='test')
            self.contact_type.set_default_user()
            self.contact_type.save()

            self.contact = Contact(name='test', contact_type=self.contact_type)
            self.contact.set_default_user()
            self.contact.save()

            self.stream = MessageStream(name='test')
            self.stream.set_default_user()
            self.stream.save()

            self.message = Message(
                title='test', body='test', author=self.contact, stream=self.stream)
            self.message.set_default_user()
            self.message.save()

            self.client = Client()

            self.prepared = True

    ######################################
    # Testing views when user is logged in
    ######################################
    def test_message_index_login(self):
        "Test index page with login at /messaging/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('messaging'))
        self.assertEquals(response.status_code, 200)

    def test_message_index_sent(self):
        "Test index page with login at /messaging/sent/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('messaging_sent'))
        self.assertEquals(response.status_code, 200)

    def test_message_index_inbox(self):
        "Test index page with login at /messaging/inbox/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('messaging_inbox'))
        self.assertEquals(response.status_code, 200)

    def test_message_index_unread(self):
        "Test index page with login at /messaging/unread/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('messaging_unread'))
        self.assertEquals(response.status_code, 200)

    # Messages
    def test_message_compose_login(self):
        "Test index page with login at /message/compose/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('messaging_message_compose'))
        self.assertEquals(response.status_code, 200)

    def test_message_view_login(self):
        "Test index page with login at /message/view/<message_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('messaging_message_view', args=[self.message.id]))
        self.assertEquals(response.status_code, 200)

    def test_message_delete_login(self):
        "Test index page with login at /message/edit/<message_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('messaging_message_delete', args=[self.message.id]))
        self.assertEquals(response.status_code, 200)

    # Streams
    def test_stream_add(self):
        "Test index page with login at /stream/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('messaging_stream_edit', args=[self.stream.id]))
        self.assertEquals(response.status_code, 200)

    def test_stream_view(self):
        "Test index page with login at /stream/view/<stream_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('messaging_stream_view', args=[self.stream.id]))
        self.assertEquals(response.status_code, 200)

    def test_stream_edit(self):
        "Test index page with login at /stream/edit/<stream_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('messaging_stream_edit', args=[self.stream.id]))
        self.assertEquals(response.status_code, 200)

    def test_stream_delete(self):
        "Test index page with login at /stream/delete/<stream_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('messaging_stream_delete', args=[self.stream.id]))
        self.assertEquals(response.status_code, 200)

    # Settings
    def test_messaging_settings_view(self):
        "Test index page with login at /messaging/settings/view/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('messaging_settings_view'))
        self.assertEquals(response.status_code, 200)

    def test_finance_settings_edit(self):
        "Test index page with login at /messaging/settings/edit/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('messaging_settings_edit'))
        self.assertEquals(response.status_code, 200)

    ######################################
    # Testing views when user is not logged in
    ######################################
    def test_message_index_out(self):
        "Test index page at /messaging/"
        response = self.client.get(reverse('messaging'))
        # Redirects as unauthenticated
        self.assertRedirects(response, reverse('user_login'))

    def test_message_sent_out(self):
        "Testing /messaging/sent/"
        response = self.client.get(reverse('messaging_sent'))
        # Redirects as unauthenticated
        self.assertRedirects(response, reverse('user_login'))

    def test_message_inbox_out(self):
        "Testing /messaging/inbox/"
        response = self.client.get(reverse('messaging_inbox'))
        # Redirects as unauthenticated
        self.assertRedirects(response, reverse('user_login'))

    def test_message_unread_out(self):
        "Testing /messaging/unread/"
        response = self.client.get(reverse('messaging_unread'))
        # Redirects as unauthenticated
        self.assertRedirects(response, reverse('user_login'))

    # Messages
    def test_message_compose_out(self):
        "Testing /message/compose/"
        response = self.client.get(reverse('messaging_message_compose'))
        self.assertRedirects(response, reverse('user_login'))

    def test_message_view_out(self):
        "Test index page with login at /message/view/<message_id>"
        response = self.client.get(
            reverse('messaging_message_view', args=[self.message.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_message_delete_out(self):
        "Test index page with login at /message/edit/<message_id>"
        response = self.client.get(
            reverse('messaging_message_delete', args=[self.message.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Streams
    def test_stream_add_out(self):
        "Testing /stream/add/"
        response = self.client.get(
            reverse('messaging_stream_edit', args=[self.stream.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_stream_view_out(self):
        "Testing /stream/view/<stream_id>"
        response = self.client.get(
            reverse('messaging_stream_view', args=[self.stream.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_stream_edit_out(self):
        "Testing /stream/edit/<stream_id>"
        response = self.client.get(
            reverse('messaging_stream_edit', args=[self.stream.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_stream_delete_out(self):
        "Testing /stream/delete/<stream_id>"
        response = self.client.get(
            reverse('messaging_stream_delete', args=[self.stream.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Settings
    def test_messaging_settings_view_out(self):
        "Testing /messaging/settings/view/"
        response = self.client.get(reverse('messaging_settings_view'))
        self.assertRedirects(response, reverse('user_login'))

    def test_finance_settings_edit_out(self):
        "Testing /messaging/settings/edit/"
        response = self.client.get(reverse('messaging_settings_edit'))
        self.assertRedirects(response, reverse('user_login'))
