# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Nuvius Connector URLs
"""
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('nuconnector.views',
        
        # Check that the submitted profile id/key pair is valid
        url(r'^profile/check/?$', 'profile_check', name='nuvius_profile_check'),
        
        # Reset nuvius_profile for the current user
        url(r'^profile/reset(\.(?P<response_format>\w+))?/?$', 'profile_reset', name='nuvius_profile_reset'),
        
)
