# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Project Management: test suites
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, Perspective, ModuleSetting, Object
from treeio.projects.models import Project, Milestone, Task, TaskStatus, TaskTimeSlot
from treeio.identities.models import Contact, ContactType
from datetime import datetime


class ProjectsModelsTest(TestCase):

    " Documents models tests"

    def test_model_project(self):
        "Test project"
        obj = Project(name='test')
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_task(self):
        "Test task"
        project = Project(name='test')
        project.save()

        status = TaskStatus(name='test')
        status.save()

        obj = Task(name='test', project=project, status=status, priority=3)
        obj.save()
        self.assertEquals(project, obj.project)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_task_status(self):
        "Test task status"
        obj = TaskStatus(name='test')
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()


class ProjectsViewsTest(TestCase):

    "Projects functional tests for views"

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

            self.project = Project(
                name='test', manager=self.contact, client=self.contact)
            self.project.set_default_user()
            self.project.save()

            self.status = TaskStatus(name='test')
            self.status.set_default_user()
            self.status.save()

            self.milestone = Milestone(
                name='test', project=self.project, status=self.status)
            self.milestone.set_default_user()
            self.milestone.save()

            self.task = Task(
                name='test', project=self.project, status=self.status, priority=3)
            self.task.set_default_user()
            self.task.save()

            self.time_slot = TaskTimeSlot(
                task=self.task, details='test', time_from=datetime.now(), user=self.user)
            self.time_slot.set_default_user()
            self.time_slot.save()

            self.parent = Project(name='test')
            self.parent.set_default_user()
            self.parent.save()

            self.parent_task = Task(
                name='test', project=self.project, status=self.status, priority=3)
            self.parent_task.set_default_user()
            self.parent_task.save()

            self.client = Client()

            self.prepared = True

    ######################################
    # Testing views when user is logged in
    ######################################
    def test_index_login(self):
        "Test index page with login at /projects/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('projects'))
        self.assertEquals(response.status_code, 200)

    # Projects
    def test_project_add(self):
        "Test index page with login at /projects/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('project_add'))
        self.assertEquals(response.status_code, 200)

    def test_project_add_typed(self):
        "Test index page with login at /projects/add/<project_id>/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_project_add_typed', args=[self.parent.id]))
        self.assertEquals(response.status_code, 200)

    def test_project_view_login(self):
        "Test index page with login at /projects/view/<project_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_project_view', args=[self.project.id]))
        self.assertEquals(response.status_code, 200)

    def test_project_edit_login(self):
        "Test index page with login at /projects/edit//<project_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_project_edit', args=[self.project.id]))
        self.assertEquals(response.status_code, 200)

    def test_project_delete_login(self):
        "Test index page with login at /projects/delete//<project_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_project_delete', args=[self.project.id]))
        self.assertEquals(response.status_code, 200)

    # Milestones
    def test_milestone_add(self):
        "Test index page with login at /projects/milestone/add"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('projects_milestone_add'))
        self.assertEquals(response.status_code, 200)

    def test_milestone_add_typed(self):
        "Test index page with login at /projects/milestone/add/<project_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_milestone_add_typed', args=[self.parent.id]))
        self.assertEquals(response.status_code, 200)

    def test_milestone_view_login(self):
        "Test index page with login at /projects/milestone/view/<milestone_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_milestone_view', args=[self.milestone.id]))
        self.assertEquals(response.status_code, 200)

    def test_milestone_edit_login(self):
        "Test index page with login at /projects/milestone/edit/<milestone_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_milestone_edit', args=[self.milestone.id]))
        self.assertEquals(response.status_code, 200)

    def test_milestone_delete_login(self):
        "Test index page with login at /projects/milestone/delete/<milestone_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_milestone_delete', args=[self.milestone.id]))
        self.assertEquals(response.status_code, 200)

    # Tasks
    def test_task_add(self):
        "Test index page with login at /projects/task/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('projects_task_add'))
        self.assertEquals(response.status_code, 200)

    def test_task_add_typed(self):
        "Test index page with login at /projects/task/add/<project_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_task_add_typed', args=[self.project.id]))
        self.assertEquals(response.status_code, 200)

    def test_task_add_to_milestone(self):
        "Test index page with login at /projects/task/add/<milestone_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_task_add_to_milestone', args=[self.milestone.id]))
        self.assertEquals(response.status_code, 200)

    def test_task_add_subtask(self):
        "Test index page with login at /projects/task/add/<task_id>/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_task_add_subtask', args=[self.parent_task.id]))
        self.assertEquals(response.status_code, 200)

    def test_task_set_status(self):
        "Test index page with login at /projects/task/add/<task_id>/status/<status_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_task_set_status', args=[self.task.id, self.status.id]))
        self.assertEquals(response.status_code, 200)

    def test_task_view_login(self):
        "Test index page with login at /projects/task/view/<task_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_task_view', args=[self.task.id]))
        self.assertEquals(response.status_code, 200)

    def test_task_edit_login(self):
        "Test index page with login at /projects/task/edit/<task_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_task_edit', args=[self.task.id]))
        self.assertEquals(response.status_code, 200)

    def test_task_delete_login(self):
        "Test index page with login at /projects/task/delete/<task_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_task_delete', args=[self.task.id]))
        self.assertEquals(response.status_code, 200)

    # Task Time Slots
    def test_time_slot_add(self):
        "Test index page with login at /projects/task/view/time/<task_id>add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_task_time_slot_add', args=[self.task.id]))
        self.assertEquals(response.status_code, 200)

    def test_time_slot_view_login(self):
        "Test index page with login at /projects/task/view/time/<time_slot_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_task_view', args=[self.task.id]))
        self.assertEquals(response.status_code, 200)

    def test_time_slot_edit_login(self):
        "Test index page with login at /projects/task/edit/time/<time_slot_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_task_edit', args=[self.task.id]))
        self.assertEquals(response.status_code, 200)

    def test_time_slot_delete_login(self):
        "Test index page with login at /projects/task/delete/time/<time_slot_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_task_delete', args=[self.task.id]))
        self.assertEquals(response.status_code, 200)

    # Task Statuses
    def test_task_status_add(self):
        "Test index page with login at /projects/task/status/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('projects_task_status_add'))
        self.assertEquals(response.status_code, 200)

    def test_task_status_view_login(self):
        "Test index page with login at /projects/task/status/view/<status_id>/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_index_by_status', args=[self.status.id]))
        self.assertEquals(response.status_code, 200)

    def test_task_status_edit_login(self):
        "Test index page with login at /projects/task/status/edit/<status_id>/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_task_status_edit', args=[self.status.id]))
        self.assertEquals(response.status_code, 200)

    def test_task_status_delete_login(self):
        "Test index page with login at /projects/task/status/delete/<status_id>/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('projects_task_status_delete', args=[self.status.id]))
        self.assertEquals(response.status_code, 200)

    # Settings

    def test_project_settings_view(self):
        "Test index page with login at /projects/settings/view/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('projects_settings_view'))
        self.assertEquals(response.status_code, 200)

    def test_project_settings_edit(self):
        "Test index page with login at /projects/settings/edit/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('projects_settings_edit'))
        self.assertEquals(response.status_code, 200)

    ######################################
    # Testing views when user is not logged in
    ######################################
    def test_index(self):
        "Test index page at /projects/"
        response = self.client.get('/projects/')
        # Redirects as unauthenticated
        self.assertRedirects(response, reverse('user_login'))

    # Projects
    def test_project_add_out(self):
        "Testing /projects/add/"
        response = self.client.get(reverse('project_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_project_add_typed_out(self):
        "Testing /projects/add/<project_id>/"
        response = self.client.get(
            reverse('projects_project_add_typed', args=[self.parent.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_project_view_out(self):
        "Testing /projects/view/<project_id>"
        response = self.client.get(
            reverse('projects_project_view', args=[self.project.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_project_edit_out(self):
        "Testing /projects/edit//<project_id>"
        response = self.client.get(
            reverse('projects_project_edit', args=[self.project.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_project_delete_out(self):
        "Testing /projects/delete//<project_id>"
        response = self.client.get(
            reverse('projects_project_delete', args=[self.project.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Milestones
    def test_milestone_add_out(self):
        "Testing /projects/milestone/add"
        response = self.client.get(reverse('projects_milestone_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_milestone_add_typed_out(self):
        "Testing /projects/milestone/add/<project_id>"
        response = self.client.get(
            reverse('projects_milestone_add_typed', args=[self.parent.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_milestone_view_out(self):
        "Testing /projects/milestone/view/<milestone_id>"
        response = self.client.get(
            reverse('projects_milestone_view', args=[self.milestone.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_milestone_edit_out(self):
        "Testing /projects/milestone/edit/<milestone_id>"
        response = self.client.get(
            reverse('projects_milestone_edit', args=[self.milestone.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_milestone_delete_out(self):
        "Testing /projects/milestone/delete/<milestone_id>"
        response = self.client.get(
            reverse('projects_milestone_delete', args=[self.milestone.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Tasks
    def test_task_add_out(self):
        "Testing /projects/task/add/"
        response = self.client.get(reverse('projects_task_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_task_add_typed_out(self):
        "Testing /projects/task/add/<project_id>"
        response = self.client.get(
            reverse('projects_task_add_typed', args=[self.project.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_task_add_to_milestone_out(self):
        "Testing /projects/task/add/<milestone_id>"
        response = self.client.get(
            reverse('projects_task_add_to_milestone', args=[self.milestone.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_task_add_subtask_out(self):
        "Testing /projects/task/add/<task_id>/"
        response = self.client.get(
            reverse('projects_task_add_subtask', args=[self.parent_task.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_task_set_status_out(self):
        "Testing /projects/task/add/<task_id>/status/<status_id>"
        response = self.client.get(
            reverse('projects_task_set_status', args=[self.task.id, self.status.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_task_view_out(self):
        "Testing /projects/task/view/<task_id>"
        response = self.client.get(
            reverse('projects_task_view', args=[self.task.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_task_edit_out(self):
        "Testing /projects/task/edit/<task_id>"
        response = self.client.get(
            reverse('projects_task_edit', args=[self.task.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_task_delete_out(self):
        "Testing /projects/task/delete/<task_id>"
        response = self.client.get(
            reverse('projects_task_delete', args=[self.task.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Task Time Slots
    def test_time_slot_add_out(self):
        "Testing /projects/task/view/time/<task_id>add/"
        response = self.client.get(
            reverse('projects_task_time_slot_add', args=[self.task.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_time_slot_view_out(self):
        "Testing /projects/task/view/time/<time_slot_id>"
        response = self.client.get(
            reverse('projects_task_view', args=[self.task.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_time_slot_edit_out(self):
        "Testing /projects/task/edit/time/<time_slot_id>"
        response = self.client.get(
            reverse('projects_task_edit', args=[self.task.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_time_slot_delete_out(self):
        "Testing /projects/task/delete/time/<time_slot_id>"
        response = self.client.get(
            reverse('projects_task_delete', args=[self.task.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Task Statuses

    def test_task_status_add_out(self):
        "Testing /projects/task/status/add/"
        response = self.client.get(reverse('projects_task_status_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_task_status_view_out(self):
        "Testing /projects/task/status/view/<status_id>/"
        response = self.client.get(
            reverse('projects_index_by_status', args=[self.status.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_task_status_edit_out(self):
        "Testing /projects/task/status/edit/<status_id>/"
        response = self.client.get(
            reverse('projects_task_status_edit', args=[self.status.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_task_status_delete_out(self):
        "Testing /projects/task/status/delete/<status_id>/"
        response = self.client.get(
            reverse('projects_task_status_delete', args=[self.status.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Settings

    def test_project_settings_view_out(self):
        "Testing /projects/settings/view/"
        response = self.client.get(reverse('projects_settings_view'))
        self.assertRedirects(response, reverse('user_login'))

    def test_project_settings_edit_out(self):
        "Testing /projects/settings/edit/"
        response = self.client.get(reverse('projects_settings_edit'))
        self.assertRedirects(response, reverse('user_login'))
