# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- coding: utf-8 -*-

import handlers
<<<<<<< HEAD:events/api/urls.py
from django.conf.urls import patterns, url
=======
from django.conf.urls import *
>>>>>>> 7eb75ad5a5164e5b47a5bca3851a1b508a1ecf26:treeio/events/api/urls.py
from treeio.core.api.auth import auth_engine
from treeio.core.api.doc import documentation_view
from treeio.core.api.resource import CsrfExemptResource

ad = {'authentication': auth_engine}

# events resources
eventResource = CsrfExemptResource(handler=handlers.EventHandler, **ad)


urlpatterns = patterns('',
    # Events
    url(r'^doc$', documentation_view, kwargs={
        'module': handlers}, name="api_events_doc"),
    url(r'^events$', eventResource, name="api_events"),
    url(r'^event/(?P<object_ptr>\d+)',
        eventResource, name="api_events"),
)
