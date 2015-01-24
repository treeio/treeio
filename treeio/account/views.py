# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core module views
"""

from treeio.core.rendering import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from treeio.account.forms import AccountForm, AccountPasswordForm, SettingsForm, MassActionForm
from treeio.core.decorators import treeio_login_required, handle_response_format
from treeio.core.models import ModuleSetting, Perspective
from treeio.account.models import NotificationSetting
from treeio.core.conf import settings
from jinja2 import Markup


@treeio_login_required
def account_view(request, response_format='html'):
    "Account view"

    profile = request.user.get_profile()
    try:
        contacts = profile.contact_set.exclude(trash=True)
    except:
        contacts = []

    return render_to_response('account/account_view',
                              {'profile': profile, 'contacts': contacts},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def watchlist(request, response_format='html'):
    "Displays all objects a User is subscribed to"

    profile = request.user.get_profile()
    watchlist = profile.subscriptions.all()

    context = {'profile': profile, 'watchlist': watchlist}

    return render_to_response('account/watchlist', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def account_edit(request, response_format='html'):
    "Account edit"

    profile = request.user.get_profile()
    if request.POST:
        form = AccountForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('account_view'))
    else:
        form = AccountForm(instance=profile)

    return render_to_response('account/account_edit',
                              {'profile': profile,
                                  'form': Markup(form.as_ul())},
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def account_password(request, response_format='html'):
    "Change password form"

    profile = request.user.get_profile()
    if request.POST:
        if not 'cancel' in request.POST:
            form = AccountPasswordForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('account_view'))
        else:
            return HttpResponseRedirect(reverse('account_view'))
    else:
        form = AccountPasswordForm(request.user)

    return render_to_response('account/account_password',
                              {'profile': profile,
                               'form': Markup(form.as_ul())},
                              context_instance=RequestContext(request), response_format=response_format)


#
# Settings
#
@treeio_login_required
def settings_view(request, response_format='html'):
    "Settings view"
    user = request.user.get_profile()

    # default permissions
    try:
        conf = ModuleSetting.get_for_module(
            'treeio.core', 'default_permissions', user=user)[0]
        default_permissions = conf.value
    except:
        default_permissions = settings.HARDTREE_DEFAULT_PERMISSIONS

    # default perspective
    try:
        conf = ModuleSetting.get_for_module(
            'treeio.core', 'default_perspective', user=user)[0]
        default_perspective = Perspective.objects.get(pk=long(conf.value))
    except:
        default_perspective = None

    # language
    language = getattr(settings, 'HARDTREE_LANGUAGES_DEFAULT', '')
    try:
        conf = ModuleSetting.get('language', user=user)[0]
        language = conf.value
    except IndexError:
        pass
    all_languages = getattr(
        settings, 'HARDTREE_LANGUAGES', [('en', 'English')])

    # time zone
    default_timezone = settings.HARDTREE_SERVER_DEFAULT_TIMEZONE
    try:
        conf = ModuleSetting.get('default_timezone')[0]
        default_timezone = conf.value
    except:
        pass

    try:
        conf = ModuleSetting.get('default_timezone', user=user)[0]
        default_timezone = conf.value
    except:
        default_timezone = getattr(
            settings, 'HARDTREE_SERVER_TIMEZONE')[default_timezone][0]

    all_timezones = getattr(settings, 'HARDTREE_SERVER_TIMEZONE')

    # email notifications e.g. new task assigned to you
    email_notifications = getattr(
        settings, 'HARDTREE_ALLOW_EMAIL_NOTIFICATIONS', False)
    try:
        conf = ModuleSetting.get('email_notifications', user=user)[0]
        email_notifications = conf.value
    except:
        pass

    try:
        ns = NotificationSetting.objects.get(owner=user, enabled=True)
        notifications_for_modules = [m.title for m in ns.modules.all()]
    except NotificationSetting.DoesNotExist:
        notifications_for_modules = []

    return render_to_response('account/settings_view',
                              {
                                  'default_permissions': default_permissions,
                                  'default_perspective': default_perspective,
                                  'language': language,
                                  'all_languages': all_languages,
                                  'default_timezone': default_timezone,
                                  'all_timezones': all_timezones,
                                  'email_notifications': email_notifications,
                                  'notifications_for_modules': notifications_for_modules,
                              },
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def settings_edit(request, response_format='html'):
    "Settings edit"

    if request.POST:
        if not 'cancel' in request.POST:
            form = SettingsForm(request.user.get_profile(), request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('account_settings_view'))
        else:
            return HttpResponseRedirect(reverse('account_settings_view'))
    else:
        form = SettingsForm(request.user.get_profile())

    return render_to_response('account/settings_edit',
                              {'form': Markup(form.as_ul())},
                              context_instance=RequestContext(request), response_format=response_format)

#
# Notification settings
#


def _process_mass_form(f):
    "Pre-process request to handle mass action form for NotificationSetting"

    def wrap(request, *args, **kwargs):
        "Wrap"
        user = request.user.get_profile()
        if 'massform' in request.POST:
            for key in request.POST:
                if 'mass-setting' in key:
                    try:
                        report = NotificationSetting.objects.get(pk=request.POST[key])
                        form = MassActionForm(
                            user, request.POST, instance=report)
                        if form.is_valid() and user.has_permission(report, mode='w'):
                            form.save()
                    except:
                        pass

        return f(request, *args, **kwargs)

    # can use functools.update_wrapper instead
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__

    return wrap
