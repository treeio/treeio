# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Documents: test api
"""

import json
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, Perspective, ModuleSetting, Object
from treeio.documents.models import Folder, Document, File, WebLink


class DocumentsViewsTest(TestCase):

    "Documents functional tests for api"

    username = "api_test"
    password = "api_password"
    prepared = False
    authentication_headers = {"CONTENT_TYPE": "application/json",
                              "HTTP_AUTHORIZATION": "Basic YXBpX3Rlc3Q6YXBpX3Bhc3N3b3Jk"}
    content_type = 'application/json'

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

            self.folder = Folder(name='test')
            self.folder.set_default_user()
            self.folder.save()

            self.document = Document(title='test_document', folder=self.folder)
            self.document.set_default_user()
            self.document.save()

            self.file = File(name='test_file', folder=self.folder)
            self.file.set_default_user()
            self.file.save()

            self.link = WebLink(title='test', folder=self.folder, url='test')
            self.link.set_default_user()
            self.link.save()

            self.client = Client()

            self.prepared = True

    def test_unauthenticated_access(self):
        "Test index page at /api/documents/folders"
        response = self.client.get('/api/documents/folders')
        # Redirects as unauthenticated
        self.assertEquals(response.status_code, 401)

    def test_get_folders_list(self):
        """ Test index page api/documents/folders """
        response = self.client.get(
            path=reverse('api_documents_folders'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_folder(self):
        response = self.client.get(path=reverse('api_documents_folders', kwargs={
                                   'object_ptr': self.folder.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_folder(self):
        updates = {"name": "Api_folder_name"}
        response = self.client.put(path=reverse('api_documents_folders', kwargs={'object_ptr': self.folder.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['name'], updates['name'])

    def test_get_files_list(self):
        """ Test index page api/documents/files """
        response = self.client.get(
            path=reverse('api_documents_files'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_file(self):
        response = self.client.get(path=reverse('api_documents_files', kwargs={
                                   'object_ptr': self.file.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

#    def test_update_file(self):
#        updates = { "name": "Api_folder_name" }
#        response = self.client.put(path=reverse('api_documents_files', kwargs={'object_ptr': self.file.id}),
#                                   content_type=self.content_type,  data=json.dumps(updates), **self.authentication_headers)
#        self.assertEquals(response.status_code, 200)
#
#        data = json.loads(response.content)
#        self.assertEquals(data['name'], updates['name'])

    def test_get_documents_list(self):
        """ Test index page api/documents/documents """
        response = self.client.get(
            path=reverse('api_documents_documents'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_document(self):
        response = self.client.get(path=reverse('api_documents_documents', kwargs={
                                   'object_ptr': self.document.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_document(self):
        updates = {"title": "Api_title",
                   "folder": self.folder.id, "body": "Api test body"}
        response = self.client.put(path=reverse('api_documents_documents', kwargs={'object_ptr': self.document.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['title'], updates['title'])
        self.assertEquals(data['folder']['id'], updates['folder'])
        self.assertEquals(data['body'], updates['body'])

    def test_get_weblinks_list(self):
        """ Test index page api/documents/weblinks """
        response = self.client.get(
            path=reverse('api_documents_weblinks'), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_get_weblink(self):
        response = self.client.get(path=reverse('api_documents_weblinks', kwargs={
                                   'object_ptr': self.link.id}), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

    def test_update_weblink(self):
        updates = {"title": "Api_title", "folder": self.folder.id,
                   "url": "http://Api-test-body"}
        response = self.client.put(path=reverse('api_documents_weblinks', kwargs={'object_ptr': self.link.id}),
                                   content_type=self.content_type, data=json.dumps(updates), **self.authentication_headers)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(data['title'], updates['title'])
        self.assertEquals(data['folder']['id'], updates['folder'])
        self.assertEquals(data['url'], updates['url'])
