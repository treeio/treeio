# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Events: test suites
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, Perspective, ModuleSetting, Object
from treeio.events.models import Event
from datetime import datetime


class EventsModelTest(TestCase):

    "Events DB models tests"

    def test_model_event(self):
        "Test Event model"
        event = Event(name="Test", end=datetime.now())
        event.save()
        self.assertNotEquals(event.id, None)

        event.delete()


class EventsViewsTest(TestCase):

    "Events functional tests for views"

    username = "test"
    password = "password"
    prepared = False

    def setUp(self):
        "Initial Setup"

        if not self.prepared:
            # Clean up first
            Object.objects.all().delete()

            # Create objects
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

            self.event = Event(name='TestStatus', end=datetime.now())
            self.event.set_default_user()
            self.event.save()

            self.client = Client()

            self.prepared = True

    ######################################
    # Testing views when user is logged in
    ######################################
    def test_index(self):
        "Test index page with login at /calendar/index"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('events_index'))
        self.assertEquals(response.status_code, 200)

    def test_upcoming(self):
        "Test index page with login at /calendar/upcoming"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('events_upcoming'))
        self.assertEquals(response.status_code, 200)

    def test_month(self):
        "Test index page with login at /calendar/month"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('events_month'))
        self.assertEquals(response.status_code, 200)

    def test_week(self):
        "Test index page with login at /calendar/week"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('events_week'))
        self.assertEquals(response.status_code, 200)

    def test_day(self):
        "Test index page with login at /calendar/day"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('events_day'))
        self.assertEquals(response.status_code, 200)

    # Events
    def test_event_add(self):
        "Test index page with login at /calendar/event/view/<event_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('events_event_add'))
        self.assertEquals(response.status_code, 200)
        # form
        self.assertEquals(Event.objects.count(), 1)
        post_data = {
            'name': 'TestStatus',
            'end': datetime.now()
        }
        response = self.client.post(reverse('events_event_add'), post_data)
        self.assertEquals(response.status_code, 302)  # redirect somewhere
        self.assertEquals(Event.objects.count(), 2)

    def test_event_view(self):
        "Test index page with login at /calendar/event/view/<event_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('events_event_view', args=[self.event.id]))
        self.assertEquals(response.status_code, 200)

    def test_event_edit(self):
        "Test index page with login at /calendar/event/edit/<event_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('events_event_edit', args=[self.event.id]))
        self.assertEquals(response.status_code, 200)

    def test_event_delete(self):
        "Test index page with login at /calendar/event/delete/<event_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('events_event_delete', args=[self.event.id]))
        self.assertEquals(response.status_code, 200)

    ######################################
    # Testing views when user is not logged in
    ######################################

    def test_index_anonymous(self):
        "Test index page at /calendar/"
        response = self.client.get(reverse('events'))
        # Redirects as unauthenticated
        self.assertRedirects(response, reverse('user_login'))

    def test_index_out(self):
        "Testing /calendar/index"
        response = self.client.get(reverse('events_index'))
        self.assertRedirects(response, reverse('user_login'))

    def test_upcoming_out(self):
        "Testing /calendar/upcoming"
        response = self.client.get(reverse('events_upcoming'))
        self.assertRedirects(response, reverse('user_login'))

    def test_month_out(self):
        "Testing /calendar/month"
        response = self.client.get(reverse('events_month'))
        self.assertRedirects(response, reverse('user_login'))

    def test_week_out(self):
        "Testing /calendar/week"
        response = self.client.get(reverse('events_week'))
        self.assertRedirects(response, reverse('user_login'))

    def test_day_out(self):
        "Testing /calendar/day"
        response = self.client.get(reverse('events_day'))
        self.assertRedirects(response, reverse('user_login'))

    # Events
    def test_event_add_out(self):
        "Testing /calendar/event/view/<event_id>"
        response = self.client.get(reverse('events_event_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_event_view_out(self):
        "Testing /calendar/event/view/<event_id>"
        response = self.client.get(
            reverse('events_event_view', args=[self.event.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_event_edit_out(self):
        "Testing /calendar/event/edit/<event_id>"
        response = self.client.get(
            reverse('events_event_edit', args=[self.event.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_event_delete_out(self):
        "Testing /calendar/event/delete/<event_id>"
        response = self.client.get(
            reverse('events_event_delete', args=[self.event.id]))
        self.assertRedirects(response, reverse('user_login'))
