# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core Account module URLs
"""

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('treeio.account.views',
                       url(r'^(\.(?P<response_format>\w+))?/?$',
                           'account_view', name='account'),
                       url(r'^view(\.(?P<response_format>\w+))?/?$',
                           'account_view', name='account_view'),
                       url(r'^password(\.(?P<response_format>\w+))?/?$',
                           'account_password', name='account_password'),
                       url(r'^watchlist(\.(?P<response_format>\w+))?/?$',
                           'watchlist', name='account_watchlist'),

                       # Settings
                       url(r'^settings(\.(?P<response_format>\w+))?/?$',
                           'settings_view', name='account_settings'),
                       url(r'^settings/view(\.(?P<response_format>\w+))?/?$',
                           'settings_view', name='account_settings_view'),
                       url(r'^settings/edit(\.(?P<response_format>\w+))?/?$',
                           'settings_edit', name='account_settings_edit'),
                       )
