# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Knowledge api: test suites
"""
import json
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, Perspective, ModuleSetting, Object
from treeio.knowledge.models import KnowledgeFolder, KnowledgeItem, KnowledgeCategory


class KnowledgeViewsTest(TestCase):

    "Knowledge functional tests for views"

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

    def test_unauthenticated_access(self):
        "Test index page at /api/knowledge/folders"
        response = self.client.get('/api/knowledge/folders')
        # Redirects as unauthenticated
        self.assertEquals(response.status_code, 401)

    def test_get_folders_list(self):
        """ Test index page api/knowledge/folders """
        response = self.client.get(
            path=reverse('api_knowledge_folders'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_folder(self):
        response = self.client.get(path=reverse('api_knowledge_folders', kwargs={
                                   'object_ptr': self.folder.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_folder(self):
        updates = {'name': 'Api folder update',
                   'parent': self.parent.id, 'details': '<p>api details</p>'}
        response = self.client.put(path=reverse('api_knowledge_folders', kwargs={'object_ptr': self.folder.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(updates["name"], data["name"])
        self.assertEquals(updates["parent"], data["parent"]["id"])
        self.assertEquals(updates["details"], data["details"])

    def test_get_categories_list(self):
        """ Test index page api/knowledge/categories """
        response = self.client.get(
            path=reverse('api_knowledge_categories'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_category(self):
        response = self.client.get(path=reverse('api_knowledge_categories', kwargs={
                                   'object_ptr': self.category.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_category(self):
        updates = {
            'name': 'Api catagory update', 'details': '<p>api details</p>'}
        response = self.client.put(path=reverse('api_knowledge_categories', kwargs={'object_ptr': self.category.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(updates["name"], data["name"])
        self.assertEquals(updates["details"], data["details"])

    def test_get_items_list(self):
        """ Test index page api/knowledge/items """
        response = self.client.get(
            path=reverse('api_knowledge_items'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_item(self):
        response = self.client.get(path=reverse('api_knowledge_items', kwargs={
                                   'object_ptr': self.item.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_item(self):
        updates = {'name': 'Api item update', 'folder': self.folder.id, 'category': self.category.id,
                   'body': '<p>api body</p>'}
        response = self.client.put(path=reverse('api_knowledge_items', kwargs={'object_ptr': self.item.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 400)

        #data = json.loads(response.content)
        #self.assertEquals(updates["name"], data["name"])
        #self.assertEquals(updates["body"], data["body"])
        #self.assertEquals(updates["folder"], data["folder"]["id"])
        #self.assertEquals(updates["category"], data["category"]["id"])
