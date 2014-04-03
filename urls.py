# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Hardtree URLs
"""
from django.conf.urls import patterns, url, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()


def if_installed(appname, *args, **kwargs):
    ret = url(*args, **kwargs)
    if appname not in settings.INSTALLED_APPS:
        ret = url(r'^(\.(?P<response_format>\w+))?$',
                  'treeio.core.dashboard.views.index', name='home')
        #ret.resolve = lambda *args: None
    return ret

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(\.(?P<response_format>\w+))?$',
        'treeio.core.dashboard.views.index', name='home'),
    (r'^user/', include('treeio.core.urls')),
    (r'^accounts/', include('treeio.core.urls')),
    (r'^account/', include('treeio.account.urls')),
    (r'^search/', include('treeio.core.search.urls')),
    (r'^dashboard/', include('treeio.core.dashboard.urls')),
    (r'^admin/', include('treeio.core.administration.urls')),
    (r'^trash/', include('treeio.core.trash.urls')),
    (r'^documents/', include('treeio.documents.urls')),
    (r'^calendar/', include('treeio.events.urls')),
    (r'^finance/', include('treeio.finance.urls')),
    (r'^contacts/', include('treeio.identities.urls')),
    (r'^infrastructure/', include('treeio.infrastructure.urls')),
    (r'^knowledge/', include('treeio.knowledge.urls')),
    (r'^messaging/', include('treeio.messaging.urls')),
    (r'^news/', include('treeio.news.urls')),
    (r'^projects/', include('treeio.projects.urls')),
    (r'^sales/', include('treeio.sales.urls')),
    (r'^services/', include('treeio.services.urls')),
    (r'^reports/', include('treeio.reports.urls')),

    # API handlers
    (r'^api/', include('treeio.core.api.urls')),

    # Forest
    # if_installed('treeio.forest', r'^forest/', include('treeio.forest.urls')),

    # Mobile handler
    url(r'^m(?P<url>.+)?$', 'treeio.core.views.mobile_view',
        name='core_mobile_view'),

    # Help handler
    url(r'^help(?P<url>[a-zA-Z0-9-_/]+)?(\.(?P<response_format>\w+))?$',
        'treeio.core.views.help_page', name='core_help_page_view'),

    # Close iframe
    url(r'^iframe/?$', 'treeio.core.views.iframe_close',
        name='core_iframe_close'),

    # Captcha Config
    url(r'^captcha/', include('captcha.urls')),

    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),

    # Changed to backend (because it's backend!)
    (r'^backend/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.STATIC_DOC_ROOT}),
)


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
                            url(r'^rosetta/', include('rosetta.urls')),
                            )
urlpatterns += staticfiles_urlpatterns()
