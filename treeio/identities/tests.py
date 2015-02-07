# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Identities: test suites
"""

from django.test import TestCase
from treeio.identities.models import Contact, ContactType, ContactField
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, Perspective, ModuleSetting, Object


class IdentitiesModelsTest(TestCase):

    "Identities Model Tests"

    def test_model_contacttype(self):
        "Test ContactType model"
        obj = ContactType(name='Test', slug='test')
        obj.save()
        self.assertEquals('Test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_contact(self):
        "Test Contact model"
        type = ContactType(name='Test', slug='test')
        type.save()
        obj = Contact(name='Test', contact_type=type)
        obj.save()
        self.assertEquals('Test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_field(self):
        "Test Field model"
        obj = ContactField(name='Test', label='test', field_type='text')
        obj.save()
        self.assertEquals('Test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()


class IdentitiesViewsTest(TestCase):

    "Identities View tests"
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

            self.contact_type = ContactType(name='Person')
            self.contact_type.set_default_user()
            self.contact_type.save()

            self.contact = Contact(name='Test', contact_type=self.contact_type)
            self.contact.set_default_user()
            self.contact.save()

            self.field = ContactField(
                name='Test', label='test', field_type='text')
            self.field.set_default_user()
            self.field.save()

            self.client = Client()

            self.prepared = True

    ######################################
    # Testing views when user is logged in
    ######################################
    def test_index_login(self):
        "Test index page with login at /contacts/"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('identities_index'))
        self.assertEquals(response.status_code, 200)

    def test_contact_users_login(self):
        "Test page with login at /contacts/users/"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('identities_index_users'))
        self.assertEquals(response.status_code, 200)

    def test_contact_groups_login(self):
        "Test page with login at /contacts/groups/"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('identities_index_groups'))
        self.assertEquals(response.status_code, 200)

    # Contact types
    def test_contact_type_add(self):
        "Test page with login at /contacts/types/add/"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('identities_type_add'))
        self.assertEquals(response.status_code, 200)

    def test_contact_type_view(self):
        "Test page with login at /contacts/type/view/(?P<type_id>\d+)"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('identities_type_view', args=[self.contact_type.id]))
        self.assertEquals(response.status_code, 200)

    def test_contact_type_edit(self):
        "Test page with login at /contacts/type/edit/(?P<type_id>\d+)"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('identities_type_edit', args=[self.contact_type.id]))
        self.assertEquals(response.status_code, 200)

    def test_contact_type_delete(self):
        "Test page with login at /contacts/type/delete/(?P<type_id>\d+)"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('identities_type_delete', args=[self.contact_type.id]))
        self.assertEquals(response.status_code, 200)

    # Contact fields
    def test_contact_field_add(self):
        "Test page with login at /contacts/field/add"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('identities_field_add'))
        self.assertEquals(response.status_code, 200)

    def test_contact_field_view(self):
        "Test page with login at /contacts/field/view/(?P<field_id>\d+)"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('identities_field_view', args=[self.field.id]))
        self.assertEquals(response.status_code, 200)

    def test_contact_field_edit(self):
        "Test page with login at /contacts/field/edit/(?P<field_id>\d+)"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('identities_field_edit', args=[self.field.id]))
        self.assertEquals(response.status_code, 200)

    def test_contact_field_delete(self):
        "Test page with login at /contacts/field/delete/(?P<field_id>\d+)"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('identities_field_delete', args=[self.field.id]))
        self.assertEquals(response.status_code, 200)

    # Contacts
    def test_contact_add(self):
        "Test page with login at /contacts/contact/add/"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('identities_contact_add'))
        self.assertEquals(response.status_code, 200)

    def test_contact_add_by_type(self):
        "Test page with login at /contacts/contact/add/<type_id>/"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('identities_contact_add_typed', args=[self.contact_type.id]))
        self.assertEquals(response.status_code, 200)

    def test_contact_me(self):
        "Test page with login at /contacts/me/"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('identities_contact_me'))
        self.assertEquals(response.status_code, 200)

    def test_contact_view(self):
        "Test page with login at /contacts/contact/view/<contact_id>/"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('identities_contact_view', args=[self.contact.id]))
        self.assertEquals(response.status_code, 200)

    def test_contact_edit(self):
        "Test page with login at /contacts/contact/edit/<contact_id>/"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('identities_contact_edit', args=[self.contact.id]))
        self.assertEquals(response.status_code, 200)

    def test_contact_delete(self):
        "Test page with login at /contacts/contact/delete/<contact_id>/"
        response = self.client.post('/accounts/login', {'username': self.username,
                                                        'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('identities_contact_delete', args=[self.contact.id]))
        self.assertEquals(response.status_code, 200)

    # Settings
    def test_contact_settings_view(self):
        "Test index page with login at /contacts/settings/view/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('identities_settings_view'))
        self.assertEquals(response.status_code, 200)

    ######################################
    # Testing views when user is not logged in
    ######################################
    def test_index(self):
        "Test index page at /contacts/"
        response = self.client.get('/contacts/')
        # Redirects as unauthenticated
        self.assertRedirects(response, reverse('user_login'))

    def test_contact_users_out(self):
        "Testing /contacts/users/"
        response = self.client.get(reverse('identities_index_users'))
        self.assertRedirects(response, reverse('user_login'))

    def test_contact_groups_out(self):
        "Testing /contacts/groups/"
        response = self.client.get(reverse('identities_index_groups'))
        self.assertRedirects(response, reverse('user_login'))

    # Contact types
    def test_contact_type_add_out(self):
        "Testing /contacts/types/add/"
        response = self.client.get(reverse('identities_type_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_contact_type_view_out(self):
        "Testing /contacts/type/view/(?P<type_id>\d+)"
        response = self.client.get(
            reverse('identities_type_view', args=[self.contact_type.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_contact_type_edit_out(self):
        "Testing /contacts/type/edit/(?P<type_id>\d+)"
        response = self.client.get(
            reverse('identities_type_edit', args=[self.contact_type.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_contact_type_delete_out(self):
        "Testing /contacts/type/delete/(?P<type_id>\d+)"
        response = self.client.get(
            reverse('identities_type_delete', args=[self.contact_type.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Contact fields
    def test_contact_field_add_out(self):
        "Testing /contacts/field/add"
        response = self.client.get(reverse('identities_field_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_contact_field_view_out(self):
        "Testing /contacts/field/view/(?P<field_id>\d+)"
        response = self.client.get(
            reverse('identities_field_view', args=[self.field.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_contact_field_edit_out(self):
        "Testing /contacts/field/edit/(?P<field_id>\d+)"
        response = self.client.get(
            reverse('identities_field_edit', args=[self.field.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_contact_field_delete_out(self):
        "Testing /contacts/field/delete/(?P<field_id>\d+)"
        response = self.client.get(
            reverse('identities_field_delete', args=[self.field.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Contacts
    def test_contact_add_out(self):
        "Testing /contacts/contact/add/"
        response = self.client.get(reverse('identities_contact_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_contact_add_by_type_out(self):
        "Testing /contacts/contact/add/<type_id>/"
        response = self.client.get(
            reverse('identities_contact_add_typed', args=[self.contact_type.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_contact_me_out(self):
        "Testing /contacts/me/"
        response = self.client.get(reverse('identities_contact_me'))
        self.assertRedirects(response, reverse('user_login'))

    def test_contact_view_out(self):
        "Testing /contacts/contact/view/<contact_id>/"
        response = self.client.get(
            reverse('identities_contact_view', args=[self.contact.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_contact_edit_out(self):
        "Testing /contacts/contact/edit/<contact_id>/"
        response = self.client.get(
            reverse('identities_contact_edit', args=[self.contact.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_contact_delete_out(self):
        "Testing /contacts/contact/delete/<contact_id>/"
        response = self.client.get(
            reverse('identities_contact_delete', args=[self.contact.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Settings
    def test_contact_settings_view_out(self):
        "Testing /contacts/settings/view/"
        response = self.client.get(reverse('identities_settings_view'))
        self.assertRedirects(response, reverse('user_login'))
