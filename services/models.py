# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
ServiceSupport module objects.

Depends on: treeio.core, treeio.identities
"""

from django.core.urlresolvers import reverse
from django.db.models import signals
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.html import strip_tags
from treeio.core.conf import settings
from treeio.identities.models import Contact
from treeio.core.models import User, Object, ModuleSetting, UpdateRecord
from treeio.core.mail import BaseEmail
from treeio.core.rendering import render_to_string, render_string_template
from treeio.messaging.models import Message, MessageStream


class TicketStatus(Object):

    "State information about a ticket"
    name = models.CharField(max_length=256)
    details = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    hidden = models.BooleanField(default=False)

    searchable = False

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        return reverse('services_status_view', args=[self.id])

    class Meta:

        "TicketStatus"
        ordering = ('hidden', '-active', 'name')


class Service(Object):

    "Technical service supported by a company"
    name = models.CharField(max_length=256)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='child_set')
    details = models.TextField(blank=True, null=True)

    access_inherit = ('parent', '*module', '*user')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        try:
            return reverse('services_service_view', args=[self.id])
        except Exception:
            return ""

    class Meta:

        "Service"
        ordering = ['name']


class ServiceLevelAgreement(Object):

    "Formal terms for service support"
    name = models.CharField(max_length=256)
    service = models.ForeignKey(Service)
    default = models.BooleanField(default=False)
    response_time = models.PositiveIntegerField(blank=True, null=True)
    uptime_rate = models.FloatField(blank=True, null=True)
    available_from = models.TimeField(blank=True, null=True)
    available_to = models.TimeField(blank=True, null=True)
    client = models.ForeignKey(
        Contact, related_name="client_sla", blank=True, null=True)
    provider = models.ForeignKey(Contact, related_name="provider_sla")

    access_inherit = ('service', '*module', '*user')

    class Meta:

        "SLA"
        ordering = ('name', 'client')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        try:
            return reverse('services_sla_view', args=[self.id])
        except Exception:
            return ""


class ServiceAgent(Object):

    "User responsible for service support"
    related_user = models.ForeignKey(User)
    active = models.BooleanField(default=True)
    occupied = models.BooleanField(default=False)
    available_from = models.TimeField(blank=True, null=True)
    available_to = models.TimeField(blank=True, null=True)

    class Meta:

        "ServiceAgent"
        ordering = ('related_user', '-active', 'occupied')

    def __unicode__(self):
        return unicode(self.related_user)

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        try:
            return reverse('services_agent_view', args=[self.id])
        except Exception:
            return ""


class TicketQueue(Object):

    "Queue for incoming tickets"
    name = models.CharField(max_length=256)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='child_set')
    default_ticket_status = models.ForeignKey(
        TicketStatus, blank=True, null=True, on_delete=models.SET_NULL)
    default_ticket_priority = models.IntegerField(default=3,
                                                  choices=((5, 'Highest'), (4, 'High'), (3, 'Normal'),
                                                           (2, 'Low'), (1, 'Lowest')))
    default_service = models.ForeignKey(
        Service, blank=True, null=True, on_delete=models.SET_NULL)
    waiting_time = models.PositiveIntegerField(blank=True, null=True)
    next_queue = models.ForeignKey(
        'self', blank=True, null=True, related_name='previous_set', on_delete=models.SET_NULL)
    ticket_code = models.CharField(
        max_length=8, blank=True, null=True, default='')
    message_stream = models.ForeignKey(
        MessageStream, blank=True, null=True, on_delete=models.SET_NULL)  # Messaging integration
    details = models.TextField(blank=True, null=True)

    class Meta:

        "TicketQueue"
        ordering = ('name', '-active', 'ticket_code')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        try:
            return reverse('services_queue_view', args=[self.id])
        except Exception:
            return ""


class Ticket(Object):

    "Problem or support request ticket"
    reference = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    caller = models.ForeignKey(
        Contact, blank=True, null=True, on_delete=models.SET_NULL)
    urgency = models.IntegerField(default=3,
                                  choices=((5, _('Highest')), (4, _('High')), (3, _('Normal')), (2, _('Low')),
                                           (1, _('Lowest'))))
    priority = models.IntegerField(default=3,
                                   choices=((5, _('Highest')), (4, _('High')), (3, _('Normal')), (2, _('Low')),
                                            (1, _('Lowest'))))
    status = models.ForeignKey(TicketStatus)
    service = models.ForeignKey(
        Service, blank=True, null=True, on_delete=models.SET_NULL)
    sla = models.ForeignKey(
        ServiceLevelAgreement, blank=True, null=True, on_delete=models.SET_NULL)
    queue = models.ForeignKey(TicketQueue, blank=True, null=True)
    assigned = models.ManyToManyField(ServiceAgent, blank=True, null=True)
    message = models.ForeignKey(
        Message, blank=True, null=True, on_delete=models.SET_NULL)  # Messaging integration
    details = models.TextField(blank=True, null=True)
    resolution = models.TextField(blank=True, null=True)

    #access_inherit = ('queue', '*module', '*user')

    class Meta:

        "Ticket"
        ordering = ('-priority', 'reference')

    def __unicode__(self):
        return self.name

    def priority_human(self):
        "Returns a Human-friendly priority name"
        choices = ((5, _('Highest')), (4, _('High')), (
            3, _('Normal')), (2, _('Low')), (1, _('Lowest')))
        for choice in choices:
            if choice[0] == self.priority:
                return choice[1]

    def urgency_human(self):
        "Returns a Human-friendly urgency name"
        choices = ((5, _('Highest')), (4, _('High')), (
            3, _('Normal')), (2, _('Low')), (1, _('Lowest')))
        for choice in choices:
            if choice[0] == self.priority:
                return choice[1]

    def save(self, *args, **kwargs):
        "Automatically set ticket reference and send message to caller"
        super(Ticket, self).save(*args, **kwargs)

        if not self.reference:
            if self.queue:
                self.reference = self.queue.ticket_code + str(self.id)
            else:
                self.reference = str(self.id)
            self.save()

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        try:
            return reverse('services_ticket_view', args=[self.id])
        except Exception:
            return ""


class TicketRecord(UpdateRecord):

    "Update for a Ticket"
    # Messaging integration
    message = models.ForeignKey(Message, blank=True, null=True)
    notify = models.BooleanField(default=False, blank=True)


"""
Service Support signals
"""


def email_caller_on_new_ticket(sender, instance, created, **kwargs):
    "When a new ticket is created send an email to the caller"
    if created:
        send_email_to_caller = False
        try:
            conf = ModuleSetting.get_for_module(
                'treeio.services', 'send_email_to_caller')[0]
            send_email_to_caller = conf.value
        except:
            send_email_to_caller = getattr(
                settings, 'HARDTREE_SEND_EMAIL_TO_CALLER', True)

        if send_email_to_caller:
            # don't send email to yourself
            creator_contact = None
            if instance.creator:
                creator_contact = instance.creator.get_contact()

            if instance.caller and instance.caller != creator_contact:
                if not instance.reference:
                    if instance.queue:
                        instance.reference = instance.queue.ticket_code + \
                            str(instance.id)
                    else:
                        instance.reference = str(instance.id)
                    instance.save()
                subject = "[#%s] %s" % (instance.reference, instance.name)

                # Construct context and render to html, body
                context = {'ticket': instance}
                try:
                    conf = ModuleSetting.get_for_module(
                        'treeio.services', 'send_email_template')[0]
                    send_email_template = conf.value
                    html = render_string_template(send_email_template, context)
                except:
                    html = render_to_string(
                        'services/emails/notify_caller', context, response_format='html')
                body = strip_tags(html)

                if instance.queue and instance.queue.message_stream:
                    stream = instance.queue.message_stream
                    if stream.outgoing_server_name:
                        try:
                            caller_email = instance.caller.get_email()
                            if caller_email:
                                toaddr = caller_email
                                ssl = False
                                if stream.outgoing_server_type == 'SMTP-SSL':
                                    ssl = True
                                email = BaseEmail(stream.outgoing_server_name,
                                                  stream.outgoing_server_username,
                                                  stream.outgoing_password,
                                                  stream.outgoing_email,
                                                  toaddr, subject, body, html=html,
                                                  ssl=ssl)
                                email.process_email()
                        except:
                            pass

signals.post_save.connect(email_caller_on_new_ticket, sender=Ticket)


def create_ticket_from_message(sender, instance, created, **kwargs):
    """
    Get a signal from messaging.models
    Check if (new) message's stream is also assigned to Ticket Queue
    Create a new ticket from that message
    Rename original message title
    """

    if created and getattr(instance, 'auto_notify', True):
        if instance.reply_to:
            tickets = instance.reply_to.ticket_set.all()
            for ticket in tickets:
                record = TicketRecord()
                record.sender = instance.author
                record.record_type = 'manual'
                record.body = instance.body
                record.save()
                record.about.add(ticket)
                ticket.set_last_updated()
        else:
            stream = instance.stream
            queues = TicketQueue.objects.filter(message_stream=stream)
            if stream and queues:
                queue = queues[0]
                ticket = Ticket()
                try:
                    conf = ModuleSetting.get_for_module(
                        'treeio.services', 'default_ticket_status')[0]
                    ticket.status = TicketStatus.objects.get(
                        pk=long(conf.value))
                except:
                    statuses = TicketStatus.objects.all()
                    ticket.status = statuses[0]
                ticket.queue = queue
                ticket.caller = instance.author
                ticket.details = instance.body
                ticket.message = instance
                ticket.name = instance.title
                ticket.auto_notify = False
                ticket.save()
                try:
                    if stream.creator:
                        ticket.set_user(stream.creator)
                    elif queue.creator:
                        ticket.set_user(queue.creator)
                    else:
                        ticket.copy_permissions(queue)
                except:
                    pass

                # Rename original message title
                instance.title = "[#" + ticket.reference + "] " + \
                    instance.title
                instance.save()

signals.post_save.connect(create_ticket_from_message, sender=Message)
