# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Nuvius Connector template tags for Jinja
"""
from coffin import template
from jinja2 import contextfunction, Markup
from django.contrib.sites.models import RequestSite
from treeio.core.conf import settings

register = template.Library()

@contextfunction
def nuvius_profile_url(context, callback=None, next=None, source=None, services=None):
    "Returns profile URL for Nuvius auto-profile"
    
    nuvius_baseurl = getattr(settings, 'NUVIUS_URL', 'http://nuvius.com')
    
    url = nuvius_baseurl + '/profile/auto.json'
    suffix = ''
    if not source:
        source = getattr(settings, 'NUVIUS_SOURCE_ID', None)
    if source:
        suffix += "source=" + unicode(source)
    
    if not services:
        services = getattr(settings, 'NUVIUS_SERVICES', None)
    if services:
        if suffix:
            suffix += "&"
        suffix += "services=" + unicode(services)
    
    if not callback:
        callback = getattr(settings, 'NUVIUS_CALLBACK', None)
    if callback:
        if suffix:
            suffix += "&"
        suffix += "callback=" + unicode(callback)
    
    if not next:
        next = getattr(settings, 'NUVIUS_NEXT', None)
    if next:
        if suffix:
            suffix += "&"
        if not 'http' in next[:4]:
            site_name = RequestSite(context['request']).domain
            next = "http://" + site_name + "/" + next
        suffix += "next=" + unicode(next)
            
    if suffix:
        url += "?" + suffix

    return Markup(url)

register.object(nuvius_profile_url)

@contextfunction
def nuvius_base_url(context):
    "Returns profile URL for Nuvius auto-profile"
    
    baseurl = getattr(settings, 'NUVIUS_URL', 'http://www.nuvius.com')
    
    return Markup(baseurl)


register.object(nuvius_base_url)
