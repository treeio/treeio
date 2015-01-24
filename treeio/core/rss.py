# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Global RSS Framework
"""
from django.contrib.syndication.views import Feed
from django.contrib.sites.models import RequestSite
from treeio.core.models import Object, UpdateRecord, User
import hashlib
import random


class ObjectFeed(Feed):

    "Generic RSS class"

    def __init__(self, title, link, description, objects, *args, **kwargs):
        self.title = title
        self.link = link
        self.description = description
        self.key = ''
        self.objects = objects
        super(ObjectFeed, self).__init__(*args, **kwargs)

    def __call__(self, request, *args, **kwargs):
        "Generates response"
        self.site_url = 'http://' + RequestSite(request).domain
        self.link = self.site_url + self.link
        response = super(ObjectFeed, self).__call__(request, *args, **kwargs)
        # Dirty hack for "example.com" - I hate it too but it works (contrast to all other solutions)
        # TODO: proper workaround for "example.com" in URLs
        # P.S. worship Ctulhu before you attempt this
        response.content = response.content.replace(
            'http://example.com', self.site_url)
        return response

    def get_object(self, request, *args, **kwargs):
        "Returns feed objects"
        return self.objects[:50]

    def items(self, obj):
        "Returns a single object"
        return obj

    def item_title(self, obj):
        "Returns object title"
        if isinstance(obj, Object):
            return obj.creator
        elif isinstance(obj, UpdateRecord):
            return obj.author

    def item_pubdate(self, obj):
        "Returns object's date_created"
        return obj.date_created

    def item_description(self, obj):
        "Returns object's body, details or full message"
        if isinstance(obj, Object):
            if obj.body:
                return obj.body
            else:
                return obj.details
        elif isinstance(obj, UpdateRecord):
            body = ''
            for object in obj.about.all():
                body += '<a href="' + self.site_url + \
                    object.get_absolute_url(
                    ) + '">' + unicode(object) + ' (' + object.get_human_type() + ')</a><br />'
            body += obj.get_full_message()
            return body

    def item_link(self, obj):
        "Returns object's full url"
        if isinstance(obj, Object):
            return self.site_url + obj.get_absolute_url()
        elif isinstance(obj, UpdateRecord):
            # link must be unique
            return self.link + '?' + str(random.random())


def verify_secret_key(request):
    "Verifies secret key for a request"
    if request.user.username:
        # always allow authenticated users
        return True
    else:
        key = request.GET['secret']
        user_id, secret = key.split('.', 1)
        try:
            profile = User.objects.get(pk=user_id)
        except:
            return False
        if key == get_secret_key(request, profile):
            request.user = profile.user
            return True
    return False


def get_secret_key(request, profile=None):
    "Generates secret key for a request in RSS format"
    if not profile:
        if request.user.username:
            profile = request.user.get_profile()
    if profile:
        params = request.GET.copy()
        if 'secret' in params:
            del params['secret']
        hash = hashlib.sha224()
        hash.update(unicode(params))
        hash.update(unicode(profile.id))
        hash.update(unicode(profile.user.date_joined))
        key = unicode(profile.id) + '.' + hash.hexdigest()
        return key
    return ''
