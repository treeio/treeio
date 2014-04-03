# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- coding: utf-8 -*-

import handlers
from django.conf.urls.defaults import patterns, url
from treeio.core.api.auth import auth_engine
from treeio.core.api.doc import documentation_view
from treeio.core.api.resource import CsrfExemptResource

ad = {'authentication': auth_engine}

# admin resources
groupResource = CsrfExemptResource(handler=handlers.GroupHandler, **ad)
userResource = CsrfExemptResource(handler=handlers.UserHandler, **ad)
moduleResource = CsrfExemptResource(handler=handlers.ModuleHandler, **ad)
perspectiveResource = CsrfExemptResource(
    handler=handlers.PerspectiveHandler, **ad)
#folderResource = CsrfExemptResource(handler = handlers.PageFolderHandler, **ad)
#pageResource = CsrfExemptResource(handler = handlers.PageHandler, **ad)

urlpatterns = patterns('',
    # Resources
    url(r'^doc$', documentation_view, kwargs={
        'module': handlers}, name="api_admin_doc"),
    url(r'^groups$', groupResource,
        name="api_admin_groups"),
    url(r'^group/(?P<accessentity_ptr>\d+)',
        groupResource, name="api_admin_groups"),
    url(r'^users$', userResource, name="api_admin_users"),
    url(r'^user/(?P<accessentity_ptr>\d+)',
        userResource, name="api_admin_users"),
    url(r'^modules$', moduleResource,
        name="api_admin_modules"),
    url(r'^module/(?P<object_ptr>\d+)',
        moduleResource, name="api_admin_modules"),
    url(r'^perspectives$', perspectiveResource,
        name="api_admin_perspectives"),
    url(r'^perspective/(?P<object_ptr>\d+)',
        perspectiveResource, name="api_admin_perspectives"),
    #url(r'^folders$', folderResource, name="api_admin_folders"),
    #url(r'^folder/(?P<object_ptr>\d+)', folderResource, name="api_admin_folders"),
    #url(r'^pages$', pageResource, name="api_admin_pages"),
    #url(r'^page/(?P<object_ptr>\d+)', pageResource, name="api_admin_pages"),
)
