# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Knowledge base module URLs
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('treeio.knowledge.views',
    url(r'^(\.(?P<response_format>\w+))?$',
        'index', name='knowledge'),
    url(r'^index(\.(?P<response_format>\w+))?$',
        'index', name='knowledge_index'),
    url(r'^categories(\.(?P<response_format>\w+))?/?$',
        'index_categories', name='knowledge_categories'),

    # Folders
    url(r'^folder/add(\.(?P<response_format>\w+))?/?$',
        'folder_add', name='knowledge_folder_add'),
    url(r'^folder/add/(?P<folderPath>.(?:[a-z,0-9,-]+/)+)(\.(?P<response_format>\w+))?/?$',
        'folder_add_folder', name='knowledge_folder_add_folder'),
    url(r'^folder/(?P<folderPath>.(?:[a-z,0-9,-]+/)+)(\.(?P<response_format>\w+))?/?$',
        'folder_view', name='knowledge_folder_view'),
    url(r'^folder/edit/(?P<knowledgeType_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'folder_edit', name='knowledge_folder_edit'),
    url(r'^folder/delete/(?P<knowledgeType_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'folder_delete', name='knowledge_folder_delete'),

    # Knowledge Items
    url(r'^item/add(\.(?P<response_format>\w+))?/?$',
        'item_add', name='knowledge_item_add'),
    url(r'^item/add/(?P<folderPath>.(?:[a-z,0-9,-]+/)+)(\.(?P<response_format>\w+))?/?$',
        'item_add_folder', name='knowledge_item_add_folder'),
    url(r'^(?P<folderPath>.(?:[a-z,0-9,-]+/)+)(?P<itemPath>.(?:[a-z,0-9,-]+/)+)(\.(?P<response_format>\w+))?/?$',
        'item_view', name='knowledge_item_view'),
    url(r'^item/edit/(?P<knowledgeItem_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'item_edit', name='knowledge_item_edit'),
    url(r'^item/delete/(?P<knowledgeItem_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'item_delete', name='knowledge_item_delete'),

    # Categories
    url(r'^category/add(\.(?P<response_format>\w+))?/?$',
        'category_add', name='knowledge_category_add'),
    url(r'^(?P<categoryPath>.(?:[a-z,0-9,-]+/)+)(\.(?P<response_format>\w+))?/?$',
        'category_view', name='knowledge_category_view'),
    url(r'^category/edit/(?P<knowledgeCategory_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'category_edit', name='knowledge_category_edit'),
    url(r'^category/delete/(?P<knowledgeCategory_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'category_delete', name='knowledge_category_delete'),
)
