# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Knowledge base: test suites
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, Perspective, ModuleSetting
from treeio.knowledge.models import KnowledgeFolder, KnowledgeItem, KnowledgeCategory


class KnowledgeModelsTest(TestCase):

    " Knowledge models tests"

    def test_model_folder(self):
        "Test folder model"
        obj = KnowledgeFolder(name='test', treepath='test')
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_item(self):
        "Test item model"
        folder = KnowledgeFolder(name='test', treepath='test')
        folder.save()
        category = KnowledgeCategory(name='test', treepath='test')
        category.save()
        obj = KnowledgeItem(
            name='test', folder=folder, category=category, treepath='test')
        obj.save()
        self.assertEquals(folder, obj.folder)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_category(self):
        "Test category model"
        obj = KnowledgeCategory(name='test', details='test', treepath='test')
        obj.save()
        obj.delete()


class KnowledgeViewsTest(TestCase):

    "Knowledge functional tests for views"

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

            self.folder = KnowledgeFolder(name='test', treepath='test')
            self.folder.set_default_user()
            self.folder.save()

            self.category = KnowledgeCategory(name='test', treepath='test')
            self.category.set_default_user()
            self.category.save()

            self.item = KnowledgeItem(name='test', folder=self.folder,
                                      category=self.category, treepath='test')
            self.item.set_default_user()
            self.item.save()

            # parent folder
            self.parent = KnowledgeFolder(name='test', treepath='test')
            self.parent.set_default_user()
            self.parent.save()

            self.client = Client()

            self.prepared = True

    ######################################
    # Testing views when user is logged in
    ######################################
    def test_index_login(self):
        "Test index page with login at /knowledge/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('knowledge'))
        self.assertEquals(response.status_code, 200)

    def test_index_categories_login(self):
        "Test index page with login at /knowledge/categories/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('knowledge_categories'))
        self.assertEquals(response.status_code, 200)

    # Knowledge folders
    def test_knowledge_folder_add(self):
        "Test index page with login at /knowledge/folder/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('knowledge_folder_add'))
        self.assertEquals(response.status_code, 200)

    def test_knowledge_folder_add_typed(self):
        "Test index page with login at /knowledge/folder/add/<folderPath>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('knowledge_folder_add_folder', args=[self.parent.treepath]))
        self.assertEquals(response.status_code, 200)

    def test_knowledge_folder_view(self):
        "Test index page with login at /knowledge/folder/view/<knowledgeType_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('knowledge_folder_view', args=[self.folder.treepath]))
        self.assertEquals(response.status_code, 200)

    def test_knowledge_folder_edit(self):
        "Test index page with login at /knowledge/folder/edit/<knowledgeType_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('knowledge_folder_edit', args=[self.folder.id]))
        self.assertEquals(response.status_code, 200)

    def test_knowledge_folder_delete(self):
        "Test index page with login at /knowledge/folder/delete/<knowledgeType_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('knowledge_folder_delete', args=[self.folder.id]))
        self.assertEquals(response.status_code, 200)

    # Knowledge items
    def test_knowledge_item_add(self):
        "Test index page with login at /knowledge/item/add"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('knowledge_item_add'))
        self.assertEquals(response.status_code, 200)

    def test_knowledge_item_add_typed(self):
        "Test index page with login at /knowledge/item/add/<folderPath>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('knowledge_item_add_folder', args=[self.folder.treepath]))
        self.assertEquals(response.status_code, 200)

    def test_knowledge_item_view(self):
        "Test index page with login at /knowledge/item/view/<knowledgeItem_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('knowledge_item_view',
                                           args=[self.item.folder.treepath, self.item.treepath]))
        self.assertEquals(response.status_code, 200)

    def test_knowledge_item_edit(self):
        "Test index page with login at /knowledge/item/edit/<knowledgeItem_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('knowledge_item_edit', args=[self.item.id]))
        self.assertEquals(response.status_code, 200)

    def test_knowledge_item_delete(self):
        "Test index page with login at /knowledge/item/delete/<knowledgeItem_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('knowledge_item_delete', args=[self.item.id]))
        self.assertEquals(response.status_code, 200)

    # Knowledge categories
    def test_knowledge_category_add(self):
        "Test index page with login at /knowledge/category/add"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('knowledge_category_add'))
        self.assertEquals(response.status_code, 200)

    def test_knowledge_category_view(self):
        "Test index page with login at /knowledge/category/view/<knowledgeCategory_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('knowledge_category_view', args=[self.category.treepath]))
        self.assertEquals(response.status_code, 200)

    def test_knowledge_category_edit(self):
        "Test index page with login at /knowledge/category/edit/<knowledgeCategory_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('knowledge_category_edit', args=[self.category.id]))
        self.assertEquals(response.status_code, 200)

    def test_knowledge_category_delete(self):
        "Test index page with login at /knowledge/category/delete/<knowledgeCategory_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('knowledge_category_delete', args=[self.category.id]))
        self.assertEquals(response.status_code, 200)

    ######################################
    # Testing views when user is not logged in
    ######################################
    def test_index(self):
        "Test index page at /knowledge/"
        response = self.client.get('/knowledge/')
        # Redirects as unauthenticated
        self.assertRedirects(response, reverse('user_login'))

    def test_index_categories_out(self):
        "Testing /knowledge/categories/"
        response = self.client.get(reverse('knowledge_categories'))
        self.assertRedirects(response, reverse('user_login'))

    # Knowledge folders

    def test_knowledge_folder_add_out(self):
        "Testing /knowledge/folder/add/"
        response = self.client.get(reverse('knowledge_folder_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_knowledge_folder_add_typed_out(self):
        "Testing /knowledge/folder/add/<folderPath>"
        response = self.client.get(
            reverse('knowledge_folder_add_folder', args=[self.parent.treepath]))
        self.assertRedirects(response, reverse('user_login'))

    def test_knowledge_folder_view_out(self):
        "Testing /knowledge/folder/view/<knowledgeType_id>"
        response = self.client.get(
            reverse('knowledge_folder_view', args=[self.folder.treepath]))
        self.assertRedirects(response, reverse('user_login'))

    def test_knowledge_folder_edit_out(self):
        "Testing /knowledge/folder/edit/<knowledgeType_id>"
        response = self.client.get(
            reverse('knowledge_folder_edit', args=[self.folder.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_knowledge_folder_delete_out(self):
        "Testing /knowledge/folder/delete/<knowledgeType_id>"
        response = self.client.get(
            reverse('knowledge_folder_delete', args=[self.folder.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Knowledge items
    def test_knowledge_item_add_out(self):
        "Testing /knowledge/item/add"
        response = self.client.get(reverse('knowledge_item_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_knowledge_item_add_typed_out(self):
        "Testing /knowledge/item/add/<folderPath>"
        response = self.client.get(
            reverse('knowledge_item_add_folder', args=[self.folder.treepath]))
        self.assertRedirects(response, reverse('user_login'))

    def test_knowledge_item_view_out(self):
        "Testing /knowledge/item/view/<knowledgeItem_id>"
        response = self.client.get(reverse('knowledge_item_view',
                                           args=[self.item.folder.treepath, self.item.treepath]))
        self.assertRedirects(response, reverse('user_login'))

    def test_knowledge_item_edit_out(self):
        "Testing /knowledge/item/edit/<knowledgeItem_id>"
        response = self.client.get(
            reverse('knowledge_item_edit', args=[self.item.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_knowledge_item_delete_out(self):
        "Testing /knowledge/item/delete/<knowledgeItem_id>"
        response = self.client.get(
            reverse('knowledge_item_delete', args=[self.item.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Knowledge categories
    def test_knowledge_category_add_out(self):
        "Testing /knowledge/category/add"
        response = self.client.get(reverse('knowledge_category_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_knowledge_category_view_out(self):
        "Testing /knowledge/category/view/<knowledgeCategory_id>"
        response = self.client.get(
            reverse('knowledge_category_view', args=[self.category.treepath]))
        self.assertRedirects(response, reverse('user_login'))

    def test_knowledge_category_edit_out(self):
        "Testing /knowledge/category/edit/<knowledgeCategory_id>"
        response = self.client.get(
            reverse('knowledge_category_edit', args=[self.category.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_knowledge_category_delete_out(self):
        "Testing /knowledge/category/delete/<knowledgeCategory_id>"
        response = self.client.get(
            reverse('knowledge_category_delete', args=[self.category.id]))
        self.assertRedirects(response, reverse('user_login'))
