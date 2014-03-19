# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
User Account templatetags
"""
from coffin import template
from django.template import RequestContext
from jinja2 import contextfunction, Markup
from treeio.core.rendering import render_to_string

register = template.Library()


@contextfunction
def account_notification_count(context):
    "Account notification count"
    request = context['request']
    user = None
    if request.user.username:
        try:
            user = request.user.get_profile()
        except Exception:
            pass

    notifications = 0
    account = None
    if user:
        modules = user.get_perspective().get_modules()
        account = modules.filter(name='treeio.account')
        if account:
            notifications = user.notification_set.count()

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('account/tags/notification_count',
                  {'account': account, 'notifications': notifications},
                  response_format=response_format))

register.object(account_notification_count)


@contextfunction
def notification_setting_list(context, notification_settings, skip_group=False):
    "Print a list of settings"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('account/tags/notification_setting_list',
                                   {'settings': notification_settings,
                                       'skip_group': skip_group},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(notification_setting_list)
