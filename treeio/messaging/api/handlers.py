# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- coding: utf-8 -*-

from __future__ import absolute_import, with_statement

__all__ = ['MailingListHandler',
           'MessageStreamHandler',
           'MessageHandler',
           ]

import re
from treeio.core.api.utils import rc
from treeio.core.models import ModuleSetting
from django.core.exceptions import ObjectDoesNotExist
from treeio.identities.models import ContactType, Contact
from treeio.core.api.handlers import ObjectHandler, getOrNone
from treeio.messaging.models import Message, MessageStream, MailingList
from treeio.messaging.forms import MessageForm, MessageStreamForm, MessageReplyForm, MailingListForm


class MailingListHandler(ObjectHandler):

    "Entrypoint for MailingList model."

    model = MailingList
    form = MailingListForm

    fields = ('id',) + MailingListForm._meta.fields

    @staticmethod
    def resource_uri():
        return ('api_messaging_mlist', ['id'])

    def check_create_permission(self, request, mode):
        return True


class MessageStreamHandler(ObjectHandler):

    "Entrypoint for MessageStream model."

    model = MessageStream
    form = MessageStreamForm

    @staticmethod
    def resource_uri():
        return ('api_messaging_streams', ['id'])

    def check_create_permission(self, request, mode):
        return True


class MessageHandler(ObjectHandler):

    "Entrypoint for Message model."

    model = Message

    @staticmethod
    def resource_uri():
        return ('api_messaging_messages', ['id'])

    def create(self, request, *args, **kwargs):
        "Send email to some recipients"

        user = request.user.get_profile()

        if request.data is None:
            return rc.BAD_REQUEST

        if request.data.has_key('stream'):
            stream = getOrNone(MessageStream, request.data['stream'])
            if stream and not user.has_permission(stream, mode='x'):
                return rc.FORBIDDEN

        message = Message()
        message.author = user.get_contact()
        if not message.author:
            return rc.FORBIDDEN

        form = MessageForm(user, None, None, request.data, instance=message)
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
            return message
        else:
            self.status = 400
            return form.errors

    def update(self, request, *args, **kwargs):
        "Reply to message"

        if request.data is None:
            return rc.BAD_REQUEST

        pkfield = kwargs.get(self.model._meta.pk.name) or request.data.get(
            self.model._meta.pk.name)

        if not pkfield:
            return rc.BAD_REQUEST

        user = request.user.get_profile()

        try:
            message = self.model.objects.get(pk=pkfield)
        except ObjectDoesNotExist:
            return rc.NOT_FOUND

        if not user.has_permission(message):
            return rc.FORBIDDEN

        reply = Message()
        reply.author = user.get_contact()
        if not reply.author:
            return rc.FORBIDDEN

        reply.reply_to = message
        form = MessageReplyForm(
            user, message.stream_id, message, request.data, instance=reply)
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
            return reply

        else:
            self.status = 400
            return form.errors
