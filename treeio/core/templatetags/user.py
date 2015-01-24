# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
User-related Core templatetags
"""
from coffin import template
from django.core.context_processors import csrf
from treeio.core.rendering import render_to_string
from jinja2 import contextfunction, Markup
from treeio.core.models import Object, Perspective
from treeio.core.conf import settings

register = template.Library()


@contextfunction
def user_block(context):
    "User block"
    request = context['request']
    user = None
    if request.user.username:
        try:
            user = request.user.get_profile()
        except Exception:
            pass

    modules = user.get_perspective().get_modules()

    account = modules.filter(name='treeio.account')

    admin = modules.filter(name='treeio.core')
    if admin:
        admin = admin[0]

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    trial = False
    if getattr(settings, 'HARDTREE_SUBSCRIPTION_USER_LIMIT') == 3:
        trial = True

    active = context.get('active', None)

    return Markup(render_to_string('core/tags/user_block',
                  {'user': user,
                   'account': account,
                   'admin': admin,
                   'active': active,
                   'trial': trial},
                  response_format=response_format))

register.object(user_block)


@contextfunction
def demo_user(context):
    "Print demo block if demo"

    response_format = 'html'

    demo = getattr(settings, 'HARDTREE_DEMO_MODE', False)

    return Markup(render_to_string('core/tags/demo_user',
                  {'demo': demo},
                  response_format=response_format))

register.object(demo_user)


@contextfunction
def core_perspective_switch(context):
    "Quick perspective switcher"

    response_format = 'html'
    request = context['request']
    try:
        user = request.user.get_profile()

        current = user.get_perspective()
        perspectives = Object.filter_by_request(request, Perspective.objects)
    except:
        current = None
        perspectives = []

    context = {'current': current, 'perspectives': perspectives}
    context.update(csrf(request))

    return Markup(render_to_string('core/tags/perspective_switch', context,
                  response_format=response_format))

register.object(core_perspective_switch)
