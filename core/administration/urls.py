# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core module Administration panel URLs
"""

from django.conf.urls import patterns, url

urlpatterns = patterns('treeio.core.administration.views',
    url(r'^(\.(?P<response_format>\w+))?$',
        'index_perspectives', name='core_admin'),

    # Perspectives
    url(r'^perspectives(\.(?P<response_format>\w+))?/?$',
        'index_perspectives', name='core_admin_index_perspectives'),
    url(r'^perspective/view/(?P<perspective_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'perspective_view', name='core_admin_perspective_view'),
    url(r'^perspective/edit/(?P<perspective_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'perspective_edit', name='core_admin_perspective_edit'),
    url(r'^perspective/delete/(?P<perspective_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'perspective_delete', name='core_admin_perspective_delete'),
    url(r'^perspective/add(\.(?P<response_format>\w+))?/?$',
        'perspective_add', name='core_admin_perspective_add'),

    # Modules
    url(r'^modules(\.(?P<response_format>\w+))?/?$',
        'index_modules', name='core_admin_index_modules'),
    url(r'^module/view/(?P<module_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'module_view', name='core_admin_module_view'),

    # Users
    url(r'^users(\.(?P<response_format>\w+))?/?$',
        'index_users', name='core_admin_index_users'),
    url(r'^user/view/(?P<user_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'user_view', name='core_admin_user_view'),
    url(r'^user/edit/(?P<user_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'user_edit', name='core_admin_user_edit'),
    url(r'^user/password/(?P<user_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'user_password', name='core_admin_user_password'),
    url(r'^user/delete/(?P<user_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'user_delete', name='core_admin_user_delete'),
    url(r'^user/add(\.(?P<response_format>\w+))?/?$',
        'user_add', name='core_admin_user_add'),
    url(r'^user/invite(\.(?P<response_format>\w+))?/?$',
        'user_invite', name='core_admin_user_invite'),

    url(r'^contact/setup(\.(?P<response_format>\w+))?/?$',
        'contact_setup', name='core_admin_contact_setup'),

    # Groups
    url(r'^groups(\.(?P<response_format>\w+))?/?$',
        'index_groups', name='core_admin_index_groups'),
    url(r'^group/view/(?P<group_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'group_view', name='core_admin_group_view'),
    url(r'^group/edit/(?P<group_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'group_edit', name='core_admin_group_edit'),
    url(r'^group/delete/(?P<group_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'group_delete', name='core_admin_group_delete'),
    url(r'^group/add(\.(?P<response_format>\w+))?/?$',
        'group_add', name='core_admin_group_add'),

    # Pages
    url(r'^pages(\.(?P<response_format>\w+))?/?$',
        'index_pages', name='core_admin_index_pages'),
    url(r'^page/add(\.(?P<response_format>\w+))?/?$',
        'page_add', name='core_admin_page_add'),
    url(r'^page/view/(?P<page_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'page_view', name='core_admin_page_view'),
    url(r'^page/edit/(?P<page_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'page_edit', name='core_admin_page_edit'),
    url(r'^page/delete/(?P<page_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'page_delete', name='core_admin_page_delete'),

    # Folders
    url(r'^folder/add(\.(?P<response_format>\w+))?/?$',
        'pagefolder_add', name='core_admin_pagefolder_add'),
    url(r'^folder/view/(?P<folder_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'pagefolder_view', name='core_admin_pagefolder_view'),
    url(r'^folder/edit/(?P<folder_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'pagefolder_edit', name='core_admin_pagefolder_edit'),
    url(r'^folder/delete/(?P<folder_id>\d+)(\.(?P<response_format>\w+))?/?$',
        'pagefolder_delete', name='core_admin_pagefolder_delete'),

    # Setup
    url(r'^setup(\.(?P<response_format>\w+))?/?$',
        'setup', name='core_setup'),

    # Settings
    url(r'^settings/edit(\.(?P<response_format>\w+))?/?$',
        'settings_edit', name='core_settings_edit'),
    url(r'^settings/view(\.(?P<response_format>\w+))?/?$',
        'settings_view', name='core_settings_view'),
)
