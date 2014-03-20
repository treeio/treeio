# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Services: test suites
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, Perspective, ModuleSetting, Object
from treeio.services.models import Ticket, TicketQueue, TicketStatus, ServiceAgent, \
    Service, ServiceLevelAgreement
from treeio.identities.models import Contact, ContactType
import datetime


class ServicesModelsTest(TestCase):

    "Services DB models tests"

    def test_model(self):
        "Test Services models"
        status = TicketStatus(name='TestStatus')
        status.save()
        self.assertNotEquals(status.id, None)

        queue = TicketQueue(name='TestQueue', default_ticket_status=status)
        queue.save()
        self.assertNotEquals(status.id, None)

        ticket = Ticket(name='TestTicket', status=status, queue=queue)
        ticket.save()
        self.assertNotEquals(ticket.id, None)

        ticket.delete()
        queue.delete()
        status.delete()


class ServicesViewsTest(TestCase):

    "Services functional tests for views"

    username = "test"
    password = "password"
    prepared = False

    def setUp(self):
        "Initial Setup"

        if not self.prepared:
            # Clean up first
            Object.objects.all().delete()
            User.objects.all().delete()

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

            self.contact_type = ContactType(name='test')
            self.contact_type.set_default_user()
            self.contact_type.save()

            self.contact = Contact(name='test', contact_type=self.contact_type)
            self.contact.set_default_user()
            self.contact.save()

            self.status = TicketStatus(name='TestStatus')
            self.status.set_default_user()
            self.status.save()

            self.queue = TicketQueue(
                name='TestQueue', default_ticket_status=self.status)
            self.queue.set_default_user()
            self.queue.save()

            self.ticket = Ticket(
                name='TestTicket', status=self.status, queue=self.queue)
            self.ticket.set_default_user()
            self.ticket.save()

            self.agent = ServiceAgent(related_user=self.user, available_from=datetime.time(9),
                                      available_to=datetime.time(17))
            self.agent.set_default_user()
            self.agent.save()

            self.service = Service(name='test')
            self.service.set_default_user()
            self.service.save()

            self.sla = ServiceLevelAgreement(name='test', service=self.service,
                                             client=self.contact, provider=self.contact)
            self.sla.set_default_user()
            self.sla.save()

            self.client = Client()

            self.prepared = True

    ######################################
    # Testing views when user is logged in
    ######################################
    def test_index_login(self):
        "Test index page with login at /services/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('services'))
        self.assertEquals(response.status_code, 200)

    def test_index_owned(self):
        "Test index page with login at /services/owned"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('services_index_owned'))
        self.assertEquals(response.status_code, 200)

    def test_index_assigned(self):
        "Test index page with login at /services/assigned"

        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('services_index_assigned'))
        self.assertEquals(response.status_code, 200)

    # Queues
    def test_queue_add(self):
        "Test page with login at /services/queue/add"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('services_queue_add'))
        self.assertEquals(response.status_code, 200)

    def test_queue_view(self):
        "Test page with login at /services/queue/view/<queue_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('services_queue_view', args=[self.queue.id]))
        self.assertEquals(response.status_code, 200)

    def test_queue_edit(self):
        "Test page with login at /services/queue/edit/<queue_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('services_queue_edit', args=[self.queue.id]))
        self.assertEquals(response.status_code, 200)

    def test_queue_delete(self):
        "Test page with login at /services/queue/delete/<queue_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('services_queue_delete', args=[self.queue.id]))
        self.assertEquals(response.status_code, 200)

    # Statuses
    def test_status_view(self):
        "Test index page with login at /services/status/view/<status_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('services_status_view', args=[self.status.id]))
        self.assertEquals(response.status_code, 200)

    def test_status_edit(self):
        "Test index page with login at /services/status/edit/<status_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('services_status_edit', args=[self.status.id]))
        self.assertEquals(response.status_code, 200)

    def test_status_delete(self):
        "Test index page with login at /services/status/delete/<status_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('services_status_delete', args=[self.status.id]))
        self.assertEquals(response.status_code, 200)

    def test_status_add(self):
        "Test index page with login at /services/status/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('services_status_add'))
        self.assertEquals(response.status_code, 200)

    # Tickets
    def test_ticket_add(self):
        "Test page with login at /services/ticket/add"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('services_ticket_add'))
        self.assertEquals(response.status_code, 200)

    def test_ticket_add_by_queue(self):
        "Test page with login at /services/ticket/add/queue/(?P<queue_id>\d+)"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('services_ticket_add_by_queue', args=[self.queue.id]))
        self.assertEquals(response.status_code, 200)

    def test_ticket_view(self):
        "Test page with login at /services/ticket/view/<ticket_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('services_ticket_view', args=[self.ticket.id]))
        self.assertEquals(response.status_code, 200)

    def test_ticket_edit(self):
        "Test page with login at /services/ticket/edit/<ticket_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('services_ticket_edit', args=[self.ticket.id]))
        self.assertEquals(response.status_code, 200)

    def test_ticket_delete(self):
        "Test page with login at /services/ticket/delete/<ticket_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('services_ticket_delete', args=[self.ticket.id]))
        self.assertEquals(response.status_code, 200)

    def test_ticket_set_status(self):
        "Test page with login at /services/ticket/set/(?P<ticket_id>\d+)/status/(?P<status_id>\d+)"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('services_ticket_set_status', args=[self.ticket.id, self.status.id]))
        self.assertEquals(response.status_code, 200)

    # Settings
    def test_settings_view(self):
        "Test page with login at /services/settings/view"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('services_settings_view'))
        self.assertEquals(response.status_code, 200)

    def test_settings_edit(self):
        "Test page with login at /services/settings/edit"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('services_settings_view'))
        self.assertEquals(response.status_code, 200)

    # Catalogue
    def test_service_catalogue(self):
        "Test page with login at /services/catalogue"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('services_service_catalogue'))
        self.assertEquals(response.status_code, 200)

    # Services
    def test_service_view(self):
        "Test page with login at /services/service/view/<service_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('services_service_view', args=[self.service.id]))
        self.assertEquals(response.status_code, 200)

    def test_service_edit(self):
        "Test page with login at /services/service/edit/<service_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('services_service_edit', args=[self.service.id]))
        self.assertEquals(response.status_code, 200)

    def test_service_delete(self):
        "Test page with login at /services/service/delete/<service_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('services_service_delete', args=[self.service.id]))
        self.assertEquals(response.status_code, 200)

    def test_service_add(self):
        "Test page with login at /services/service/add"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('services_service_add'))
        self.assertEquals(response.status_code, 200)

    # SLAs
    def test_sla_index(self):
        "Test page with login at /services/sla"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('services_sla_index'))
        self.assertEquals(response.status_code, 200)

    def test_sla_view(self):
        "Test page with login at /services/sla/view/<sla_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('services_sla_view', args=[self.sla.id]))
        self.assertEquals(response.status_code, 200)

    def test_sla_edit(self):
        "Test page with login at /services/sla/edit/<sla_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('services_sla_edit', args=[self.sla.id]))
        self.assertEquals(response.status_code, 200)

    def test_sla_delete(self):
        "Test page with login at /services/sla/delete/<sla_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('services_sla_delete', args=[self.sla.id]))
        self.assertEquals(response.status_code, 200)

    def test_sla_add(self):
        "Test page with login at /services/sla/add"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('services_sla_index'))
        self.assertEquals(response.status_code, 200)

    # Agents
    def test_agent_index(self):
        "Test page with login at /services/agent"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('services_agent_index'))
        self.assertEquals(response.status_code, 200)

    def test_agent_view(self):
        "Test page with login at /services/agent/view/<agent_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('services_agent_view', args=[self.agent.id]))
        self.assertEquals(response.status_code, 200)

    def test_agent_edit(self):
        "Test page with login at /services/agent/edit/<agent_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('services_agent_edit', args=[self.agent.id]))
        self.assertEquals(response.status_code, 200)

    def test_agent_delete(self):
        "Test page with login at /services/agent/delete/<agent_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('services_agent_delete', args=[self.agent.id]))
        self.assertEquals(response.status_code, 200)

    def test_agent_add(self):
        "Test page with login at /services/agent/add"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('services_agent_add'))
        self.assertEquals(response.status_code, 200)

    ######################################
    # Testing views when user is not logged in
    ######################################
    def test_index(self):
        "Test index page at /services/"
        response = self.client.get(reverse('services'))
        # Redirects as unauthenticated
        self.assertRedirects(response, reverse('user_login'))

    def test_index_owned_out(self):
        "Testing /services/owned"
        response = self.client.get(reverse('services_index_owned'))
        self.assertRedirects(response, reverse('user_login'))

    def test_index_assigned_out(self):
        "Testing /services/assigned"
        response = self.client.get(reverse('services_index_assigned'))
        self.assertRedirects(response, reverse('user_login'))

    # Queues
    def test_queue_add_out(self):
        "Testing /services/queue/add"
        response = self.client.get(reverse('services_queue_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_queue_view_out(self):
        "Testing /services/queue/view/<queue_id>"
        response = self.client.get(
            reverse('services_queue_view', args=[self.queue.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_queue_edit_out(self):
        "Testing /services/queue/edit/<queue_id>"
        response = self.client.get(
            reverse('services_queue_edit', args=[self.queue.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_queue_delete_out(self):
        "Testing /services/queue/delete/<queue_id>"
        response = self.client.get(
            reverse('services_queue_delete', args=[self.queue.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Statuses
    def test_status_view_out(self):
        "Testing /services/status/view/<status_id>"
        response = self.client.get(
            reverse('services_status_view', args=[self.status.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_status_edit_out(self):
        "Testing /services/status/edit/<status_id>"
        response = self.client.get(
            reverse('services_status_edit', args=[self.status.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_status_delete_out(self):
        "Testing /services/status/delete/<status_id>"
        response = self.client.get(
            reverse('services_status_delete', args=[self.status.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_status_add_out(self):
        "Testing /services/status/add/"
        response = self.client.get(reverse('services_status_add'))
        self.assertRedirects(response, reverse('user_login'))

    # Tickets
    def test_ticket_add_out(self):
        "Testing /services/ticket/add"
        response = self.client.get(reverse('services_ticket_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_ticket_add_by_queue_out(self):
        "Testing /services/ticket/add/queue/(?P<queue_id>\d+)"
        response = self.client.get(
            reverse('services_ticket_add_by_queue', args=[self.queue.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_ticket_view_out(self):
        "Testing /services/ticket/view/<ticket_id>"
        response = self.client.get(
            reverse('services_ticket_view', args=[self.ticket.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_ticket_edit_out(self):
        "Testing /services/ticket/edit/<ticket_id>"
        response = self.client.get(
            reverse('services_ticket_edit', args=[self.ticket.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_ticket_delete_out(self):
        "Testing /services/ticket/delete/<ticket_id>"
        response = self.client.get(
            reverse('services_ticket_delete', args=[self.ticket.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_ticket_set_status_out(self):
        "Testing /services/ticket/set/(?P<ticket_id>\d+)/status/(?P<status_id>\d+)"
        response = self.client.get(
            reverse('services_ticket_set_status', args=[self.ticket.id, self.status.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Settings
    def test_settings_view_out(self):
        "Testing /services/settings/view"
        response = self.client.get(reverse('services_settings_view'))
        self.assertRedirects(response, reverse('user_login'))

    def test_settings_edit_out(self):
        "Testing /services/settings/edit"
        response = self.client.get(reverse('services_settings_view'))
        self.assertRedirects(response, reverse('user_login'))

    # Catalogue
    def test_service_catalogue_out(self):
        "Testing /services/catalogue"
        response = self.client.get(reverse('services_service_catalogue'))
        self.assertRedirects(response, reverse('user_login'))

    # Services
    def test_service_view_out(self):
        "Testing /services/service/view/<service_id>"
        response = self.client.get(
            reverse('services_service_view', args=[self.service.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_service_edit_out(self):
        "Testing /services/service/edit/<service_id>"
        response = self.client.get(
            reverse('services_service_edit', args=[self.service.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_service_delete_out(self):
        "Testing /services/service/delete/<service_id>"
        response = self.client.get(
            reverse('services_service_delete', args=[self.service.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_service_add_out(self):
        "Testing /services/service/add"
        response = self.client.get(reverse('services_service_add'))
        self.assertRedirects(response, reverse('user_login'))

    # SLAs
    def test_sla_index_out(self):
        "Testing /services/sla"
        response = self.client.get(reverse('services_sla_index'))
        self.assertRedirects(response, reverse('user_login'))

    def test_sla_view_out(self):
        "Testing /services/sla/view/<sla_id>"
        response = self.client.get(
            reverse('services_sla_view', args=[self.sla.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_sla_edit_out(self):
        "Testing /services/sla/edit/<sla_id>"
        response = self.client.get(
            reverse('services_sla_edit', args=[self.sla.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_sla_delete_out(self):
        "Testing /services/sla/delete/<sla_id>"
        response = self.client.get(
            reverse('services_sla_delete', args=[self.sla.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_sla_add_out(self):
        "Testing /services/sla/add"
        response = self.client.get(reverse('services_sla_index'))
        self.assertRedirects(response, reverse('user_login'))

    # Agents
    def test_agent_index_out(self):
        "Testing /services/agent"
        response = self.client.get(reverse('services_agent_index'))
        self.assertRedirects(response, reverse('user_login'))

    def test_agent_view_out(self):
        "Testing /services/agent/view/<agent_id>"
        response = self.client.get(
            reverse('services_agent_view', args=[self.agent.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_agent_edit_out(self):
        "Testing /services/agent/edit/<agent_id>"
        response = self.client.get(
            reverse('services_agent_edit', args=[self.agent.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_agent_delete_out(self):
        "Test page with login at /services/agent/delete/<agent_id>"
        response = self.client.get(
            reverse('services_agent_delete', args=[self.agent.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_agent_add_out(self):
        "Test page with login at /services/agent/add"
        response = self.client.get(reverse('services_agent_add'))
        self.assertRedirects(response, reverse('user_login'))
