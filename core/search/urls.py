# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core Search module URLs
"""

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('treeio.core.search.views',
                       url(r'^(\.(?P<response_format>\w+))?/?$',
                           'search_query', name='core_search_query'),
                       )
