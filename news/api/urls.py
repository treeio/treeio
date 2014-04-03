# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- coding: utf-8 -*-

import handlers
from django.conf.urls import patterns, url
from treeio.core.api.auth import auth_engine
from treeio.core.api.doc import documentation_view
from treeio.core.api.resource import CsrfExemptResource

ad = {'authentication': auth_engine}

# news resources
updateRecordsResource = CsrfExemptResource(
    handler=handlers.UpdateRecordHandler, **ad)


urlpatterns = patterns('',
    # News
    url(r'^doc$', documentation_view, kwargs={
        'module': handlers}, name="api_news_doc"),
    url(r'^records$', updateRecordsResource,
        name="api_news_update_records"),
    url(r'^record/(?P<record_id>\d+)', updateRecordsResource,
        name="api_news_update_records"),
)
