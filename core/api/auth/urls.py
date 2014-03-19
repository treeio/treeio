# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('treeio.core.api.auth.views',
    url(r'^get_request_token$', 'get_request_token',
        name="api_get_request_token"),
    url(r'^authorize_request_token$', 'authorize_request_token',
        name="api_authorize_request_token"),
    url(r'^get_access_token$', 'get_access_token',
        name="api_get_access_token"),
)
