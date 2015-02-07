# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Messaging templatetags
"""
from coffin import template
from treeio.core.rendering import render_to_string
from jinja2 import contextfunction, Markup
from django.template import RequestContext
from treeio.core.models import Object
from treeio.messaging.models import Message

register = template.Library()


@contextfunction
def messaging_message_list(context, messages, skip_group=False, nomass=False):
    "Print a list of messages"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    profile = request.user.get_profile()

    return Markup(render_to_string('messaging/tags/message_list',
                                   {'messages': messages,
                                    'profile': profile,
                                    'skip_group': skip_group,
                                    'nomass': nomass},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(messaging_message_list)


@contextfunction
def messaging_unread(context):
    "Print a number of unread messages"

    request = context['request']

    user = None
    if request.user.username:
        try:
            user = request.user.get_profile()
        except Exception:
            pass

    unread = 0
    messaging = None
    if user:
        modules = user.get_perspective().get_modules()
        messaging = modules.filter(name='treeio.messaging')
        if messaging:
            unread = Object.filter_permitted(user,
                                             Message.objects.filter(reply_to__isnull=True).exclude(read_by=user)).count()

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('messaging/tags/unread',
                                   {'messaging': messaging, 'unread': unread},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(messaging_unread)
