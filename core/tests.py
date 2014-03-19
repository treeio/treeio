# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core: test suites
Middleware: test chat
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, ModuleSetting, Module, Object, Perspective


class CoreModelsTest(TestCase):

    "Core Model Tests"

    def test_model_perspective(self):
        "Test Perspective model"
        obj = Perspective(name='test')
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_module(self):
        "Test Module model"
        obj = Module(name='test', title='Test', url='/test/')
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_group(self):
        "Test Group model"
        obj = Group(name='test')
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_user(self):
        "Test User model"
        username = "test"
        password = "password"
        user = DjangoUser(username=username, password=password)
        user.set_password(password)
        user.save()
        self.assertEquals('test', user.username)
        self.assertNotEquals(user.id, None)
        group = Group(name='test')
        group.save()
        self.assertEquals('test', group.name)
        self.assertNotEquals(group.id, None)
        profile = User(user=user, default_group=group)
        profile.save()
        self.assertEquals(user, profile.user)
        self.assertNotEquals(profile.id, None)
        profile.delete()
        group.delete()


class CoreViewsTest(TestCase):

    "Core View tests"
    username = "test"
    password = "password"
    prepared = False

    def setUp(self):
        "Initial Setup"

        if not self.prepared:
            Object.objects.all().delete()

            # Create objects

            self.group, created = Group.objects.get_or_create(name='test')
            duser, created = DjangoUser.objects.get_or_create(
                username=self.username)
            duser.set_password(self.password)
            duser.save()
            self.user, created = User.objects.get_or_create(user=duser)
            self.user.save()

            self.perspective = Perspective(name='test')
            self.perspective.set_default_user()
            self.perspective.save()

            self.client = Client()

            self.prepared = True

    ######################################
    # Testing views when user is logged in
    ######################################
    def test_home_login(self):
        "Test home page with login at /"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    # Perspectives
    def test_index_perspectives_login(self):
        "Test page with login at /admin/perspectives/"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('core_admin_index_perspectives'))
        self.assertEquals(response.status_code, 200)

    def test_perspective_add(self):
        "Test index page with login at /admin/perspective/add"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('core_admin_perspective_add'))
        self.assertEquals(response.status_code, 200)

    def test_perspective_view(self):
        "Test index page with login at /admin/perspective/view/<perspective_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('core_admin_perspective_view', args=[self.perspective.id]))
        self.assertEquals(response.status_code, 200)

    def test_perspective_edit(self):
        "Test index page with login at /admin/perspective/edit/<perspective_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('core_admin_perspective_edit', args=[self.perspective.id]))
        self.assertEquals(response.status_code, 200)

    def test_perspective_delete(self):
        "Test index page with login at /admin/perspective/delete/<perspective_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('core_admin_perspective_delete', args=[self.perspective.id]))
        self.assertEquals(response.status_code, 200)

    # Modules
    def test_index_modules_login(self):
        "Test page with login at /admin/modules/"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('core_admin_index_modules'))
        self.assertEquals(response.status_code, 200)

    # Users
    def test_index_users_login(self):
        "Test page with login at /admin/users/"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('core_admin_index_users'))
        self.assertEquals(response.status_code, 200)

    def test_core_user_add(self):
        "Test page with login at /admin/user/add"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('core_admin_user_add'))
        self.assertEquals(response.status_code, 200)

    def test_core_user_invite(self):
        "Test page with login at /admin/user/invite"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('core_admin_user_invite'))
        self.assertEquals(response.status_code, 200)

    # Groups
    def test_index_groups_login(self):
        "Test page with login at /admin/groups/"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('core_admin_index_groups'))
        self.assertEquals(response.status_code, 200)

    def test_core_group_add(self):
        "Test page with login at /admin/group/add"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('core_admin_group_add'))
        self.assertEquals(response.status_code, 200)

    def test_core_group_view(self):
        "Test index page with login at /admin/group/view/<group_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('core_admin_group_view', args=[self.group.id]))
        self.assertEquals(response.status_code, 200)

    def test_core_group_edit(self):
        "Test index page with login at /admin/group/edit/<group_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('core_admin_group_edit', args=[self.group.id]))
        self.assertEquals(response.status_code, 200)

    def test_core_group_delete(self):
        "Test index page with login at /admin/group/delete/<group_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('core_admin_group_delete', args=[self.group.id]))
        self.assertEquals(response.status_code, 200)

    # Settings
    def test_core_settings_view(self):
        "Test index page with login at /admin/settings/view/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('core_settings_view'))
        self.assertEquals(response.status_code, 200)

    def test_core_settings_edit(self):
        "Test index page with login at /admin/settings/edit/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('core_settings_edit'))
        self.assertEquals(response.status_code, 200)

    ######################################
    # Testing views when user is not logged in
    ######################################
    def test_home(self):
        "Test home page at /"
        response = self.client.get('/')
        # Redirects as unauthenticated
        self.assertRedirects(response, reverse('user_login'))

    def test_index_perspectives_out(self):
        "Test page at /admin/perspectives/"
        response = self.client.get(reverse('core_admin_index_perspectives'))
        self.assertRedirects(response, reverse('user_login'))

    def test_perspective_add_out(self):
        "Test add perspective page at /admin/perspective/add"
        response = self.client.get(reverse('core_admin_perspective_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_perspective_view_out(self):
        "Test perspective view at /admin/perspective/view/<perspective_id>"
        response = self.client.get(
            reverse('core_admin_perspective_view', args=[self.perspective.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_perspective_edit_out(self):
        "Test perspective add at /admin/perspective/edit/<perspective_id>"
        response = self.client.get(
            reverse('core_admin_perspective_edit', args=[self.perspective.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_perspective_delete_out(self):
        "Test perspective delete at /admin/perspective/delete/<perspective_id>"
        response = self.client.get(
            reverse('core_admin_perspective_delete', args=[self.perspective.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Modules
    def test_index_modules_out(self):
        "Test index modules page at /admin/modules/"
        response = self.client.get(reverse('core_admin_index_modules'))
        self.assertRedirects(response, reverse('user_login'))

    # Users
    def test_index_users_out(self):
        "Test index users page at /admin/users/"
        response = self.client.get(reverse('core_admin_index_users'))
        self.assertRedirects(response, reverse('user_login'))

    def test_core_user_add_out(self):
        "Test user add at /admin/user/add"
        response = self.client.get(reverse('core_admin_user_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_core_user_invite_out(self):
        "Test user invite at /admin/user/invite"
        response = self.client.get(reverse('core_admin_user_invite'))
        self.assertRedirects(response, reverse('user_login'))

    # Groups
    def test_index_groups_out(self):
        "Test index groups at /admin/groups/"
        response = self.client.get(reverse('core_admin_index_groups'))
        self.assertRedirects(response, reverse('user_login'))

    def test_core_group_add_out(self):
        "Test group add at /admin/group/add"
        response = self.client.get(reverse('core_admin_group_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_core_group_view_out(self):
        "Test group view at /admin/group/view/<group_id>"
        response = self.client.get(
            reverse('core_admin_group_view', args=[self.group.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_core_group_edit_out(self):
        "Test group edit at /admin/group/edit/<group_id>"
        response = self.client.get(
            reverse('core_admin_group_edit', args=[self.group.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_core_group_delete_out(self):
        "Test group delete at /admin/group/delete/<group_id>"
        response = self.client.get(
            reverse('core_admin_group_delete', args=[self.group.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Settings
    def test_core_settings_view_out(self):
        "Test isettings view at /admin/settings/view/"
        response = self.client.get(reverse('core_settings_view'))
        self.assertRedirects(response, reverse('user_login'))

    def test_core_settings_edit_out(self):
        "Test settings edit at /admin/settings/edit/"
        response = self.client.get(reverse('core_settings_edit'))
        self.assertRedirects(response, reverse('user_login'))


class MiddlewareChatTest(TestCase):

    "Midleware chat tests"
    username = "test"
    password = "password"
    prepared = False

    def setUp(self):
        "Initial Setup"

        if not self.prepared:
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

            self.client = Client()

            self.prepared = True

    def test_chat_get_new_messages(self):
        "Test get_new_messages"
        response = self.client.post(
            '/chat', {'json': '{"cmd":"Get", "location":"#"}'})
        self.assertEqual(response.status_code, 200)

    def test_chat_connect(self):
        "Test connect"
        response = self.client.post(
            '/chat', {'json': '{"cmd":"Connect", "location":"#"}'})
        self.assertEqual(response.status_code, 200)

    def test_chat_disconnect(self):
        "Test disconnect"
        response = self.client.post(
            '/chat', {'json': '{"cmd":"Disconnect", "location":"#"}'})
        self.assertEqual(response.status_code, 200)

    def test_chat_add_new_message(self):
        "Test add_new_message"
        response = self.client.post(
            '/chat', {'json': '{"cmd":"Message","data":{"id":"test_b5e6d0470a5f4656c3bc77f879c3dbbc","text":"test message"},"location":"#"}'})
        self.assertEqual(response.status_code, 200)

    def test_chat_exit_from_conference(self):
        "Test exit_from_conference"
        response = self.client.post(
            '/chat', {'json': '{"cmd":"Exit","data":{"id":"test_b5e6d0470a5f4656c3bc77f879c3dbbc"},"location":"#"}'})
        self.assertEqual(response.status_code, 200)

    def test_chat_add_users_in_conference(self):
        "Test add_users_in_conference"
        response = self.client.post(
            '/chat', {'json': '{"cmd":"Add","data":{"id":"guest_006f721c4a59a44d969b9f73fb6360a5","users":["test"]},"location":"#"}'})
        self.assertEqual(response.status_code, 200)

    def test_chat_create_conference(self):
        "Test create_conference"
        response = self.client.post(
            '/chat', {'json': '{"cmd":"Create","data":{"title":["Admin"],"users":["admin"]},"location":"#"}'})
        self.assertEqual(response.status_code, 200)
