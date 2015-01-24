# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

<<<<<<< HEAD:core/api/auth/urls.py
from django.conf.urls.defaults import patterns, url
=======
from django.conf.urls import *
>>>>>>> 7eb75ad5a5164e5b47a5bca3851a1b508a1ecf26:treeio/core/api/auth/urls.py


urlpatterns = patterns('treeio.core.api.auth.views',
    url(r'^get_request_token$', 'get_request_token',
        name="api_get_request_token"),
    url(r'^authorize_request_token$', 'authorize_request_token',
        name="api_authorize_request_token"),
    url(r'^get_access_token$', 'get_access_token',
        name="api_get_access_token"),
)
