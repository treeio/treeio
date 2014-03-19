# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
API Project Management: test suites
"""
from time import sleep
import json
from datetime import datetime
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser

from treeio.identities.models import Contact, ContactType
from treeio.core.models import User, Group, Perspective, ModuleSetting, Object
from treeio.projects.models import Project, Milestone, Task, TaskStatus, TaskTimeSlot


class ProjectsAPITest(TestCase):

    "Projects functional tests for api"
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
            User.objects.all().delete()

            # Create objects

            try:
                self.group = Group.objects.get(name='api_test')
            except Group.DoesNotExist:
                Group.objects.all().delete()
                self.group = Group(name='api_test')
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

            self.contact_type = ContactType(name='api_test')
            self.contact_type.set_default_user()
            self.contact_type.save()

            self.contact = Contact(
                name='api_test', contact_type=self.contact_type)
            self.contact.set_default_user()
            self.contact.save()

            self.project = Project(
                name='api_test', manager=self.contact, client=self.contact)
            self.project.set_default_user()
            self.project.save()

            self.status = TaskStatus(name='api_test')
            self.status.set_default_user()
            self.status.save()

            self.milestone = Milestone(
                name='api_test', project=self.project, status=self.status)
            self.milestone.set_default_user()
            self.milestone.save()

            self.task = Task(
                name='api_test', project=self.project, status=self.status, priority=3)
            self.task.set_default_user()
            self.task.save()

            self.time_slot = TaskTimeSlot(
                task=self.task, details='api_test', time_from=datetime.now(), user=self.user.get_profile())
            self.time_slot.set_default_user()
            self.time_slot.save()

            self.parent = Project(name='api_test')
            self.parent.set_default_user()
            self.parent.save()

            self.parent_task = Task(
                name='api_test', project=self.project, status=self.status, priority=3)
            self.parent_task.set_default_user()
            self.parent_task.save()

            self.client = Client()

            self.prepared = True

    def test_unauthenticated_access(self):
        "Test index page at /projects"
        response = self.client.get('/api/projects/projects')
        # Redirects as unauthenticated
        self.assertEquals(response.status_code, 401)

    # Get info about projects, milestones, status, tasks, tasktimes.

    def test_get_project_list(self):
        """ Test index page api/projects """
        response = self.client.get(
            path=reverse('api_projects'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_status_list(self):
        """ Test index page api/status """
        response = self.client.get(
            path=reverse('api_projects_status'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_milestones_list(self):
        """ Test index page api/milestones """
        response = self.client.get(
            path=reverse('api_projects_milestones'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_task_list(self):
        """ Test index page api/tasks """
        response = self.client.get(
            path=reverse('api_projects_tasks'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_tasktimes_list(self):
        """ Test index page api/tasktimes """
        response = self.client.get(
            path=reverse('api_projects_tasktimes'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_project(self):
        response = self.client.get(reverse(
            'api_projects', kwargs={'object_ptr': self.project.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['id'], self.project.id)
        self.assertEquals(data['name'], self.project.name)
        self.assertEquals(data['details'], self.project.details)

    def test_get_status(self):
        response = self.client.get(reverse('api_projects_status', kwargs={
                                   'object_ptr': self.status.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['id'], self.status.id)
        self.assertEquals(data['name'], self.status.name)

    def test_get_milestone(self):
        response = self.client.get(reverse('api_projects_milestones', kwargs={
                                   'object_ptr': self.milestone.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['id'], self.milestone.id)
        self.assertEquals(data['name'], self.milestone.name)
        self.assertEquals(data['project']['id'], self.milestone.project.id)
        self.assertEquals(data['status']['id'], self.milestone.status.id)

    def test_get_task(self):
        response = self.client.get(reverse('api_projects_tasks', kwargs={
                                   'object_ptr': self.task.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['id'], self.task.id)
        self.assertEquals(data['name'], self.task.name)
        self.assertEquals(data['priority'], self.task.priority)
        self.assertEquals(data['project']['id'], self.task.project.id)
        self.assertEquals(data['status']['id'], self.task.status.id)

    def test_get_timeslot(self):
        response = self.client.get(reverse('api_projects_tasktimes', kwargs={
                                   'object_ptr': self.time_slot.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['id'], self.time_slot.id)
        self.assertEquals(data['task']['id'], self.time_slot.task.id)

    # Common test

    def test_common_project(self):

        # create new project
        new_project = {'name': 'api test',
                       'details': '<p>test details</p>'}
        response = self.client.post(reverse('api_projects'), data=json.dumps(new_project),
                                    content_type=self.content_type, **self.authentication_headers)
        # print response.request
        self.assertEquals(response.status_code, 200)

        # check data in response
        data = json.loads(response.content)
        self.assertEquals(data['name'], new_project['name'])
        self.assertEquals(data['details'], new_project['details'])
        project_id = data['id']

        # get info about new project
        response = self.client.get(path=reverse(
            'api_projects', kwargs={'object_ptr': project_id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        # get statuses list
        response = self.client.get(
            path=reverse('api_projects_status'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        statuses = json.loads(response.content)
        fstatus = statuses[0]['id']

        # create new task status
        new_status = {'name': 'Open api test',
                      'active': True,
                      'hidden': False,
                      'details': '<p>test details</p>'}
        response = self.client.post(reverse('api_projects_status'), data=json.dumps(new_status),
                                    content_type=self.content_type, **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], new_status['name'])
        self.assertEquals(data['active'], new_status['active'])
        self.assertEquals(data['hidden'], new_status['hidden'])
        self.assertEquals(data['details'], new_status['details'])
        sstatus = data['id']

        # create new milestone
        new_milestone = {'name': 'api test milestone',
                         'status': fstatus,
                         'project': project_id,
                         'start_date': '2011-06-09 12:00:00',
                         'details': '<p>test details</p>'}
        response = self.client.post(reverse('api_projects_milestones'), data=json.dumps(new_milestone),
                                    content_type=self.content_type, **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], new_milestone['name'])
        self.assertEquals(data['status']['id'], new_milestone['status'])
        self.assertEquals(data['project']['id'], new_milestone['project'])
        self.assertEquals(data['details'], new_milestone['details'])
        milestone_id = data['id']

        #  create new task
        new_task = {'name': 'api test task',
                    'status': sstatus,
                    'project': project_id,
                    'milestone': milestone_id,
                    'priority': 5,
                    'start_date': '2011-06-02 12:00:00',
                    'estimated_time': 5000,
                    'details': '<p>test details</p>'
                    }
        response = self.client.post(reverse('api_projects_tasks'), data=json.dumps(new_task),
                                    content_type=self.content_type, **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], new_task['name'])
        self.assertEquals(data['priority'], new_task['priority'])
        self.assertEquals(data['status']['id'], new_task['status'])
        self.assertEquals(data['project']['id'], new_task['project'])
        self.assertEquals(data['milestone']['id'], new_task['milestone'])
        self.assertEquals(data['estimated_time'], new_task['estimated_time'])
        self.assertEquals(data['details'], new_task['details'])
        task_id = data['id']

        # create new subtask
        new_sub_task = {'name': 'api test task',
                        'status': sstatus,
                        'parent': task_id,
                        'project': project_id,
                        'priority': 5,
                        'start_date': '2011-06-02 13:00:00',
                        'estimated_time': 2500,
                        'details': '<p>test details</p>'
                        }

        response = self.client.post(reverse('api_projects_tasks'), data=json.dumps(new_sub_task),
                                    content_type=self.content_type, **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], new_sub_task['name'])
        self.assertEquals(data['priority'], new_sub_task['priority'])
        self.assertEquals(data['status']['id'], new_sub_task['status'])
        self.assertEquals(data['parent']['id'], new_sub_task['parent'])
        self.assertEquals(data['project']['id'], new_sub_task['project'])
        self.assertEquals(
            data['estimated_time'], new_sub_task['estimated_time'])
        self.assertEquals(data['details'], new_sub_task['details'])
        sub_task_id = data['id']

        # create task time
        new_tasktime = {'task': task_id,
                        'minutes': 400,
                        'details': '<p>test details</p>'
                        }

        response = self.client.post(reverse('api_projects_tasktimes'), data=json.dumps(new_tasktime),
                                    content_type=self.content_type, **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['task']['id'], new_tasktime['task'])
        self.assertEquals(data['details'], new_tasktime['details'])
        tasktime_id = data['id']

        # start task time
        response = self.client.get(path=reverse('api_projects_tasktime_start', kwargs={
                                   'task_id': sub_task_id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        slot_id = data['id']

        sleep(60)

        # stop task time
        response = self.client.post(reverse('api_projects_tasktime_stop', kwargs={'slot_id': slot_id}), data=json.dumps({'details': '<p>test details</p>'}),
                                    content_type=self.content_type, **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        # delete task time
        response = self.client.delete(reverse('api_projects_tasktimes', kwargs={
                                      'object_ptr': tasktime_id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 204)

        # delete task
        response = self.client.delete(reverse(
            'api_projects_tasks', kwargs={'object_ptr': task_id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 204)

        # check subtask
        response = self.client.get(path=reverse('api_projects_tasks', kwargs={
                                   'object_ptr': sub_task_id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 404)

        # delete milestone
        response = self.client.delete(reverse('api_projects_milestones', kwargs={
                                      'object_ptr': milestone_id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 204)

        # delete status
        response = self.client.delete(reverse(
            'api_projects_status', kwargs={'object_ptr': sstatus}), **self.authentication_headers)
        self.assertEquals(response.status_code, 204)

        # delete project
        response = self.client.delete(reverse(
            'api_projects', kwargs={'object_ptr': project_id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 204)
