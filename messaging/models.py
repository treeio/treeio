# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Messaging models
"""
from django.db import models
from treeio.core.models import User, Object
from treeio.identities.models import Contact, ContactValue
from treeio.messaging.emails import EmailStream, EmailMessage
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from jinja2.filters import do_striptags
from treeio.core.templatetags.modules import htsafe
import re

#
# Mailing Lists
#


class Template(Object):

    "A template for sending emails using template tags"
    name = models.CharField(max_length=255)
    body = models.TextField()
    subject = models.CharField(max_length=255)


class MailingList(Object):

    "A mailling list for mass mailing"
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    from_contact = models.ForeignKey(Contact, related_name="from_contact_set")
    opt_in = models.ForeignKey(Template, blank=True, null=True)
    members = models.ManyToManyField(
        Contact, blank=True, null=True, related_name="members_set")

    class Meta:

        "Message"
        ordering = ['-date_created']

    def __unicode__(self):
        return self.name


# TODO: Add segment and urltrack models


# MessageStream Model
class MessageStream(Object):
    """
    A Stream that contains a list of messages
    """
    name = models.CharField(max_length=255)

    incoming_server_name = models.CharField(
        max_length=255, null=True, blank=True)
    incoming_server_type = models.CharField(max_length=255, null=True, blank=True,
                                            choices=(('POP3', 'POP3'),
                                                     ('POP3-SSL', 'POP3-SSL'),
                                                     ('IMAP', 'IMAP'),
                                                     ('IMAP-SSL', 'IMAP-SSL'),))
    incoming_server_username = models.CharField(
        max_length=255, null=True, blank=True)
    incoming_password = models.CharField(max_length=255, null=True, blank=True)

    outgoing_email = models.EmailField(max_length=255, null=True, blank=True)
    outgoing_server_name = models.CharField(
        max_length=255, null=True, blank=True)
    outgoing_server_type = models.CharField(max_length=255, null=True, blank=True,
                                            choices=(("SMTP", "SMTP"),
                                                     ("SMTP-SSL", "SMTP-SSL")))
    outgoing_server_username = models.CharField(
        max_length=255, null=True, blank=True)
    outgoing_password = models.CharField(max_length=255, null=True, blank=True)

    faulty = models.BooleanField(default=False)
    last_checked = models.DateTimeField(null=True, blank=True)

    class Meta:

        "MessageStream"
        ordering = ['name', 'last_updated']
        verbose_name = _("Stream")
        verbose_name_plural = _("Streams")

    def __unicode__(self):
        return self.name

    def process_email(self):
        "Get email from the email box"
        email = EmailStream(self)
        email.get_emails()

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        try:
            return reverse('messaging_stream_view', args=[self.id])
        except Exception:
            return ""


class Message(Object):
    """
    A Single Message
    """
    title = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField()
    author = models.ForeignKey(Contact)
    recipients = models.ManyToManyField(
        Contact, null=True, blank=True, related_name='message_recipients')
    stream = models.ForeignKey(
        MessageStream, blank=True, null=True, related_name='stream', on_delete=models.SET_NULL)
    reply_to = models.ForeignKey(
        'self', blank=True, null=True, related_name='child_set')
    read_by = models.ManyToManyField(
        User, null=True, blank=True, related_name='read_by_user')
    mlist = models.ForeignKey(
        MailingList, blank=True, null=True, related_name='mlist')

    access_inherit = ('stream', '*module', '*user')

    class Meta:
        "Message"
        ordering = ['-date_created']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        try:
            return reverse('messaging_message_view', args=[self.id])
        except Exception:
            return ""

    def save(self, *args, **kwargs):
        "Automatically set message title"

        if not self.title:
            self.title = self.body
            self.title = re.split('<[^>]+?>', self.title)
            self.title = ''.join(self.title)
            self.title = self.title[:50]

        super(Message, self).save(*args, **kwargs)

    def is_read(self, user):
        "Checks if the message is read by the given user"
        if not isinstance(user, User):
            raise TypeError("The given user is not an instance of core.User")
        return self.read_by.filter(pk=user.id).exists()

    def get_stripped_body(self):
        "Returns body without HTML tags and other shit"
        return do_striptags(htsafe(self.body)).replace(u"\u00A0", " ")

    def send_email(self):
        "Send email"
        email = EmailMessage(self)
        if self.stream and self.stream.outgoing_server_name:
            email.send_email()

    def get_original_message_author_email(self):
        "Returns email of the original message author"
        message = self.message
        contact = message.author

        email = ContactValue.objects.filter(
            field__field_type='email', contact=contact)
        if email:
            email = email[0]

        return email
