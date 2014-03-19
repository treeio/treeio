# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Services module forms
"""
from django import forms
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from treeio.core.conf import settings
from treeio.identities.models import Contact
from treeio.core.decorators import preprocess_form
from treeio.core.models import Object, ModuleSetting
from treeio.core.rendering import get_template_source
from treeio.messaging.models import Message
from treeio.messaging.emails import EmailMessage
from treeio.services.models import Ticket, TicketRecord, ServiceAgent, TicketStatus, Service
from treeio.services.models import ServiceLevelAgreement, TicketQueue

preprocess_form()


class SettingsForm(forms.Form):

    """ Administration settings form """

    default_ticket_status = forms.ModelChoiceField(
        label='Default Ticket Status', queryset=[])
    default_ticket_queue = forms.ModelChoiceField(
        label='Default Queue', queryset=[])
    send_email_to_caller = forms.ChoiceField(label="Notify Caller By E-mail", choices=((True, _('Yes')),
                                                                                       (False, _('No'))), required=False)
    send_email_template = forms.CharField(
        label="E-mail Template", widget=forms.Textarea, required=False)

    def __init__(self, user, *args, **kwargs):
        "Sets choices and initial value"
        super(SettingsForm, self).__init__(*args, **kwargs)

        # Translate
        self.fields['default_ticket_status'].label = _('Default Ticket Status')
        self.fields['default_ticket_queue'].label = _('Default Queue')
        self.fields['send_email_to_caller'].label = _(
            "Notify Caller By E-mail")
        self.fields['send_email_template'].label = _("E-mail Template")

        self.fields['default_ticket_status'].queryset = Object.filter_permitted(
            user, TicketStatus.objects, mode='x')
        self.fields['default_ticket_queue'].queryset = Object.filter_permitted(
            user, TicketQueue.objects, mode='x')

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.services', 'default_ticket_status')[0]
            default_ticket_status = TicketStatus.objects.get(
                pk=long(conf.value))
            self.fields[
                'default_ticket_status'].initial = default_ticket_status.id
        except Exception:
            pass

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.services', 'default_ticket_queue')[0]
            default_ticket_queue = TicketQueue.objects.get(pk=long(conf.value))
            self.fields[
                'default_ticket_queue'].initial = default_ticket_queue.id
        except Exception:
            pass

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.services', 'send_email_to_caller')[0]
            self.fields['send_email_to_caller'].initial = conf.value
        except:
            self.fields[
                'send_email_to_caller'].initial = settings.HARDTREE_SEND_EMAIL_TO_CALLER

        # notification template
        try:
            conf = ModuleSetting.get_for_module(
                'treeio.services', 'send_email_template')[0]
            self.fields['send_email_template'].initial = conf.value
        except Exception:
            self.fields['send_email_template'].initial = get_template_source(
                'services/emails/notify_caller.html')

    def save(self):
        "Form processor"
        try:
            ModuleSetting.set_for_module('default_ticket_status',
                                         self.cleaned_data[
                                             'default_ticket_status'].id,
                                         'treeio.services')
            ModuleSetting.set_for_module('default_ticket_queue',
                                         self.cleaned_data[
                                             'default_ticket_queue'].id,
                                         'treeio.services')
            ModuleSetting.set_for_module('send_email_to_caller',
                                         self.cleaned_data[
                                             'send_email_to_caller'],
                                         'treeio.services')
            ModuleSetting.set_for_module('send_email_template',
                                         self.cleaned_data[
                                             'send_email_template'],
                                         'treeio.services')
            return True

        except Exception:
            return False


class MassActionForm(forms.Form):

    """ Mass action form for Tickets """

    status = forms.ModelChoiceField(queryset=[], required=False)
    service = forms.ModelChoiceField(queryset=[], required=False)
    queue = forms.ModelChoiceField(queryset=[], required=False)
    delete = forms.ChoiceField(label=_("Delete"), choices=(('', '-----'), ('delete', _('Delete Completely')),
                                                           ('trash', _('Move to Trash'))), required=False)
    instance = None

    def __init__(self, user, *args, **kwargs):
        "Sets allowed values"
        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            del kwargs['instance']

        super(MassActionForm, self).__init__(*args, **kwargs)

        self.fields['status'].queryset = Object.filter_permitted(
            user, TicketStatus.objects, mode='x')
        self.fields['status'].label = _("Status")
        self.fields['service'].queryset = Object.filter_permitted(
            user, Service.objects, mode='x')
        self.fields['service'].label = _("Service")
        self.fields['queue'].queryset = Object.filter_permitted(
            user, TicketQueue.objects, mode='x')
        self.fields['queue'].label = _("Queue")
        self.fields['delete'] = forms.ChoiceField(label=_("Delete"), choices=(('', '-----'),
                                                                              ('delete', _(
                                                                                  'Delete Completely')),
                                                                              ('trash', _('Move to Trash'))), required=False)

    def save(self, *args, **kwargs):
        "Process form"
        if self.instance:
            if self.is_valid():
                if self.cleaned_data['service']:
                    self.instance.service = self.cleaned_data['service']
                if self.cleaned_data['status']:
                    self.instance.status = self.cleaned_data['status']
                if self.cleaned_data['queue']:
                    self.instance.queue = self.cleaned_data['queue']
                self.instance.save()
                if self.cleaned_data['delete']:
                    if self.cleaned_data['delete'] == 'delete':
                        self.instance.delete()
                    if self.cleaned_data['delete'] == 'trash':
                        self.instance.trash = True
                        self.instance.save()


class TicketForm(forms.ModelForm):

    """ Ticket form """
    name = forms.CharField(
        label='Title', widget=forms.TextInput(attrs={'size': '50'}))

    def __init__(self, user, queue, agent, *args, **kwargs):
        "Sets allowed values"
        super(TicketForm, self).__init__(*args, **kwargs)

        # Filter allowed selections for TicketForm
        self.fields['reference'].required = False
        self.fields['reference'].label = _("Reference")
        self.fields['caller'].queryset = Object.filter_permitted(
            user, Contact.objects)
        self.fields['caller'].widget.attrs.update({'class': 'autocomplete',
                                                   'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['caller'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})
        self.fields['caller'].label = _("Caller")

        self.fields['assigned'].queryset = Object.filter_permitted(
            user, ServiceAgent.objects, mode='x')
        self.fields['assigned'].label = _("Assigned to")
        self.fields['assigned'].help_text = ""
        self.fields['assigned'].widget.attrs.update({'class': 'multicomplete',
                                                     'callback': reverse('services_ajax_agent_lookup')})
        self.fields['assigned'].widget.attrs.update(
            {'popuplink': reverse('services_agent_add')})

        self.fields['status'].queryset = Object.filter_permitted(
            user, TicketStatus.objects, mode='x')
        self.fields['status'].label = _("Status")
        self.fields['service'].queryset = Object.filter_permitted(
            user, Service.objects, mode='x')
        self.fields['service'].label = _("Service")
        self.fields['queue'].queryset = Object.filter_permitted(
            user, TicketQueue.objects, mode='x')
        self.fields['queue'].label = _("Queue")
        self.fields['sla'].queryset = Object.filter_permitted(
            user, ServiceLevelAgreement.objects, mode='x')
        self.fields['sla'].label = _("Service Level Agreement")

        self.fields['resolution'].label = _("Resolution")

        # Set default values if not editing
        if not 'instance' in kwargs:
            try:
                self.fields['caller'].initial = user.get_contact().id
            except Exception:
                pass

            if queue:
                self.fields['queue'].initial = queue.id
                if queue.default_ticket_status and queue.default_ticket_status in self.fields['status'].queryset:
                    self.fields[
                        'status'].initial = queue.default_ticket_status_id
                else:
                    try:
                        conf = ModuleSetting.get_for_module(
                            'treeio.services', 'default_ticket_status')[0]
                        self.fields['status'].initial = long(conf.value)
                    except:
                        pass

                if queue.default_ticket_priority:
                    self.fields[
                        'priority'].initial = queue.default_ticket_priority
                if queue.default_service:
                    self.fields['service'].initial = queue.default_service_id
                    try:
                        default_sla = ServiceLevelAgreement.objects.get(
                            service=queue.default_service, default=True)
                        if default_sla:
                            self.fields['sla'].initial = default_sla.id
                    except:
                        pass
            else:
                try:
                    conf = ModuleSetting.get_for_module(
                        'treeio.services', 'default_ticket_status')[0]
                    self.fields['status'].initial = long(conf.value)
                except:
                    pass
                try:
                    conf = ModuleSetting.get_for_module(
                        'treeio.services', 'default_ticket_queue')[0]
                    self.fields['queue'].initial = long(conf.value)
                except:
                    pass

        self.fields['name'].label = _("Name")
        self.fields['name'].widget.attrs.update({'class': 'duplicates',
                                                 'callback': reverse('services_ajax_ticket_lookup')})
        self.fields['priority'].label = _("Priority")
        self.fields['priority'].choices = ((5, _('Highest')), (
            4, _('High')), (3, _('Normal')), (2, _('Low')), (1, _('Lowest')))
        self.fields['urgency'].label = _("Urgency")
        self.fields['urgency'].choices = ((5, _('Highest')), (
            4, _('High')), (3, _('Normal')), (2, _('Low')), (1, _('Lowest')))
        self.fields['details'].label = _("Details")

        if not agent:
            del self.fields['caller']
            del self.fields['reference']
            del self.fields['priority']
            del self.fields['status']
            del self.fields['queue']
            del self.fields['sla']
            del self.fields['assigned']
            del self.fields['resolution']

    class Meta:

        "Ticket specified as model"
        model = Ticket
        fields = ('name', 'reference', 'caller', 'assigned', 'urgency', 'priority',
                  'status', 'service', 'sla', 'queue', 'details', 'resolution')


class TicketStatusForm(forms.ModelForm):

    """ TicketStatus form """
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '30'}))

    def __init__(self, user, *args, **kwargs):
        "Sets allowed values"
        super(TicketStatusForm, self).__init__(*args, **kwargs)

    class Meta:

        "TicketStatus specified as model"
        model = TicketStatus
        fields = ('name', 'active', 'hidden', 'details')


class TicketRecordForm(forms.ModelForm):

    """ TicketRecord form """

    def __init__(self, agent, ticket, *args, **kwargs):
        super(TicketRecordForm, self).__init__(*args, **kwargs)

        self.ticket = ticket

        self.fields['body'].label = _("body")
        self.fields['body'].required = True
        self.fields['notify'].label = _("Notify caller")
        self.fields['resolution'] = forms.BooleanField(
            label=_("Set as Resolution"), required=False)

        if not agent:
            del self.fields['notify']
            del self.fields['resolution']

    def save(self, *args, **kwargs):
        "Set Resolution if selected"
        instance = super(TicketRecordForm, self).save(*args, **kwargs)
        ticket = self.ticket
        if 'resolution' in self.cleaned_data and self.cleaned_data['resolution']:
            ticket.resolution = self.cleaned_data['body']
            ticket.save()

        # Send update if notify clicked
        if 'notify' in self.cleaned_data and self.cleaned_data['notify'] and ticket.caller:
            toaddr = ticket.caller.get_email()
            if ticket.message or toaddr:
                reply = Message()
                reply.author = instance.sender
                reply.body = instance.body
                reply.auto_notify = False
                if ticket.message:
                    reply.stream = ticket.message.stream
                    reply.reply_to = ticket.message
                else:
                    reply.stream = ticket.queue.message_stream if ticket.queue else None
                    reply.title = "[#%s] %s" % (ticket.reference, ticket.name)
                reply.save()
                if not ticket.message:
                    ticket.message = reply
                reply.recipients.add(ticket.caller)
                email = EmailMessage(reply)
                email.send_email()

        return instance

    class Meta:

        "TicketRecord specified as model"
        model = TicketRecord
        fields = ['body', 'notify']


class QueueForm(forms.ModelForm):

    """ Queue form """
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))

    def __init__(self, user, *args, **kwargs):
        "Sets allowed values"
        super(QueueForm, self).__init__(*args, **kwargs)

        manager = TicketQueue.objects
        if 'instance' in kwargs:
            instance = kwargs['instance']
            manager = manager.exclude(Q(parent=instance) & Q(pk=instance.id))
        self.fields['parent'].queryset = Object.filter_permitted(
            user, manager, mode='x')

        self.fields['default_service'].queryset = Object.filter_permitted(
            user, Service.objects, mode='x')

        self.fields['waiting_time'].help_text = "seconds"

        self.fields['name'].label = _("Name")
        self.fields['active'].label = _("Active")
        self.fields['parent'].label = _("Parent")
        self.fields['default_ticket_status'].label = _("Default ticket status")
        self.fields['default_ticket_priority'].label = _(
            "Default ticket priority")
        self.fields['default_service'].label = _("Default service")
        self.fields['waiting_time'].label = _("Waiting time")
        self.fields['next_queue'].queryset = Object.filter_permitted(
            user, TicketQueue.objects, mode='x')
        self.fields['next_queue'].label = _("Next queue")
        self.fields['ticket_code'].label = _("Ticket code")
        self.fields['message_stream'].label = _("Message stream")
        self.fields['message_stream'].widget.attrs.update(
            {'popuplink': reverse('messaging_stream_add')})
        self.fields['details'].label = _("Details")

    class Meta:

        "TicketQueue specified as model"
        model = TicketQueue
        fields = ('name', 'active', 'parent', 'default_ticket_status',
                  'default_ticket_priority', 'default_service', 'waiting_time',
                  'next_queue', 'ticket_code', 'message_stream', 'details')


class ServiceForm(forms.ModelForm):

    """ Service form """
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))

    def __init__(self, user, *args, **kwargs):
        "Sets allowed values"
        super(ServiceForm, self).__init__(*args, **kwargs)

        manager = Service.objects
        if 'instance' in kwargs:
            instance = kwargs['instance']
            manager = manager.exclude(Q(parent=instance) & Q(pk=instance.id))
        self.fields['parent'].queryset = Object.filter_permitted(
            user, manager, mode='x')

        self.fields['name'].label = _("Name")
        self.fields['parent'].label = _("Parent")
        self.fields['details'].label = _("Details")

    class Meta:

        "Service specified as model"
        model = Service
        fields = ('name', 'parent', 'details')


class ServiceLevelAgreementForm(forms.ModelForm):

    """ ServiceLevelAgreement form """
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))

    def __init__(self, user, *args, **kwargs):
        "Sets allowed values"
        super(ServiceLevelAgreementForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")

        self.fields['response_time'].help_text = 'minutes'
        self.fields['response_time'].widget.attrs.update({'size': 10})
        self.fields['response_time'].label = _("Response time")

        self.fields['uptime_rate'].help_text = 'percent'
        self.fields['uptime_rate'].widget.attrs.update({'size': 5})
        self.fields['uptime_rate'].label = _("Uptime rate")

        self.fields['service'].queryset = Object.filter_permitted(
            user, Service.objects, mode='x')
        self.fields['service'].label = _("Service")

        self.fields['client'].queryset = Object.filter_permitted(
            user, Contact.objects, mode='x')
        self.fields['client'].widget.attrs.update({'class': 'autocomplete',
                                                   'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['client'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})
        self.fields['client'].label = _("Client")

        self.fields['provider'].queryset = Object.filter_permitted(
            user, Contact.objects, mode='x')
        self.fields['provider'].widget.attrs.update({'class': 'autocomplete',
                                                     'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['provider'].widget.attrs.update(
            {'popuplink': reverse('identities_contact_add')})
        self.fields['provider'].label = _("Provider")

        self.fields['available_from'].initial = "09:00"
        self.fields['available_from'].widget.attrs.update({'size': 10})
        self.fields['available_from'].label = _("Available from")
        self.fields['available_to'].initial = "18:00"
        self.fields['available_to'].widget.attrs.update({'size': 10})
        self.fields['available_to'].label = _("Available to")

        contact = user.default_group.get_contact()
        if contact:
            self.fields['provider'].initial = contact.id

    class Meta:

        "ServiceLevelAgreement specified as model"
        model = ServiceLevelAgreement
        fields = ('name', 'service', 'client', 'provider', 'response_time', 'uptime_rate', 'available_from',
                  'available_to')


class AgentForm(forms.ModelForm):

    """ Agent form """

    def __init__(self, user, *args, **kwargs):
        "Sets allowed values"
        super(AgentForm, self).__init__(*args, **kwargs)

        self.fields['related_user'].label = _("Related user")
        self.fields['related_user'].widget.attrs.update({'class': 'autocomplete',
                                                         'callback': reverse('identities_ajax_user_lookup')})
        self.fields['active'].label = _("Active")
        self.fields['occupied'].label = _("Occupied")
        self.fields['available_from'].label = _("Available from")
        self.fields['available_to'].label = _("Available to")

    class Meta:

        "Agent specified as model"
        model = ServiceAgent
        fields = ('related_user', 'active', 'occupied',
                  'available_from', 'available_to')


class FilterForm(forms.ModelForm):

    """ Ticket Filters definition """

    def __init__(self, user, skip=[], *args, **kwargs):
        "Sets allowed values"
        super(FilterForm, self).__init__(*args, **kwargs)

        if 'caller' in skip:
            del self.fields['caller']
        else:
            self.fields['caller'].queryset = Object.filter_permitted(
                user, Contact.objects, mode='x')
            self.fields['caller'].widget.attrs.update({'class': 'autocomplete',
                                                       'callback': reverse('identities_ajax_contact_lookup')})
            self.fields['caller'].label = _("Caller")

        if 'status' in skip:
            del self.fields['status']
        else:
            self.fields['status'].queryset = Object.filter_permitted(
                user, TicketStatus.objects, mode='x')
            self.fields['status'].label = _("Status")

        self.fields['service'].queryset = Object.filter_permitted(
            user, Service.objects, mode='x')
        self.fields['service'].label = _("Service")

        self.fields['sla'].queryset = Object.filter_permitted(
            user, ServiceLevelAgreement.objects, mode='x')
        self.fields['sla'].label = _("SLA")

        if 'queue' in skip:
            del self.fields['queue']
        else:
            self.fields['queue'].queryset = Object.filter_permitted(
                user, TicketQueue.objects, mode='x')
            self.fields['queue'].label = _("Queue")

        if 'assigned' in skip:
            del self.fields['assigned']
        else:
            self.fields['assigned'].queryset = Object.filter_permitted(
                user, ServiceAgent.objects, mode='x')
            self.fields['assigned'].widget.attrs.update({'class': 'multicomplete',
                                                         'callback': reverse('services_ajax_agent_lookup')})
            self.fields['assigned'].label = _("Assigned to")
            self.fields['assigned'].help_text = ""

    class Meta:

        "Ticket specified as model"
        model = Ticket
        fields = ('caller', 'status', 'service', 'sla', 'queue', 'assigned')


class SLAFilterForm(forms.ModelForm):

    """ SLA Filters definition """

    def __init__(self, user, skip=[], *args, **kwargs):
        "Sets allowed values"
        super(SLAFilterForm, self).__init__(*args, **kwargs)

        self.fields['client'].queryset = Object.filter_permitted(
            user, Contact.objects, mode='x')
        self.fields['client'].required = False
        self.fields['client'].widget.attrs.update({'class': 'autocomplete',
                                                   'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['client'].label = _("Client")

        self.fields['provider'].queryset = Object.filter_permitted(
            user, Contact.objects, mode='x')
        self.fields['provider'].required = False
        self.fields['provider'].widget.attrs.update({'class': 'autocomplete',
                                                     'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['provider'].label = _("Provider")

        self.fields['service'].queryset = Object.filter_permitted(
            user, Service.objects, mode='x')
        self.fields['service'].required = False
        self.fields['service'].label = _("Service")

    class Meta:

        "ServiceLevelAgreement specified as model"
        model = ServiceLevelAgreement
        fields = ('service', 'client', 'provider')


class AgentFilterForm(forms.ModelForm):

    """ Agent Filters definition """

    def __init__(self, user, skip=[], *args, **kwargs):
        "Sets allowed values"
        super(AgentFilterForm, self).__init__(*args, **kwargs)

        self.fields['related_user'].required = True
        self.fields['related_user'].label = _("Related user")

    class Meta:

        "ServiceAgent specified as model"
        model = ServiceAgent
        fields = ['related_user']
