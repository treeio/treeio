# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Documents: test suites
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, Perspective, ModuleSetting, Object
from treeio.documents.models import Folder, Document, File, WebLink


class DocumentsModelsTest(TestCase):

    "Documents Models Tests"

    def test_model_folder(self):
        "Test Folder Model"
        obj = Folder(name='test')
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_document(self):
        "Test Document Model"
        folder = Folder(name='test')
        folder.save()
        obj = Document(title='test', folder=folder)
        obj.save()
        self.assertEquals(folder, obj.folder)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_file(self):
        "Test File Model"
        folder = Folder(name='test')
        folder.save()
        obj = File(name='test', folder=folder)
        obj.save()
        self.assertEquals(folder, obj.folder)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_weblink(self):
        "Test WebLink Model"
        folder = Folder(name='test')
        folder.save()
        obj = WebLink(title='test', folder=folder, url='test')
        obj.save()
        self.assertEquals(folder, obj.folder)
        self.assertNotEquals(obj.id, None)
        obj.delete()


class DocumentsViewsTest(TestCase):

    "Documents functional tests for views"

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
            perspective, created = Perspective.objects.get_or_create(
                name='default')
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

    ######################################
    # Testing views when user is logged in
    ######################################
    def test_index_login(self):
        "Test index page with login at /documents/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('document_index'))
        self.assertEquals(response.status_code, 200)

    def test_index_documents_login(self):
        "Test index page with login at /documents/documents/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('index_documents'))
        self.assertEquals(response.status_code, 200)

    def test_index_files_login(self):
        "Test index page with login at /documents/files/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('index_files'))
        self.assertEquals(response.status_code, 200)

    def test_index_weblinks_login(self):
        "Test index page with login at /documents/weblinks/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('index_weblinks'))
        self.assertEquals(response.status_code, 200)

    # Folders

    def test_folder_add(self):
        "Test index page with login at /documents/folder/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('documents_folder_add'))
        self.assertEquals(response.status_code, 200)
        # form
        self.assertEqual(Folder.objects.count(), 1)
        post_data = {'name': 'test'}
        response = self.client.post(reverse('documents_folder_add'), post_data)
        self.assertEquals(response.status_code, 302)  # redirect somewhere
        self.assertEquals(Folder.objects.count(), 2)

    def test_folder_view_login(self):
        "Test index page with login at /documents/folder/view/<folder_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('documents_folder_view', args=[self.folder.id]))
        self.assertEquals(response.status_code, 200)

    def test_folder_edit_login(self):
        "Test index page with login at /documents/folder/edit/<folder_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('documents_folder_edit', args=[self.folder.id]))
        self.assertEquals(response.status_code, 200)

    def test_folder_delete_login(self):
        "Test index page with login at /documents/folder/delete/<folder_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('documents_folder_delete', args=[self.folder.id]))
        self.assertEquals(response.status_code, 200)

    # Documents

    def test_document_add(self):
        "Test index page with login at /documents/add"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('documents_document_add'))
        self.assertEquals(response.status_code, 200)
        # form
        self.assertEqual(Document.objects.count(), 1)
        response = self.client.get(reverse('documents_document_add'))
        post_data = {'title': 'test',
                     'folder': self.folder,
                     }
        response = self.client.post(
            reverse('documents_document_add'), post_data)
        #self.assertEqual(Document.objects.count(), 2)

    def test_document_add_typed(self):
        "Test index page with login at /documents/add/folder/<folder_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('documents_document_add_typed', args=[self.folder.id]))
        self.assertEquals(response.status_code, 200)

    def test_document_view_login(self):
        "Test index page with login at /documents/view/<document_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('documents_document_view', args=[self.document.id]))
        self.assertEquals(response.status_code, 200)

    def test_document_edit_login(self):
        "Test index page with login at /documents/edit/<document_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('documents_document_edit', args=[self.document.id]))
        self.assertEquals(response.status_code, 200)

    def test_document_delete_login(self):
        "Test index page with login at /documents/delete/<document_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('documents_document_delete', args=[self.document.id]))
        self.assertEquals(response.status_code, 200)

    # Files

    def test_file_view_login(self):
        "Test index page with login at /file/view/<file_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('documents_file_view', args=[self.file.id]))
        self.assertEquals(response.status_code, 200)

    def test_file_edit_login(self):
        "Test index page with login at /file/edit/<file_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('documents_file_edit', args=[self.file.id]))
        self.assertEquals(response.status_code, 200)

    def test_file_delete_login(self):
        "Test index page with login at /file/view/<file_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('documents_file_delete', args=[self.file.id]))
        self.assertEquals(response.status_code, 200)

    # Web Links
    def test_weblink_add_typed(self):
        "Test index page with login at /documents/weblink/add/<folder_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('documents_weblink_add_typed', args=[self.folder.id]))
        self.assertEquals(response.status_code, 200)

    def test_weblink_add(self):
        "Test index page with login at /documents/weblink/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('documents_weblink_add'))
        self.assertEquals(response.status_code, 200)
        # form
        self.assertEqual(WebLink.objects.count(), 1)
        response = self.client.get(reverse('documents_weblink_add'))
        post_data = {'title': 'test',
                     'folder': self.folder,
                     'url': 'test',
                     }
        response = self.client.post(
            reverse('documents_weblink_add'), post_data)
        #self.assertEqual(WebLink.objects.count(), 2)

    def test_weblink_view_login(self):
        "Test index page with login at /documents/view/<weblink_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('documents_weblink_view', args=[self.link.id]))
        self.assertEquals(response.status_code, 200)

    def test_weblink_edit_login(self):
        "Test index page with login at /documents/edit/<weblink_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('documents_weblink_edit', args=[self.link.id]))
        self.assertEquals(response.status_code, 200)

    def test_weblink_delete_login(self):
        "Test index page with login at /documents/delete/<weblink_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('documents_weblink_delete', args=[self.link.id]))
        self.assertEquals(response.status_code, 200)

    ######################################
    # Testing views when user is not logged in
    ######################################
    def test_index(self):
        "Test index page at /documents/"
        response = self.client.get('/documents/')
        # Redirects as unauthenticated
        self.assertRedirects(response, reverse('user_login'))

    def test_index_documents_out(self):
        "Testing /documents/documents/"
        response = self.client.get(reverse('index_documents'))
        self.assertRedirects(response, reverse('user_login'))

    def test_index_files_out(self):
        "Testing /documents/files/"
        response = self.client.get(reverse('index_files'))
        self.assertRedirects(response, reverse('user_login'))

    def test_index_weblinks_out(self):
        "Testing /documents/weblinks/"
        response = self.client.get(reverse('index_weblinks'))
        self.assertRedirects(response, reverse('user_login'))

    # Folders

    def test_folder_add_out(self):
        "Testing /documents/folder/add/"
        response = self.client.get(reverse('documents_folder_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_folder_view_out(self):
        "Testing /documents/folder/view/<folder_id>"
        response = self.client.get(
            reverse('documents_folder_view', args=[self.folder.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_folder_edit_out(self):
        "Testing /documents/folder/edit/<folder_id>"
        response = self.client.get(
            reverse('documents_folder_edit', args=[self.folder.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_folder_delete_out(self):
        "Testing /documents/folder/delete/<folder_id>"
        response = self.client.get(
            reverse('documents_folder_delete', args=[self.folder.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Documents

    def test_document_add_out(self):
        "Testing /documents/add"
        response = self.client.get(reverse('documents_document_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_document_add_typed_out(self):
        "Testing /documents/add/folder/<folder_id>"
        response = self.client.get(
            reverse('documents_document_add_typed', args=[self.folder.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_document_view_out(self):
        "Testing /documents/view/<document_id>"
        response = self.client.get(
            reverse('documents_document_view', args=[self.document.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_document_edit_out(self):
        "Testing /documents/edit/<document_id>"
        response = self.client.get(
            reverse('documents_document_edit', args=[self.document.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_document_delete_out(self):
        "Testing /documents/delete/<document_id>"
        response = self.client.get(
            reverse('documents_document_delete', args=[self.document.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Files

    def test_file_view_out(self):
        "Testing /file/view/<file_id>"
        response = self.client.get(
            reverse('documents_file_view', args=[self.file.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_file_edit_out(self):
        "Testing /file/edit/<file_id>"
        response = self.client.get(
            reverse('documents_file_edit', args=[self.file.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_file_delete_out(self):
        "Testing /file/view/<file_id>"
        response = self.client.get(
            reverse('documents_file_delete', args=[self.file.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Web Links

    def test_weblink_add_typed_out(self):
        "Testing /documents/weblink/add/<folder_id>"
        response = self.client.get(
            reverse('documents_weblink_add_typed', args=[self.folder.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_weblink_add_out(self):
        "Testing /documents/weblink/add/"
        response = self.client.get(reverse('documents_weblink_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_weblink_view_out(self):
        "Testing /documents/view/<weblink_id>"
        response = self.client.get(
            reverse('documents_weblink_view', args=[self.link.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_weblink_edit_out(self):
        "Testing /documents/edit/<weblink_id>"
        response = self.client.get(
            reverse('documents_weblink_edit', args=[self.link.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_weblink_delete_out(self):
        "Testing /documents/delete/<weblink_id>"
        response = self.client.get(
            reverse('documents_weblink_delete', args=[self.link.id]))
        self.assertRedirects(response, reverse('user_login'))
