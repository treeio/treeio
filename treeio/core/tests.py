# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core: test suites
Middleware: test chat
"""
import datetime

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio import identities
from treeio.core.models import User, Group, ModuleSetting, Module, Object, Perspective, AccessEntity


class CoreModelsTest(TestCase):
    """Core Model Tests"""
    fixtures = ['myinitial_data.json']

    def test_model_AccessEntity(self):
        obj = AccessEntity()
        obj.save()
        self.assertIsNotNone(obj.id)
        obj = AccessEntity.objects.get(id=obj.id)
        self.assertTrue(obj.last_updated - datetime.datetime.now() < datetime.timedelta(seconds=1))
        self.assertIsNone(obj.get_entity())
        self.assertFalse(obj.is_user())
        self.assertEqual(obj.__unicode__(), str(obj.id))
        self.assertEqual(obj.get_absolute_url(), '')

    def test_model_Group_basic(self):
        """Test Group model"""
        name = 'testgroup'
        obj = Group(name=name)
        obj.save()
        self.assertIsNotNone(obj.id)
        obj = Group.objects.get(id=obj.id)
        self.assertEqual(obj.name, name)
        self.assertIsNone(obj.parent)
        self.assertIsNone(obj.details)
        self.assertQuerysetEqual(obj.child_set.all(), [])
        self.assertEqual(obj.get_absolute_url(), '/contacts/group/view/{}'.format(obj.id))
        self.assertEqual(obj.get_root(), obj)
        self.assertEqual(obj.get_tree_path(), [obj])
        self.assertIsNone(obj.get_contact())
        self.assertFalse(obj.has_contact())
        self.assertEqual(obj.get_fullname(), name)
        self.assertEqual(obj.get_perspective(), Perspective.objects.all()[0])
        # todo obj.set_perspective()

    def test_model_User_profile(self):
        """Test User model"""
        username = "testusername"
        password = "password"
        user = DjangoUser(username=username)
        user.set_password(password)
        user.save()
        self.assertEquals(user.username, username)
        self.assertIsNotNone(user.id)
        profile = user.profile
        self.assertEquals(profile.name, username)
        self.assertEquals(profile.default_group, Group.objects.all()[0])
        self.assertQuerysetEqual(profile.other_groups.all(), [])
        self.assertFalse(profile.disabled)
        self.assertTrue(profile.last_access - datetime.datetime.now() < datetime.timedelta(seconds=1))
        self.assertEqual(profile.get_absolute_url(), '/contacts/user/view/{}'.format(profile.id))
        oldpsw = profile.user.password
        self.assertNotEqual(profile.generate_new_password(), oldpsw)
        self.assertQuerysetEqual(profile.get_groups(), map(repr, [profile.default_group]))
        self.assertTrue(profile.is_admin())
        self.assertEqual(profile.get_username(), username)
        self.assertEqual(profile.get_perspective(), Perspective.objects.get(name='Default'))
        self.assertEqual(profile.get_contact(), identities.models.Contact.objects.get(related_user=profile))
        self.assertTrue(profile.has_contact())

    def test_model_User_profile_change_default_group(self):
        username = "testusername"
        user = DjangoUser(username=username)
        user.save()
        profile = user.profile
        group = Group(name='testgroupname')
        group.save()
        profile.default_group = group
        profile.save()
        profile = User.objects.get(user=user)
        self.assertEquals(profile.default_group, group)

    def test_model_Module_basic(self):
        """Test Module model with minimum parameters"""
        name = 'test module'
        title = 'Test title'
        url = '/test_url/'
        obj = Module(name=name, title=title, url=url)
        obj.save()
        self.assertIsNotNone(obj.id)
        obj = Module.objects.get(id=obj.id)
        self.assertEquals(obj.name, name)
        self.assertEquals(obj.title, title)
        self.assertEquals(obj.url, url)
        self.assertEquals(obj.details, '')
        self.assertTrue(obj.display)
        self.assertTrue(obj.system)
        self.assertEqual(obj.get_absolute_url(), '/admin/module/view/{}'.format(obj.id))

    def test_model_Perspective_basic(self):
        """Test Perspective model with minimum parameters"""
        name = 'test'
        obj = Perspective(name=name)
        obj.save()
        self.assertIsNotNone(obj.id)
        obj = Perspective.objects.get(id=obj.id)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.details, '')
        self.assertQuerysetEqual(obj.modules.all(), [])
        # default is to have all modules available
        self.assertQuerysetEqual(obj.get_modules(), map(repr, Module.objects.all()))
        self.assertEqual(obj.get_absolute_url(), '/admin/perspective/view/{}'.format(obj.id))

    def test_model_Perspective_full(self):
        """Test Perspective model with all parameters"""
        name = 'test'
        details = 'perspective details'
        obj = Perspective(name='test', details=details)
        obj.save()
        self.assertIsNotNone(obj.id)
        obj = Perspective.objects.get(id=obj.id)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.details, details)
        module = Module.objects.all()[0]
        obj.modules.add(module)
        self.assertQuerysetEqual(obj.modules.all(), map(repr, [module]))
        self.assertQuerysetEqual(obj.get_modules(), map(repr, [module]))
        self.assertEqual(obj.get_absolute_url(), '/admin/perspective/view/{}'.format(obj.id))


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
            # self.user, created = User.objects.get_or_create(user=duser)
            # self.user.save()

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

    def login(self):
        self.assertEquals(self.client.login(username=self.username, password=self.password), True)

    def test_core_user_add(self):
        "Test page with login at /admin/user/add"
        name = 'newuser'
        password = 'newuserpsw'
        data = {'name': name, 'password': password, 'password_again': password}
        self.login()
        response = self.client.post(path=reverse('core_admin_user_add'), data=data)
        self.assertEquals(response.status_code, 302)
        profile = User.objects.get(name=name)
        profiles = User.objects.all()
        self.assertEquals(profile.name, name)
        self.assertRedirects(response, reverse('core_admin_user_view', args=[profile.id]))
        self.assertEquals(self.client.login(username=name, password=password), True)
        self.client.logout()
        response = self.client.post('/accounts/login', {'username': name, 'password': password})
        self.assertRedirects(response, '/')

    def test_core_user_delete(self):
        "Test page with login at /admin/user/delete"
        name = 'newuser'
        password = 'newuserpsw'
        user, created = DjangoUser.objects.get_or_create(username=name)
        if created:
            user.set_password(password)
            user.save()
        self.login()
        response = self.client.post(path=reverse('core_admin_user_delete', args=[user.profile.id]),
                                    data={'delete': ''})
        self.assertRedirects(response, reverse('core_admin_index_users'))
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(name=name)
        with self.assertRaises(DjangoUser.DoesNotExist):
            DjangoUser.objects.get(username=name)

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
                    self.profile = self.user.profile
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
            '/chat', {
                'json': '{"cmd":"Message","data":{"id":"test_b5e6d0470a5f4656c3bc77f879c3dbbc","text":"test message"},"location":"#"}'})
        self.assertEqual(response.status_code, 200)

    def test_chat_exit_from_conference(self):
        "Test exit_from_conference"
        response = self.client.post(
            '/chat', {'json': '{"cmd":"Exit","data":{"id":"test_b5e6d0470a5f4656c3bc77f879c3dbbc"},"location":"#"}'})
        self.assertEqual(response.status_code, 200)

    def test_chat_add_users_in_conference(self):
        "Test add_users_in_conference"
        response = self.client.post(
            '/chat', {
                'json': '{"cmd":"Add","data":{"id":"guest_006f721c4a59a44d969b9f73fb6360a5","users":["test"]},"location":"#"}'})
        self.assertEqual(response.status_code, 200)

    def test_chat_create_conference(self):
        "Test create_conference"
        response = self.client.post(
            '/chat', {'json': '{"cmd":"Create","data":{"title":["Admin"],"users":["admin"]},"location":"#"}'})
        self.assertEqual(response.status_code, 200)
