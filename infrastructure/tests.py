# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Infrastructure: test suites
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, Perspective, ModuleSetting
from treeio.infrastructure.models import Item, ItemValue, ItemField, ItemType, ItemStatus, ItemServicing


class InfrastructureModelsTest(TestCase):

    "Infrastructure models tests"

    def test_model_item_field(self):
        "Test item field model"
        obj = ItemField(name='test', label='test', field_type='text')
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_item_type(self):
        "Test item type model"
        obj = ItemType(name='test')
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_item_status(self):
        "Test item status model"
        obj = ItemStatus(name='test')
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_item(self):
        "Test item model"

        type = ItemType(name='test')
        type.save()

        status = ItemStatus(name='test')
        status.save()

        obj = Item(name='test', item_type=type, status=status)
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_item_value(self):
        "Test item value model"

        status = ItemStatus(name='test')
        status.save()

        type = ItemType(name='test')
        type.save()

        item = Item(name='test', item_type=type, status=status)
        item.save()

        field = ItemField(name='test', label='test', field_type='text')
        field.save()

        obj = ItemValue(value='test', field=field, item=item)
        obj.save()
        self.assertEquals('test', obj.value)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_item_servicing(self):
        "Test item servicing model"
        obj = ItemServicing(name='test')
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()


class InfrastructureViewsTest(TestCase):

    "Infrastructure functional tests for views"

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

            self.type = ItemType(name='test')
            self.type.set_default_user()
            self.type.save()

            self.status = ItemStatus(name='test')
            self.status.set_default_user()
            self.status.save()

            self.field = ItemField(
                name='test', label='test', field_type='text')
            self.field.set_default_user()
            self.field.save()

            self.item = Item(
                name='test', item_type=self.type, status=self.status)
            self.item.set_default_user()
            self.item.save()

            self.value = ItemValue(field=self.field, item=self.item)
            self.value.save()

            self.servicing = ItemServicing(name='test')
            self.servicing.set_default_user()
            self.servicing.save()

            self.client = Client()

            self.prepared = True

    ######################################
    # Testing views when user is logged in
    ######################################
    def test_index_login(self):
        "Test index page with login at /infrastructure/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('infrastructure'))
        self.assertEquals(response.status_code, 200)

    def test_index_infrastructure_login(self):
        "Test index page with login at /infrastructure/index/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('infrastructure_index'))
        self.assertEquals(response.status_code, 200)

    def test_infrastructure_index_owned(self):
        "Test index page with login at /infrastructure/owned/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('infrastructure_index_owned'))
        self.assertEquals(response.status_code, 200)

    # Type
    def test_infrastructure_type_add(self):
        "Test index page with login at /infrastructure/type/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('infrastructure_type_add'))
        self.assertEquals(response.status_code, 200)

    def test_infrastructure_type_view(self):
        "Test index page with login at /infrastructure/type/view/<type_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('infrastructure_type_view', args=[self.type.id]))
        self.assertEquals(response.status_code, 200)

    def test_infrastructure_type_edit(self):
        "Test index page with login at /infrastructure/type/edit/<type_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('infrastructure_type_edit', args=[self.type.id]))
        self.assertEquals(response.status_code, 200)

    def test_infrastructure_type_delete(self):
        "Test index page with login at /infrastructure/type/delete/<type_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('infrastructure_type_delete', args=[self.type.id]))
        self.assertEquals(response.status_code, 200)

    # Field
    def test_infrastructure_field_add(self):
        "Test index page with login at /infrastructure/field/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('infrastructure_field_add'))
        self.assertEquals(response.status_code, 200)

    def test_infrastructure_field_view(self):
        "Test index page with login at /infrastructure/field/view/<field_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('infrastructure_field_view', args=[self.field.id]))
        self.assertEquals(response.status_code, 200)

    def test_infrastructure_field_edit(self):
        "Test index page with login at /infrastructure/field/edit/<field_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('infrastructure_field_edit', args=[self.field.id]))
        self.assertEquals(response.status_code, 200)

    def test_infrastructure_field_del(self):
        "Test index page with login at /infrastructure/field/delete/<field_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('infrastructure_field_delete', args=[self.field.id]))
        self.assertEquals(response.status_code, 200)

    # Status
    def test_infrastructure_status_add(self):
        "Test index page with login at /infrastructure/status/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('infrastructure_status_add'))
        self.assertEquals(response.status_code, 200)

    def test_infrastructure_status_view(self):
        "Test index page with login at /infrastructure/status/view/<status_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('infrastructure_status_view', args=[self.status.id]))
        self.assertEquals(response.status_code, 200)

    def test_infrastructure_status_edit(self):
        "Test index page with login at /infrastructure/status/edit/<status_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('infrastructure_status_edit', args=[self.status.id]))
        self.assertEquals(response.status_code, 200)

    def test_infrastructure_status_del(self):
        "Test index page with login at /infrastructure/status/delete/<status_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('infrastructure_status_delete', args=[self.status.id]))
        self.assertEquals(response.status_code, 200)

    # Item
    def test_infrastructure_item_add(self):
        "Test index page with login at /infrastructure/item/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('infrastructure_item_add'))
        self.assertEquals(response.status_code, 200)

    def test_infr_item_add_typed(self):
        "Test index page with login at /infrastructure/item/add/<type_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('infrastructure_item_add_typed', args=[self.type.id]))
        self.assertEquals(response.status_code, 200)

    def test_infrastructure_item_view(self):
        "Test index page with login at /infrastructure/item/view/<item_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('infrastructure_item_view', args=[self.item.id]))
        self.assertEquals(response.status_code, 200)

    def test_infrastructure_item_edit(self):
        "Test index page with login at /infrastructure/item/edit/<item_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('infrastructure_item_edit', args=[self.item.id]))
        self.assertEquals(response.status_code, 200)

    def test_infrastructure_item_del(self):
        "Test index page with login at /infrastructure/item/delete/<item_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('infrastructure_item_delete', args=[self.item.id]))
        self.assertEquals(response.status_code, 200)

    # Service Record
    def test_infr_service_record_index(self):
        "Test index page with login at /infrastructure/service_record/index/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('infrastructure_service_record_index'))
        self.assertEquals(response.status_code, 200)

    def test_infr_service_record_add(self):
        "Test index page with login at /infrastructure/service_record/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('infrastructure_service_record_add'))
        self.assertEquals(response.status_code, 200)

    def test_infr_service_record_view(self):
        "Test index page with login at /infrastructure/service_record/view/<service_record_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('infrastructure_service_record_view', args=[self.servicing.id]))
        self.assertEquals(response.status_code, 200)

    def test_infr_service_record_edit(self):
        "Test index page with login at /infrastructure/service_record/edit/<service_record_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('infrastructure_service_record_edit', args=[self.servicing.id]))
        self.assertEquals(response.status_code, 200)

    def test_infr_service_record_delete(self):
        "Test index page with login at /infrastructure/service_record/delete/<service_record_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('infrastructure_service_record_delete', args=[self.servicing.id]))
        self.assertEquals(response.status_code, 200)

    ######################################
    # Testing views when user is not logged in
    ######################################
    def test_index(self):
        "Testing /infrastructure/"
        response = self.client.get('/infrastructure/')
        # Redirects as unauthenticated
        self.assertRedirects(response, reverse('user_login'))

    def test_index_infrastructure_out(self):
        "Testing /infrastructure/index/"
        response = self.client.get(reverse('infrastructure_index'))
        self.assertRedirects(response, reverse('user_login'))

    def test_infrastructure_index_owned_out(self):
        "Testing /infrastructure/owned/"
        response = self.client.get(reverse('infrastructure_index_owned'))
        self.assertRedirects(response, reverse('user_login'))

    # Type
    def test_infrastructure_type_add_out(self):
        "Testing /infrastructure/type/add/"
        response = self.client.get(reverse('infrastructure_type_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_infrastructure_type_view_out(self):
        "Testing /infrastructure/type/view/<type_id>"
        response = self.client.get(
            reverse('infrastructure_type_view', args=[self.type.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_infrastructure_type_edit_out(self):
        "Testing /infrastructure/type/edit/<type_id>"
        response = self.client.get(
            reverse('infrastructure_type_edit', args=[self.type.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_infrastructure_type_delete_out(self):
        "Testing /infrastructure/type/delete/<type_id>"
        response = self.client.get(
            reverse('infrastructure_type_delete', args=[self.type.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Field
    def test_infrastructure_field_add_out(self):
        "Testing /infrastructure/field/add/"
        response = self.client.get(reverse('infrastructure_field_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_infrastructure_field_view_out(self):
        "Testing /infrastructure/field/view/<field_id>"
        response = self.client.get(
            reverse('infrastructure_field_view', args=[self.field.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_infrastructure_field_edit_out(self):
        "Testing /infrastructure/field/edit/<field_id>"
        response = self.client.get(
            reverse('infrastructure_field_edit', args=[self.field.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_infrastructure_field_del_out(self):
        "Testing /infrastructure/field/delete/<field_id>"
        response = self.client.get(
            reverse('infrastructure_field_delete', args=[self.field.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Status
    def test_infrastructure_status_add_out(self):
        "Testing /infrastructure/status/add/"
        response = self.client.get(reverse('infrastructure_status_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_infrastructure_status_view_out(self):
        "Testing /infrastructure/status/view/<status_id>"
        response = self.client.get(
            reverse('infrastructure_status_view', args=[self.status.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_infrastructure_status_edit_out(self):
        "Testing /infrastructure/status/edit/<status_id>"
        response = self.client.get(
            reverse('infrastructure_status_edit', args=[self.status.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_infrastructure_status_del_out(self):
        "Testing /infrastructure/status/delete/<status_id>"
        response = self.client.get(
            reverse('infrastructure_status_delete', args=[self.status.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Item
    def test_infrastructure_item_add_out(self):
        "Testing /infrastructure/item/add/"
        response = self.client.get(reverse('infrastructure_item_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_infr_item_add_typed_out(self):
        "Testing /infrastructure/item/add/<type_id>"
        response = self.client.get(
            reverse('infrastructure_item_add_typed', args=[self.type.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_infrastructure_item_view_out(self):
        "Testing /infrastructure/item/view/<item_id>"
        response = self.client.get(
            reverse('infrastructure_item_view', args=[self.item.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_infrastructure_item_edit_out(self):
        "Testing /infrastructure/item/edit/<item_id>"
        response = self.client.get(
            reverse('infrastructure_item_edit', args=[self.item.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_infrastructure_item_del_out(self):
        "Testing /infrastructure/item/delete/<item_id>"
        response = self.client.get(
            reverse('infrastructure_item_delete', args=[self.item.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Service Record
    def test_infr_service_record_index_out(self):
        "Testing /infrastructure/service_record/index/"
        response = self.client.get(
            reverse('infrastructure_service_record_index'))
        self.assertRedirects(response, reverse('user_login'))

    def test_infr_service_record_add_out(self):
        "Testing /infrastructure/service_record/add/"
        response = self.client.get(
            reverse('infrastructure_service_record_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_infr_service_record_view_out(self):
        "Testing /infrastructure/service_record/view/<service_record_id>"
        response = self.client.get(
            reverse('infrastructure_service_record_view', args=[self.servicing.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_infr_service_record_edit_out(self):
        "Testing /infrastructure/service_record/edit/<service_record_id>"
        response = self.client.get(
            reverse('infrastructure_service_record_edit', args=[self.servicing.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_infr_service_record_delete_out(self):
        "Testing /infrastructure/service_record/delete/<service_record_id>"
        response = self.client.get(
            reverse('infrastructure_service_record_delete', args=[self.servicing.id]))
        self.assertRedirects(response, reverse('user_login'))
