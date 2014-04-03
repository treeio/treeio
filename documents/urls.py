# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio
# License www.tree.io/license

"""
Documents module URLs
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('treeio.documents.views',
    url(r'^(\.(?P<response_format>\w+))?$',
        'index', name='document'),
    url(r'^index(\.(?P<response_format>\w+))?$',
        'index', name='document_index'),
    url(r'^files(\.(?P<response_format>\w+))?/?$',
        'index_files', name='index_files'),
    url(r'^documents(\.(?P<response_format>\w+))?/?$',
        'index_documents', name='index_documents'),
    url(r'^weblinks(\.(?P<response_format>\w+))?/?$',
        'index_weblinks', name='index_weblinks'),

    # Folders
    url(r'^folder/add(\.(?P<response_format>\w+))?/?$',
        'folder_add', name='documents_folder_add'),
    url(r'^folder/add/folder/(?P<folder_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'folder_add_typed', name='documents_folder_add_typed'),
    url(r'^folder/view/(?P<folder_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'folder_view', name='documents_folder_view'),
    url(r'^folder/edit/(?P<folder_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'folder_edit', name='documents_folder_edit'),
    url(r'^folder/delete/(?P<folder_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'folder_delete', name='documents_folder_delete'),

    # Documents
    url(r'^add(\.(?P<response_format>\w+))?/?$',
        'document_add', name='documents_document_add'),
    url(r'^add/folder/(?P<folder_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'document_add_typed', name='documents_document_add_typed'),
    url(r'^view/(?P<document_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'document_view', name='documents_document_view'),
    url(r'^edit/(?P<document_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'document_edit', name='documents_document_edit'),
    url(r'^delete/(?P<document_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'document_delete', name='documents_document_delete'),

    # Files
    url(r'^file/view/(?P<file_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'file_view', name='documents_file_view'),
    url(r'^file/upload(\.(?P<response_format>\w+))?/?$',
        'file_upload', name='documents_file_upload'),
    url(r'^file/upload/folder/(?P<folder_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'file_upload_typed', name='documents_file_upload_typed'),
    url(r'^file/delete/(?P<file_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'file_delete', name='documents_file_delete'),
    url(r'^file/edit/(?P<file_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'file_edit', name='documents_file_edit'),

    # Web Links
    url(r'^weblink/add(\.(?P<response_format>\w+))?/?$',
        'weblink_add', name='documents_weblink_add'),
    url(r'^weblink/add/folder/(?P<folder_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'weblink_add_typed', name='documents_weblink_add_typed'),
    url(r'^weblink/view/(?P<weblink_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'weblink_view', name='documents_weblink_view'),
    url(r'^weblink/edit/(?P<weblink_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'weblink_edit', name='documents_weblink_edit'),
    url(r'^weblink/delete/(?P<weblink_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'weblink_delete', name='documents_weblink_delete'),
)
