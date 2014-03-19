# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Messaging module views
"""
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.db.models import Q
from treeio.core.models import Object, ModuleSetting
from treeio.core.views import user_denied
from treeio.core.conf import settings
from treeio.core.rendering import render_to_response
from treeio.core.decorators import treeio_login_required, handle_response_format
from treeio.identities.models import ContactType, Contact
from treeio.messaging.models import Message, MessageStream, MailingList
from treeio.messaging.forms import MessageForm, MessageStreamForm, FilterForm, MassActionForm, SettingsForm, MessageReplyForm, MailingListForm
import re


def _get_filter_query(args):
    "Creates a query to filter Messages based on FilterForm arguments"
    query = Q()

    for arg in args:
        if hasattr(Message, arg) and args[arg]:
            kwargs = {str(arg + '__id'): long(args[arg])}
            query = query & Q(**kwargs)

    return query


def _get_default_context(request):
    "Returns default context as a dict()"
    streams = Object.filter_by_request(request, MessageStream.objects)
    mlists = MailingList.objects.all()
    massform = MassActionForm(request.user.get_profile())

    context = {'streams': streams,
               'mlists': mlists,
               'massform': massform}

    return context


def _process_mass_form(f):
    "Pre-process request to handle mass action form for Messages"

    def wrap(request, *args, **kwargs):
        "Wrap"
        user = request.user.get_profile()
        if 'massform' in request.POST:
            for key in request.POST:
                if 'mass-message' in key:
                    try:
                        message = Message.objects.get(pk=request.POST[key])
                        form = MassActionForm(
                            user, request.POST, instance=message)
                        if form.is_valid() and user.has_permission(message, mode='w'):
                            form.save()
                    except Exception:
                        pass
            try:
                form = MassActionForm(request.user.get_profile(), request.POST)
                if form.is_valid():
                    form.save()
            except Exception:
                pass

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__

    return wrap


@handle_response_format
@treeio_login_required
@_process_mass_form
def index(request, response_format='html'):
    "Messaging index page"

    query = Q(reply_to__isnull=True)
    if request.GET:
        query = query & _get_filter_query(request.GET)
        objects = Object.filter_by_request(
            request, Message.objects.filter(query))
    else:
        objects = Object.filter_by_request(
            request, Message.objects.filter(query))

    filters = FilterForm(request.user.get_profile(), 'title', request.GET)

    context = _get_default_context(request)
    context.update({'filters': filters,
                    'messages': objects})

    return render_to_response('messaging/index', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def index_sent(request, response_format='html'):
    "Sent messages index page"

    query = Q(reply_to__isnull=True) & Q(
        author=request.user.get_profile().get_contact())
    if request.GET:
        query = query & _get_filter_query(request.GET)
        objects = Object.filter_by_request(
            request, Message.objects.filter(query))
    else:
        objects = Object.filter_by_request(
            request, Message.objects.filter(query))

    filters = FilterForm(request.user.get_profile(), 'title', request.GET)

    context = _get_default_context(request)
    context.update({'filters': filters,
                    'messages': objects})

    return render_to_response('messaging/index_sent', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def index_inbox(request, response_format='html'):
    "Received messages index page"

    query = Q(reply_to__isnull=True) & ~Q(
        author=request.user.get_profile().get_contact())
    if request.GET:
        query = query & _get_filter_query(request.GET)
        objects = Object.filter_by_request(
            request, Message.objects.filter(query))
    else:
        objects = Object.filter_by_request(
            request, Message.objects.filter(query))

    filters = FilterForm(request.user.get_profile(), 'title', request.GET)
    context = _get_default_context(request)
    context.update({'filters': filters,
                    'messages': objects})

    return render_to_response('messaging/index_inbox', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def index_unread(request, response_format='html'):
    "Messaging unread page"

    user = request.user.get_profile()

    query = Q(reply_to__isnull=True) & ~Q(read_by=user)
    if request.GET:
        query = query & _get_filter_query(request.GET)
        objects = Object.filter_by_request(
            request, Message.objects.filter(query))
    else:
        objects = Object.filter_by_request(
            request, Message.objects.filter(query))

    filters = FilterForm(request.user.get_profile(), 'title', request.GET)

    context = _get_default_context(request)
    context.update({'filters': filters,
                    'messages': objects})

    return render_to_response('messaging/unread', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def stream_add(request, response_format='html'):
    "New message stream"
    user = request.user.get_profile()

    if request.POST:
        if not 'cancel' in request.POST:
            stream = MessageStream()
            form = MessageStreamForm(user, request.POST, instance=stream)
            if form.is_valid():
                stream = form.save()
                stream.set_user_from_request(request)
                return HttpResponseRedirect(reverse('messaging'))
        else:
            return HttpResponseRedirect(reverse('messaging'))
    else:
        form = MessageStreamForm(user)

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('messaging/stream_add', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def stream_view(request, stream_id, response_format='html'):
    "Stream view page"

    user = request.user.get_profile()

    stream = get_object_or_404(MessageStream, pk=stream_id)
    if not request.user.get_profile().has_permission(stream):
        return user_denied(request, message="You don't have access to this Stream",
                           response_format=response_format)

    if request.user.get_profile().has_permission(stream, mode='x'):
        if request.POST:
            message = Message()
            message.author = user.get_contact()
            if not message.author:
                return user_denied(request,
                                   message="You can't send message without a Contact Card assigned to you.",
                                   response_format=response_format)

            form = MessageForm(
                request.user.get_profile(), None, None, request.POST, instance=message)
            if form.is_valid():
                message = form.save()
                message.recipients.add(user.get_contact())
                message.set_user_from_request(request)
                message.read_by.add(user)
                try:
                    # if email entered create contact and add to recipients
                    if 'multicomplete_recipients' in request.POST and request.POST['multicomplete_recipients']:
                        try:
                            conf = ModuleSetting.get_for_module(
                                'treeio.messaging', 'default_contact_type')[0]
                            default_contact_type = ContactType.objects.get(
                                pk=long(conf.value))
                        except Exception:
                            default_contact_type = None
                        emails = request.POST[
                            'multicomplete_recipients'].split(',')
                        for email in emails:
                            emailstr = unicode(email).strip()
                            if re.match('[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+', emailstr):
                                contact, created = Contact.get_or_create_by_email(
                                    emailstr, contact_type=default_contact_type)
                                message.recipients.add(contact)
                                if created:
                                    contact.set_user_from_request(request)
                except:
                    pass
                # send email to all recipients
                message.send_email()

                return HttpResponseRedirect(reverse('messaging_stream_view', args=[stream.id]))
        else:
            form = MessageForm(request.user.get_profile(), stream_id)

    else:
        form = None

    objects = Object.filter_by_request(request, Message.objects.filter(
        reply_to__isnull=True, stream=stream).order_by('-date_created'))
    context = _get_default_context(request)
    context.update({'messages': objects,
                    'form': form,
                    'stream': stream})

    return render_to_response('messaging/stream_view', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def stream_edit(request, stream_id, response_format='html'):
    "Stream edit page"
    user = request.user.get_profile()

    stream = get_object_or_404(MessageStream, pk=stream_id)
    if not request.user.get_profile().has_permission(stream, mode="w"):
        return user_denied(request, message="You don't have access to this Stream",
                           response_format=response_format)

    if request.POST:
        if not 'cancel' in request.POST:
            form = MessageStreamForm(user, request.POST, instance=stream)
            if form.is_valid():
                stream = form.save()
                return HttpResponseRedirect(reverse('messaging_stream_view', args=[stream.id]))
        else:
            return HttpResponseRedirect(reverse('messaging_stream_view', args=[stream.id]))
    else:
        form = MessageStreamForm(user, instance=stream)

    context = _get_default_context(request)
    context.update({'form': form,
                    'stream': stream})

    return render_to_response('messaging/stream_edit', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def stream_checkmail(request, stream_id, response_format='html'):
    "Stream check mail"
    user = request.user.get_profile()

    stream = get_object_or_404(MessageStream, pk=stream_id)
    if not user.has_permission(stream):
        return user_denied(request, message="You don't have access to this Stream",
                           response_format=response_format)

    try:
        stream.process_email()
        messages.add_message(
            request, messages.INFO, _("E-mails fetched successfully."), fail_silently=True)
    except Exception, e:
        print e
        try:
            messages.add_message(request, messages.ERROR, _(
                "Failed to retrieve messages for this stream. Please check stream settings"), fail_silently=True)
        except:
            pass

    return HttpResponseRedirect(reverse('messaging_stream_view', args=[stream.id]))


@handle_response_format
@treeio_login_required
def stream_delete(request, stream_id, response_format='html'):
    "Delete stream page"

    stream = get_object_or_404(MessageStream, pk=stream_id)
    if not request.user.get_profile().has_permission(stream, mode="w"):
        return user_denied(request, message="You don't have access to this Stream",
                           response_format=response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                stream.trash = True
                stream.save()
            else:
                stream.delete()
            return HttpResponseRedirect('/messaging/')
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('messaging_stream_view', args=[stream.id]))

    context = _get_default_context(request)
    context.update({'stream': stream})

    return render_to_response('messaging/stream_delete', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def messaging_compose(request, response_format='html'):
    "New message page"

    user = request.user.get_profile()

    if request.POST:
        if not 'cancel' in request.POST:
            message = Message()
            message.author = user.get_contact()
            if not message.author:
                return user_denied(request,
                                   message="You can't send message without a Contact Card assigned to you.",
                                   response_format=response_format)

            form = MessageForm(
                request.user.get_profile(), None, None, request.POST, instance=message)
            if form.is_valid():
                message = form.save()
                message.recipients.add(user.get_contact())
                message.set_user_from_request(request)
                message.read_by.add(user)
                try:
                    # if email entered create contact and add to recipients
                    if 'multicomplete_recipients' in request.POST and request.POST['multicomplete_recipients']:
                        try:
                            conf = ModuleSetting.get_for_module(
                                'treeio.messaging', 'default_contact_type')[0]
                            default_contact_type = ContactType.objects.get(
                                pk=long(conf.value))
                        except Exception:
                            default_contact_type = None
                        emails = request.POST[
                            'multicomplete_recipients'].split(',')
                        for email in emails:
                            emailstr = unicode(email).strip()
                            if re.match('[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+', emailstr):
                                contact, created = Contact.get_or_create_by_email(
                                    emailstr, contact_type=default_contact_type)
                                message.recipients.add(contact)
                                if created:
                                    contact.set_user_from_request(request)
                except:
                    pass
                # send email to all recipients
                message.send_email()

                return HttpResponseRedirect(reverse('messaging'))
        else:
            return HttpResponseRedirect(reverse('messaging'))

    else:
        form = MessageForm(request.user.get_profile(), None)

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('messaging/message_compose', context,
                              context_instance=RequestContext(request), response_format=response_format)


@handle_response_format
@treeio_login_required
def messaging_view(request, message_id, response_format='html'):
    "Single message page"

    message = get_object_or_404(Message, pk=message_id)
    user = request.user.get_profile()

    if not user.has_permission(message):
        return user_denied(request, message="You don't have access to this Message",
                           response_format=response_format)

    message.read_by.add(user)

    if request.POST and request.POST.get('body', False):
        "Unread message"

        reply = Message()
        reply.author = user.get_contact()
        if not reply.author:
            return user_denied(request,
                               message="You can't send message without a Contact Card assigned to you.",
                               response_format=response_format)
        reply.reply_to = message
        form = MessageReplyForm(
            user, message.stream_id, message, request.POST, instance=reply)
        if form.is_valid():
            reply = form.save()
            reply.set_user_from_request(request)
            # Add author to recipients
            reply.recipients.add(reply.author)
            message.read_by.clear()

            try:
                # if email entered create contact and add to recipients
                if 'multicomplete_recipients' in request.POST and request.POST['multicomplete_recipients']:
                    try:
                        conf = ModuleSetting.get_for_module(
                            'treeio.messaging', 'default_contact_type')[0]
                        default_contact_type = ContactType.objects.get(
                            pk=long(conf.value))
                    except Exception:
                        default_contact_type = None
                    emails = request.POST[
                        'multicomplete_recipients'].split(',')
                    for email in emails:
                        emailstr = unicode(email).strip()
                        if re.match('[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+', emailstr):
                            contact, created = Contact.get_or_create_by_email(
                                emailstr, contact_type=default_contact_type)
                            reply.recipients.add(contact)
                            if created:
                                contact.set_user_from_request(request)
            except:
                pass

            # Add each recipient of the reply to the original message
            for recipient in reply.recipients.all():
                message.recipients.add(recipient)

            # send email to all recipients
            reply.send_email()

            return HttpResponseRedirect(reverse('messaging_message_view', args=[message.id]))

    else:
        form = MessageReplyForm(
            request.user.get_profile(), message.stream_id, message)

    replies = Object.filter_by_request(request,
                                       Message.objects.filter(reply_to=message).order_by('date_created'))

    context = _get_default_context(request)
    context.update({'message': message,
                    'messages': replies,
                    'form': form})

    return render_to_response('messaging/message_view', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def messaging_delete(request, message_id, response_format='html'):
    "Delete message page"

    message = get_object_or_404(Message, pk=message_id)

    if not request.user.get_profile().has_permission(message, mode="w"):
        return user_denied(request, message="You don't have access to this Message",
                           response_format=response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                message.trash = True
                message.save()
            else:
                message.delete()
            return HttpResponseRedirect('/messaging/')
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('messaging_stream_view', args=[message.stream.id]))

    context = _get_default_context(request)
    context.update({'message': message})

    return render_to_response('messaging/message_delete', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)

"""
Mailing Lists
"""


@handle_response_format
@treeio_login_required
def mlist_add(request, response_format='html'):
    "New message mlist"
    user = request.user.get_profile()

    if request.POST:

        mlist = MailingList()

        form = MailingListForm(user, request.POST, instance=mlist)
        if form.is_valid():
            mlist = form.save()
            mlist.set_user_from_request(request)
            return HttpResponseRedirect('/messaging/')
    else:
        form = MailingListForm(user)

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('messaging/mlist_add', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def mlist_view(request, mlist_id, response_format='html'):
    "Mailing List view page"

    user = request.user.get_profile()

    mlist = get_object_or_404(MailingList, pk=mlist_id)
    if not request.user.get_profile().has_permission(mlist):
        return user_denied(request, message="You don't have access to this Mailing List",
                           response_format=response_format)

    if request.user.get_profile().has_permission(mlist, mode='x'):
        if request.POST:
            message = Message()
            message.author = request.user.get_profile().get_contact()
            if not message.author:
                return user_denied(request,
                                   message="You can't send message without a Contact Card assigned to you.",
                                   response_format=response_format)
            form = MessageForm(
                request.user.get_profile(), mlist_id, None, request.POST, instance=message)
            if form.is_valid():
                message = form.save()
                message.set_user_from_request(request)
                message.read_by.add(user)
                return HttpResponseRedirect(reverse('messaging_mlist_view', args=[mlist.id]))
        else:
            form = MessageForm(request.user.get_profile(), mlist_id)

    else:
        form = None

    messages = Object.filter_by_request(request,
                                        Message.objects.filter(reply_to__isnull=True,
                                                               mlist=mlist).order_by('-date_created'))
    context = _get_default_context(request)
    context.update({'messages': messages,
                    'form': form,
                    'mlist': mlist})

    return render_to_response('messaging/mlist_view', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def mlist_edit(request, mlist_id, response_format='html'):
    "MailingList edit page"
    user = request.user.get_profile()

    mlist = get_object_or_404(MailingList, pk=mlist_id)
    if not user.has_permission(mlist, mode="w"):
        return user_denied(request, message="You don't have access to this Mailing List",
                           response_format=response_format)

    context = _get_default_context(request)
    context.update({'mlist': mlist})

    return render_to_response('messaging/mlist_edit', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def mlist_delete(request, mlist_id, response_format='html'):
    "Delete mlist page"

    mlist = get_object_or_404(MailingList, pk=mlist_id)
    if not request.user.get_profile().has_permission(mlist, mode="w"):
        return user_denied(request, message="You don't have access to this Mailing List",
                           response_format=response_format)

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                mlist.trash = True
                mlist.save()
            else:
                mlist.delete()
            return HttpResponseRedirect('/messaging/')
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('messaging_mlist_view', args=[mlist.id]))

    context = _get_default_context(request)
    context.update({'mlist': mlist})

    return render_to_response('messaging/mlist_delete', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


"""
Settings
"""


@handle_response_format
@treeio_login_required
def settings_view(request, response_format='html'):
    "Settings admin view"

    # default content type
    try:
        conf = ModuleSetting.get_for_module('treeio.messaging', 'default_contact_type',
                                            user=request.user.get_profile())[0]
        default_contact_type = ContactType.objects.get(pk=long(conf.value))
    except:
        default_contact_type = None

    # default imap folder
    try:
        conf = ModuleSetting.get_for_module(
            'treeio.messaging', 'default_imap_folder')[0]
        default_imap_folder = conf.value
    except:
        default_imap_folder = getattr(
            settings, 'HARDTREE_MESSAGING_IMAP_DEFAULT_FOLDER_NAME', 'UNSEEN')

    # signature
    try:
        conf = ModuleSetting.get_for_module('treeio.messaging', 'signature',
                                            user=request.user.get_profile(), strict=True)[0]
        signature = conf.value
    except:
        signature = ''

    types = Object.filter_by_request(
        request, ContactType.objects.order_by('name'))

    context = _get_default_context(request)
    context.update({'types': types,
                    'signature': signature,
                    'default_contact_type': default_contact_type,
                    'default_imap_folder': default_imap_folder})

    return render_to_response('messaging/settings_view', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def settings_edit(request, response_format='html'):
    "Settings admin view"

    if request.POST:
        if not 'cancel' in request.POST:
            form = SettingsForm(request.user.get_profile(), request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('messaging_settings_view'))
        else:
            return HttpResponseRedirect(reverse('messaging_settings_view'))
    else:
        form = SettingsForm(request.user.get_profile())

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('messaging/settings_edit', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


#
# Widgets
#

@treeio_login_required
def widget_new_messages(request, response_format='html'):
    "A list of new messages. Limit by 5."

    query = Q(reply_to__isnull=True) & ~Q(read_by=request.user.get_profile())

    messages = Object.filter_by_request(
        request, Message.objects.filter(query))[:5]

    return render_to_response('messaging/widgets/new_messages',
                              {'messages': messages},
                              context_instance=RequestContext(request), response_format=response_format)
