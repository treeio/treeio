# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- coding: utf-8 -*-

import urllib
import json
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, Perspective, ModuleSetting, Object
from treeio.services.models import Ticket, TicketQueue, TicketStatus, ServiceAgent, \
    Service, ServiceLevelAgreement
from treeio.identities.models import Contact, ContactType
import datetime


class ServicesViewsTest(TestCase):

    "Services functional tests for api"

    username = "api_test"
    password = "api_password"
    prepared = False
    authentication_headers = {"CONTENT_TYPE": "application/json",
                              "HTTP_AUTHORIZATION": "Basic YXBpX3Rlc3Q6YXBpX3Bhc3N3b3Jk"}
    content_type = 'application/json'
    prepared = False

    def setUp(self):
        "Initial Setup"

        if not self.prepared:
            # Clean up first
            Object.objects.all().delete()
            User.objects.all().delete()

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
                perspective.set_user(self.user.get_profile())
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

            self.agent = ServiceAgent(related_user=self.user.get_profile(), available_from=datetime.time(9),
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

    def test_unauthenticated_access(self):
        "Test index page at /api/services/services"
        response = self.client.get('/api/services/services')
        # Redirects as unauthenticated
        self.assertEquals(response.status_code, 401)

    def test_get_ticket_statuses_list(self):
        """ Test index page api/services/status """
        response = self.client.get(
            path=reverse('api_services_status'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_status(self):
        response = self.client.get(path=reverse('api_services_status', kwargs={
                                   'object_ptr': self.status.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_status(self):
        updates = {'name': 'Api update', 'details': '<p>api details</p>'}
        response = self.client.put(path=reverse('api_services_status', kwargs={'object_ptr': self.status.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_services_list(self):
        """ Test index page api/services """
        response = self.client.get(
            path=reverse('api_services'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_service(self):
        response = self.client.get(path=reverse(
            'api_services', kwargs={'object_ptr': self.service.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_service(self):
        updates = {'name': 'Api update', 'details': '<p>api details</p>'}
        response = self.client.put(path=reverse('api_services', kwargs={'object_ptr': self.service.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_sla_list(self):
        """ Test index page api/services/sla """
        response = self.client.get(
            path=reverse('api_services_sla'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_sla(self):
        response = self.client.get(path=reverse(
            'api_services_sla', kwargs={'object_ptr': self.sla.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_sla(self):
        updates = {'name': 'Api update',
                   'service': self.service.id, 'provider': self.contact.id}
        response = self.client.put(path=reverse('api_services_sla', kwargs={'object_ptr': self.sla.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_agents_list(self):
        """ Test index page api/services/agents """
        response = self.client.get(
            path=reverse('api_services_agents'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_agent(self):
        response = self.client.get(path=reverse('api_services_agents', kwargs={
                                   'object_ptr': self.agent.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_agents(self):
        updates = {"activate": True, "related_user": User.objects.all()[0].id}
        response = self.client.put(path=reverse('api_services_agents', kwargs={'object_ptr': self.agent.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_queues_list(self):
        """ Test index page api/services/queues """
        response = self.client.get(
            path=reverse('api_services_queues'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_queue(self):
        response = self.client.get(path=reverse('api_services_queues', kwargs={
                                   'object_ptr': self.queue.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_queue(self):
        updates = {"name": "Api test", "default_ticket_priority": 5, "ticket_code": "api",
                   "waiting_time": 300, "default_ticket_status": self.status.id}
        response = self.client.put(path=reverse('api_services_queues', kwargs={'object_ptr': self.queue.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_records(self):
        """ Test index page api/services/ticket/records/{ticket number} """
        response = self.client.get(path=reverse('api_services_ticket_records', kwargs={
                                   'ticket_id': self.ticket.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_create_record(self):
        new_record = {"body": "api test message", "notify": False}
        response = self.client.post(path=reverse('api_services_ticket_records', kwargs={'ticket_id': self.ticket.id}),
                                    data=json.dumps(new_record), content_type=self.content_type, **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(new_record['body'], data['body'])

    def test_get_tasks_list(self):
        """ Test index page api/services/tasks """
        response = self.client.get(
            path=reverse('api_services_tickets'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_ticket(self):
        response = self.client.get(path=reverse('api_services_tickets', kwargs={
                                   'object_ptr': self.ticket.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_ticket(self):
        updates = {"name": "Api updates",
                   "status": self.status.id, "priority": 3, "urgency": 5}
        response = self.client.put(path=reverse('api_services_tickets', kwargs={'object_ptr': self.ticket.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_create_ticket(self):
        new_ticket = {"name": "Api creates",
                      "status": self.status.id, "priority": 3, "urgency": 5}
        response = self.client.post(path=reverse('api_services_tickets',) + '?' + urllib.urlencode({'queue_id': self.queue.id}),
                                    content_type=self.content_type, data=json.dumps(new_ticket), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(new_ticket["name"], data["name"])
        self.assertEquals(new_ticket["urgency"], data["urgency"])
        self.assertEquals(new_ticket["priority"], data["priority"])
        self.assertEquals(new_ticket["status"], data["status"]["id"])
