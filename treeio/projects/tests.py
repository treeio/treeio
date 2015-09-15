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
from datetime import datetime, timedelta
from freezegun import freeze_time


class ProjectsModelsTest(TestCase):
    """ Documents models tests"""
    def setUp(self):
        self.project = Project(name='test')
        self.project.save()

        self.taskstatus = TaskStatus(name='test')
        self.taskstatus.save()

        self.task = Task(name='test', project=self.project, status=self.taskstatus)
        self.task.save()

    def test_task_priority_human(self):
        """Default priority should be 3, text representation should be 'Normal'
        """
        self.assertEqual(self.task.priority, 3)
        self.assertEqual(self.task.priority_human(), 'Normal')

    def test_get_estimated_time_default(self):
        """Default estimated time is None, string representation is empty string """
        self.assertIsNone(self.task.estimated_time)
        self.assertEqual(self.task.get_estimated_time(), '')

    def test_get_estimated_time_one_min(self):
        self.task.estimated_time = 1
        self.assertEqual(self.task.get_estimated_time(), ' 1 minutes')

    def test_get_estimated_time_zero_min(self):
        self.task.estimated_time = 0
        self.assertEqual(self.task.get_estimated_time(), 'Less than 1 minute')

    def test_get_estimated_time_60_min(self):
        self.task.estimated_time = 60
        self.assertEqual(self.task.get_estimated_time(), ' 1 hours ')

    def test_get_estimated_time_61_min(self):
        self.task.estimated_time = 61
        self.assertEqual(self.task.get_estimated_time(), ' 1 hours  1 minutes')

    def test_model_task_get_absolute_url(self):
        self.task.get_absolute_url()

    # def test_save TODO: save is overridden and has some extra logic

    def test_get_absolute_url(self):
        """Test if get_absolute_url works without raising any exception"""
        self.project.get_absolute_url()

    def add_time_slot(self, total_time):
        duser, created = DjangoUser.objects.get_or_create(username='testuser')
        time_from = datetime(year=2015, month=8, day=3)
        time_to = time_from + total_time
        timeslot = TaskTimeSlot(task=self.task, user=duser.profile, time_from=time_from, time_to=time_to)
        timeslot.save()

    def test_get_total_time_default(self):
        self.assertEqual(self.task.get_total_time(), timedelta())

    def test_get_total_time_with_timeslots1(self):
        total_time = timedelta(hours=3)
        self.add_time_slot(total_time)
        self.assertEqual(self.task.get_total_time(), total_time)

    def test_get_total_time_tuple_default(self):
        self.assertIsNone(self.task.get_total_time_tuple())

    def test_get_total_time_tuple(self):
        total_time = timedelta(hours=3)
        self.add_time_slot(total_time)
        h, m, s = self.task.get_total_time_tuple()
        self.assertEqual((h, m, s), (3, 0, 0))

    def test_get_total_time_string_default(self):
        self.assertEqual(self.task.get_total_time_string(), '0 minutes')

    def test_get_total_time_string_one_min(self):
        total_time = timedelta(minutes=1)
        self.add_time_slot(total_time)
        self.assertEqual(self.task.get_total_time_string(), ' 1 minutes')

    def test_get_total_time_string_zero_min(self):
        total_time = timedelta(minutes=0)
        self.add_time_slot(total_time)
        self.assertEqual(self.task.get_total_time_string(), '0 minutes')

    def test_get_total_time_string_30_secs(self):
        total_time = timedelta(seconds=30)
        self.add_time_slot(total_time)
        self.assertEqual(self.task.get_total_time_string(), 'Less than 1 minute')

    def test_get_total_time_string_60_min(self):
        total_time = timedelta(minutes=60)
        self.add_time_slot(total_time)
        self.assertEqual(self.task.get_total_time_string(), ' 1 hours ')

    def test_get_total_time_string_61_min(self):
        total_time = timedelta(minutes=61)
        self.add_time_slot(total_time)
        self.assertEqual(self.task.get_total_time_string(), ' 1 hours  1 minutes')

    def test_is_being_done_by(self):
        duser, created = DjangoUser.objects.get_or_create(username='testuser')
        self.assertFalse(self.task.is_being_done_by(duser))

        time_from = datetime(year=2015, month=8, day=3)
        timeslot = TaskTimeSlot(task=self.task, user=duser.profile, time_from=time_from)
        timeslot.save()
        self.task.save()

        self.assertTrue(self.task.is_being_done_by(duser))

    def test_model_task_status(self):
        """Test task status"""
        obj = TaskStatus(name='test')
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.get_absolute_url()
        obj.delete()

    def test_model_milestone(self):
        tstatus = TaskStatus(name='test')
        tstatus.save()
        mstone = Milestone(project=self.project, status=tstatus)
        mstone.save()
        mstone.get_absolute_url()


class TestModelTaskTimeSlot(TestCase):
    def setUp(self):
        self.project = Project(name='test')
        self.project.save()

        self.taskstatus = TaskStatus(name='test')
        self.taskstatus.save()

        self.task = Task(name='test', project=self.project, status=self.taskstatus)
        self.task.save()

        duser, created = DjangoUser.objects.get_or_create(username='testuser')
        self.user = duser
        self.time_from = datetime(year=2015, month=8, day=3)
        self.total_time = timedelta(minutes=61)
        self.time_to = self.time_from + self.total_time
        self.timeslot = TaskTimeSlot(task=self.task, user=duser.profile, time_from=self.time_from, time_to=self.time_to)
        self.timeslot.save()

    def test_get_absolute_url(self):
        self.timeslot.get_absolute_url()

    def test_get_time_secs(self):
        with freeze_time(datetime(year=2015, month=8, day=4)):
            self.assertEqual(self.timeslot.get_time_secs(), 86400)

    def test_get_time(self):
        """A time slot without a time from or time to will return a delta of 0"""
        timeslot2 = TaskTimeSlot(task=self.task, user=self.user.profile, time_from=self.time_from)
        timeslot3 = TaskTimeSlot(task=self.task, user=self.user.profile, time_to=self.time_to)
        self.assertEqual(timeslot2.get_time(), timedelta(0))
        self.assertEqual(timeslot3.get_time(), timedelta(0))
        self.assertEqual(self.timeslot.get_time(), self.total_time)

    def test_get_time_tuple(self):
        h, m, s = self.timeslot.get_time_tuple()
        self.assertEqual((h, m, s), (1, 1, 0))
        timeslot2 = TaskTimeSlot(task=self.task, user=self.user.profile, time_to=self.time_to)
        self.assertIsNone(timeslot2.get_time_tuple())

    def test_get_time_string(self):
        self.assertEqual(self.timeslot.get_time_string(), ' 1 hours  1 minutes')

        total_time = timedelta(minutes=1)
        self.timeslot.time_to = self.time_from + total_time
        self.assertEqual(self.timeslot.get_time_string(), ' 1 minutes')

        # if it has a timedelta of zero it will use now-time_from
        total_time = timedelta(minutes=0)
        self.timeslot.time_to = self.time_from + total_time
        with freeze_time(datetime(year=2015, month=8, day=4)):
            self.assertEqual(self.timeslot.get_time_string(), '24 hours ')

        total_time = timedelta(seconds=30)
        self.timeslot.time_to = self.time_from + total_time
        self.assertEqual(self.timeslot.get_time_string(), 'Less than 1 minute')

        total_time = timedelta(minutes=60)
        self.timeslot.time_to = self.time_from + total_time
        self.assertEqual(self.timeslot.get_time_string(), ' 1 hours ')

        self.timeslot.time_from = None
        self.assertEqual(self.timeslot.get_time_string(), '')

        self.timeslot.time_from = self.time_from
        self.timeslot.time_to = None
        with freeze_time(datetime(year=2015, month=8, day=4)):
            self.assertEqual(self.timeslot.get_time_string(), '24 hours ')

    def test_is_open(self):
        # a time slot with both time_from and time_to means it is closed
        self.assertFalse(self.timeslot.is_open())
        self.timeslot.time_to = None
        self.assertTrue(self.timeslot.is_open())


class ProjectsViewsNotLoggedIn(TestCase):
    """Test views Behaviour when user is not logged in
    Basically assert that all views are protected by login
    """

    def assert_protected(self, name, args=None):
        response = self.client.get(reverse(name, args=args))
        self.assertRedirects(response, reverse('user_login'))

    def test_index(self):
        self.assert_protected('projects')

    def test_index_owned(self):
        self.assert_protected('projects_index_owned')

    def test_index_assigned(self):
        self.assert_protected('projects_index_assigned')

    def test_index_by_status(self):
        self.assert_protected('projects_index_by_status', (1,))

    def test_index_in_progress(self):
        self.assert_protected('projects_tasks_in_progress')

    def test_project_add(self):
        self.assert_protected('project_add')

    def test_project_add_typed(self):
        self.assert_protected('projects_project_add_typed', (1,))

    def test_project_view(self):
        self.assert_protected('projects_project_view', (1, ))

    def test_project_edit(self):
        self.assert_protected('projects_project_edit', (1, ))

    def test_project_delete(self):
        self.assert_protected('projects_project_delete', (1, ))

    def test_milestone_add(self):
        self.assert_protected('projects_milestone_add')

    def test_milestone_add_typed(self):
        self.assert_protected('projects_milestone_add_typed', (1, ))

    def test_milestone_view(self):
        self.assert_protected('projects_milestone_view', (1, ))

    def test_milestone_edit(self):
        self.assert_protected('projects_milestone_edit', (1, ))

    def test_milestone_delete(self):
        self.assert_protected('projects_milestone_delete', (1, ))

    def test_milestone_set_status(self):
        self.assert_protected('projects_milestone_set_status', (1, 1))

    def test_task_add(self):
        self.assert_protected('projects_task_add')

    def test_task_add_typed(self):
        self.assert_protected('projects_task_add_typed', (1,))

    def test_task_add_to_milestone(self):
        self.assert_protected('projects_task_add_to_milestone', (1,))

    def test_task_add_subtask(self):
        self.assert_protected('projects_task_add_subtask', (1,))

    def test_task_view(self):
        self.assert_protected('projects_task_view', (1,))

    def test_task_edit(self):
        self.assert_protected('projects_task_edit', (1,))

    def test_task_delete(self):
        self.assert_protected('projects_task_delete', (1,))

    def test_task_set_status(self):
        self.assert_protected('projects_task_set_status', (1, 1))

    def test_task_time_slot_start(self):
        self.assert_protected('projects_task_time_slot_start', (1,))

    def test_task_time_slot_stop(self):
        self.assert_protected('projects_task_time_slot_stop', (1,))

    def test_task_time_slot_add(self):
        self.assert_protected('projects_task_time_slot_add', (1,))

    def test_task_time_slot_view(self):
        self.assert_protected('projects_task_time_slot_view', (1,))

    def test_task_time_slot_edit(self):
        self.assert_protected('projects_task_time_slot_edit', (1,))

    def test_task_time_slot_delete(self):
        self.assert_protected('projects_task_time_slot_delete', (1,))

    def test_task_status_add(self):
        self.assert_protected('projects_task_status_add')

    def test_task_status_edit(self):
        self.assert_protected('projects_task_status_edit', (1,))

    def test_task_status_delete(self):
        self.assert_protected('projects_task_status_delete', (1,))

    def test_settings_view(self):
        self.assert_protected('projects_settings_view')

    def test_settings_edit(self):
        self.assert_protected('projects_settings_edit')

    def test_ajax_task_lookup(self):
        self.assert_protected('projects_ajax_task_lookup')

    def test_gantt_view(self):
        self.assert_protected('projects_gantt_view', (1,))


class ProjectsViewsTest(TestCase):
    """Projects functional tests for views"""

    username = "test"
    password = "password"

    def setUp(self):
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

        self.client.login(username=self.username, password=self.password)

    def test_index(self):
        """Test index page with login at /projects/"""
        response = self.client.get(reverse('projects'))
        self.assertEquals(response.status_code, 200)

    def test_index_owned(self):
        """Test index page with login at /projects/"""
        response = self.client.get(reverse('projects_index_owned'))
        self.assertEquals(response.status_code, 200)

    # Projects
    def test_project_add(self):
        """Test index page with login at /projects/add/"""
        response = self.client.get(reverse('project_add'))
        self.assertEquals(response.status_code, 200)

    def test_project_add_typed(self):
        """Test index page with login at /projects/add/<project_id>/"""
        response = self.client.get(reverse('projects_project_add_typed', args=[self.parent.id]))
        self.assertEquals(response.status_code, 200)

    def test_project_view_login(self):
        """Test index page with login at /projects/view/<project_id>"""
        response = self.client.get(reverse('projects_project_view', args=[self.project.id]))
        self.assertEquals(response.status_code, 200)

    def test_project_edit_login(self):
        """Test index page with login at /projects/edit//<project_id>"""
        response = self.client.get(reverse('projects_project_edit', args=[self.project.id]))
        self.assertEquals(response.status_code, 200)

    def test_project_delete_login(self):
        """Test index page with login at /projects/delete//<project_id>"""
        response = self.client.get(reverse('projects_project_delete', args=[self.project.id]))
        self.assertEquals(response.status_code, 200)

    # Milestones
    def test_milestone_add(self):
        """Test index page with login at /projects/milestone/add"""
        response = self.client.get(reverse('projects_milestone_add'))
        self.assertEquals(response.status_code, 200)

    def test_milestone_add_typed(self):
        """Test index page with login at /projects/milestone/add/<project_id>"""
        response = self.client.get(reverse('projects_milestone_add_typed', args=[self.parent.id]))
        self.assertEquals(response.status_code, 200)

    def test_milestone_view_login(self):
        """Test index page with login at /projects/milestone/view/<milestone_id>"""
        response = self.client.get(reverse('projects_milestone_view', args=[self.milestone.id]))
        self.assertEquals(response.status_code, 200)

    def test_milestone_edit_login(self):
        """Test index page with login at /projects/milestone/edit/<milestone_id>"""
        response = self.client.get(reverse('projects_milestone_edit', args=[self.milestone.id]))
        self.assertEquals(response.status_code, 200)

    def test_milestone_delete_login(self):
        """Test index page with login at /projects/milestone/delete/<milestone_id>"""
        response = self.client.get(reverse('projects_milestone_delete', args=[self.milestone.id]))
        self.assertEquals(response.status_code, 200)

    # Tasks
    def test_task_add(self):
        """Test index page with login at /projects/task/add/"""
        response = self.client.get(reverse('projects_task_add'))
        self.assertEquals(response.status_code, 200)

    def test_task_add_typed(self):
        """Test index page with login at /projects/task/add/<project_id>"""
        response = self.client.get(reverse('projects_task_add_typed', args=[self.project.id]))
        self.assertEquals(response.status_code, 200)

    def test_task_add_to_milestone(self):
        """Test index page with login at /projects/task/add/<milestone_id>"""
        response = self.client.get(reverse('projects_task_add_to_milestone', args=[self.milestone.id]))
        self.assertEquals(response.status_code, 200)

    def test_task_add_subtask(self):
        """Test index page with login at /projects/task/add/<task_id>/"""
        response = self.client.get(reverse('projects_task_add_subtask', args=[self.parent_task.id]))
        self.assertEquals(response.status_code, 200)

    def test_task_set_status(self):
        """Test index page with login at /projects/task/add/<task_id>/status/<status_id>"""
        response = self.client.get(reverse('projects_task_set_status', args=[self.task.id, self.status.id]))
        self.assertEquals(response.status_code, 200)

    def test_task_view_login(self):
        """Test index page with login at /projects/task/view/<task_id>"""
        response = self.client.get(reverse('projects_task_view', args=[self.task.id]))
        self.assertEquals(response.status_code, 200)

    def test_task_edit_login(self):
        """Test index page with login at /projects/task/edit/<task_id>"""
        response = self.client.get(reverse('projects_task_edit', args=[self.task.id]))
        self.assertEquals(response.status_code, 200)

    def test_task_delete_login(self):
        """Test index page with login at /projects/task/delete/<task_id>"""
        response = self.client.get(reverse('projects_task_delete', args=[self.task.id]))
        self.assertEquals(response.status_code, 200)

    # Task Time Slots
    def test_time_slot_add(self):
        """Test index page with login at /projects/task/view/time/<task_id>add/"""
        response = self.client.get(reverse('projects_task_time_slot_add', args=[self.task.id]))
        self.assertEquals(response.status_code, 200)

    def test_time_slot_view_login(self):
        """Test index page with login at /projects/task/view/time/<time_slot_id>"""
        response = self.client.get(reverse('projects_task_view', args=[self.task.id]))
        self.assertEquals(response.status_code, 200)

    def test_time_slot_edit_login(self):
        """Test index page with login at /projects/task/edit/time/<time_slot_id>"""
        response = self.client.get(reverse('projects_task_edit', args=[self.task.id]))
        self.assertEquals(response.status_code, 200)

    def test_time_slot_delete_login(self):
        """Test index page with login at /projects/task/delete/time/<time_slot_id>"""
        response = self.client.get(reverse('projects_task_delete', args=[self.task.id]))
        self.assertEquals(response.status_code, 200)

    # Task Statuses
    def test_task_status_add(self):
        """Test index page with login at /projects/task/status/add/"""
        response = self.client.get(reverse('projects_task_status_add'))
        self.assertEquals(response.status_code, 200)

    def test_task_status_view_login(self):
        """Test index page with login at /projects/task/status/view/<status_id>/"""
        response = self.client.get(reverse('projects_index_by_status', args=[self.status.id]))
        self.assertEquals(response.status_code, 200)

    def test_task_status_edit_login(self):
        """Test index page with login at /projects/task/status/edit/<status_id>/"""
        response = self.client.get(reverse('projects_task_status_edit', args=[self.status.id]))
        self.assertEquals(response.status_code, 200)

    def test_task_status_delete_login(self):
        """Test index page with login at /projects/task/status/delete/<status_id>/"""
        response = self.client.get(reverse('projects_task_status_delete', args=[self.status.id]))
        self.assertEquals(response.status_code, 200)

    # Settings

    def test_project_settings_view(self):
        """Test index page with login at /projects/settings/view/"""
        response = self.client.get(reverse('projects_settings_view'))
        self.assertEquals(response.status_code, 200)

    def test_project_settings_edit(self):
        """Test index page with login at /projects/settings/edit/"""
        response = self.client.get(reverse('projects_settings_edit'))
        self.assertEquals(response.status_code, 200)
