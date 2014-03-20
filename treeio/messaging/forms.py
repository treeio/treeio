# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Messaging model forms
"""
from django import forms
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from treeio.core.models import Object, ModuleSetting
from treeio.core.conf import settings
from treeio.core.decorators import preprocess_form
from treeio.messaging.models import Message, MessageStream, MailingList
from django.db.models import Q
from treeio.identities.models import ContactType, Contact
preprocess_form()


class SettingsForm(forms.Form):

    """ Administration settings form """

    default_contact_type = forms.ModelChoiceField(
        label='Default Contact Type', queryset=[])
    default_imap_folder = forms.ChoiceField(label='Default IMAP Folder', choices=(('ALL', 'ALL'),
                                                                                  ('UNSEEN', _('UNSEEN'))), required=False)
    signature = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, user, *args, **kwargs):
        "Sets choices and initial value"
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.user = user

        self.fields['default_contact_type'].label = _('Default Contact Type')
        self.fields['default_contact_type'].queryset = Object.filter_permitted(user,
                                                                               ContactType.objects, mode='x')
        try:
            conf = ModuleSetting.get_for_module('treeio.messaging', 'default_contact_type',
                                                user=user)[0]
            default_contact_type = ContactType.objects.get(pk=long(conf.value))
            self.fields[
                'default_contact_type'].initial = default_contact_type.id
        except:
            pass

        self.fields['default_imap_folder'].label = _('Default IMAP Folder')
        try:
            conf = ModuleSetting.get_for_module('treeio.messaging', 'default_imap_folder',
                                                user=user)[0]
            self.fields['default_imap_folder'].initial = conf.value
        except:
            self.fields[
                'default_imap_folder'].initial = settings.HARDTREE_MESSAGING_IMAP_DEFAULT_FOLDER_NAME

        self.fields['signature'].label = _('Signature')
        try:
            conf = ModuleSetting.get_for_module('treeio.messaging', 'signature',
                                                user=user, strict=True)[0]
            signature = conf.value
            self.fields['signature'].initial = signature
        except:
            pass

    def save(self):
        "Form processor"
        try:
            ModuleSetting.set_for_module('default_contact_type',
                                         self.cleaned_data[
                                             'default_contact_type'].id,
                                         'treeio.messaging')
        except:
            pass

        try:
            ModuleSetting.set_for_module('default_imap_folder',
                                         self.cleaned_data[
                                             'default_imap_folder'],
                                         'treeio.messaging')
        except:
            pass

        try:
            ModuleSetting.set_for_module('signature',
                                         self.cleaned_data['signature'],
                                         'treeio.messaging', user=self.user)
        except:
            pass


class MassActionForm(forms.Form):

    """ Mass action form for Messages """

    mark = forms.ChoiceField(label=_("With selected"), choices=(('', '-----'), ('read', _('Mark Read')),
                                                                ('unread', _('Mark Unread')), (
                                                                    'delete', _('Delete Completely')),
                                                                ('trash', _('Move to Trash'))), required=False)
    stream = forms.ModelChoiceField(queryset=[], required=False)
    user = None
    markall = forms.ChoiceField(label=_("Mark all"), choices=(('', '-----'), ('markall', _('Mark all as Read'))),
                                required=False)

    instance = None

    def __init__(self, user, *args, **kwargs):
        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            del kwargs['instance']

        self.user = user

        super(MassActionForm, self).__init__(*args, **kwargs)

        self.fields['stream'].queryset = Object.filter_permitted(
            user, MessageStream.objects, mode='x')
        self.fields['stream'].label = _("Move to")
        self.fields['mark'] = forms.ChoiceField(label=_("With selected"), choices=(('', '-----'), ('read', _('Mark Read')),
                                                                                   ('unread', _('Mark Unread')), (
                                                                                       'delete', _('Delete Completely')),
                                                                                   ('trash', _('Move to Trash'))), required=False)
        self.fields['markall'] = forms.ChoiceField(label=_("Mark all"), choices=(('', '-----'), ('markall', _('Mark all as Read'))),
                                                   required=False)

    def save(self, *args, **kwargs):
        "Save override to omit empty fields"
        if self.instance:
            if self.is_valid():
                if self.cleaned_data['stream']:
                    self.instance.stream = self.cleaned_data['stream']
                if self.user and self.cleaned_data['mark']:
                    if self.cleaned_data['mark'] == 'read':
                        try:
                            self.instance.read_by.add(self.user)
                        except Exception:
                            pass
                    if self.cleaned_data['mark'] == 'unread':
                        try:
                            self.instance.read_by.remove(self.user)
                        except Exception:
                            pass
                self.instance.save()
                if self.user and self.cleaned_data['mark']:
                    if self.cleaned_data['mark'] == 'delete':
                        self.instance.delete()
                    if self.cleaned_data['mark'] == 'trash':
                        self.instance.trash = True
                        self.instance.save()
        else:
            if self.user and self.cleaned_data['markall']:
                query = Q(reply_to__isnull=True) & ~Q(read_by=self.user)
                for message in Object.filter_permitted(self.user, Message.objects.filter(query), mode='x'):
                    try:
                        message.read_by.add(self.user)
                    except Exception:
                        pass


class MessageForm(forms.ModelForm):

    """ Message form """

    def __init__(self, user, stream_id, message=None, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields['title'].label = _("Subject")
        self.fields['title'].widget = forms.TextInput(attrs={'size': '40'})
        self.fields['stream'].queryset = Object.filter_permitted(
            user, MessageStream.objects, mode='x')
        self.fields['stream'].label = _("Stream")

        self.fields['recipients'].label = _("To")
        self.fields['recipients'].help_text = ""
        self.fields['recipients'].widget.attrs.update({'class': 'multicomplete',
                                                       'callback': reverse('identities_ajax_contact_lookup')})

        if stream_id:
            self.fields['stream'].initial = stream_id
            self.fields['stream'].widget = forms.HiddenInput()
        elif self.fields['stream'].queryset:
            self.fields['stream'].initial = self.fields[
                'stream'].queryset[0].id

        self.fields['body'].label = _("Body")
        # signature
        try:
            conf = ModuleSetting.get_for_module('treeio.messaging', 'signature',
                                                user=user, strict=True)[0]
            signature = conf.value
            self.fields['body'].initial = signature
        except:
            pass

    class Meta:

        "Message"
        model = Message
        fields = ('recipients', 'title', 'stream', 'body')


class MessageReplyForm(forms.ModelForm):

    """ Message reply form """

    def __init__(self, user, stream_id, message=None, *args, **kwargs):
        super(MessageReplyForm, self).__init__(*args, **kwargs)

        self.fields['recipients'].label = _("To")
        self.fields['recipients'].help_text = ""
        self.fields['recipients'].initial = [
            contact.id for contact in message.recipients.all()]
        try:
            user_contact = user.get_contact()
            self.fields['recipients'].initial.pop(
                self.fields['recipients'].initial.index(user_contact.id))
        except:
            pass
        self.fields['recipients'].widget.attrs.update({'class': 'multicomplete',
                                                       'callback': reverse('identities_ajax_contact_lookup')})

        self.fields['stream'].widget = forms.HiddenInput()
        if stream_id:
            self.fields['stream'].initial = stream_id
        elif self.fields['stream'].queryset:
            self.fields['stream'].initial = self.fields[
                'stream'].queryset[0].id

        self.fields['body'].label = _("Body")

    class Meta:

        "Message Reply"
        model = Message
        fields = ('recipients', 'stream', 'body')


class MessageStreamForm(forms.ModelForm):

    """ Message Stream form """

    def __init__(self, user, *args, **kwargs):
        super(MessageStreamForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")
        self.fields['name'].widget = forms.TextInput(attrs={'size': '30'})

        self.fields['incoming_server_name'].label = _("Incoming Mail Server")
        self.fields['incoming_server_type'].label = _("Server Type")
        self.fields['incoming_server_username'].label = _("User Name")
        self.fields['incoming_password'].label = _("Password")
        self.fields['incoming_password'].widget = forms.PasswordInput()

        self.fields['outgoing_email'].label = _("From Address")
        self.fields['outgoing_server_name'].label = _("Outgoing Mail Server")
        self.fields['outgoing_server_type'].label = _("Server Type")
        self.fields['outgoing_server_username'].label = _("User Name")
        self.fields['outgoing_password'].label = _("Password")
        self.fields['outgoing_password'].widget = forms.PasswordInput()

    def clean_incoming_password(self):
        password = self.cleaned_data['incoming_password']
        if not password and hasattr(self, 'instance') and self.instance.id:
            return self.instance.incoming_password
        return password

    def clean_outgoing_password(self):
        password = self.cleaned_data['outgoing_password']
        if not password and hasattr(self, 'instance') and self.instance.id:
            return self.instance.outgoing_password
        return password

    class Meta:

        "Message Stream"
        model = MessageStream
        fields = ('name', 'incoming_server_name', 'incoming_server_type',
                  'incoming_server_username', 'incoming_password', 'outgoing_email',
                  'outgoing_server_name', 'outgoing_server_username', 'outgoing_password',
                  'outgoing_server_type')


class MailingListForm(forms.ModelForm):

    """ Message Stream form """

    def __init__(self, user, *args, **kwargs):
        super(MailingListForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")
        self.fields['name'].widget = forms.TextInput(attrs={'size': '30'})
        self.fields['description'].label = _("Description")
        self.fields['from_contact'].label = _("Sender Contact Details")
        self.fields['members'].widget.attrs.update({'class': 'multicomplete',
                                                    'callback': reverse('identities_ajax_contact_lookup')})
        self.fields['members'].label = _("Members")
        self.fields['members'].help_text = None
        self.fields['opt_in'].label = _("Opt-In Template")

    class Meta:

        "Message Stream"
        model = MailingList
        fields = ('name', 'description', 'from_contact', 'opt_in', 'members')


class FilterForm(forms.ModelForm):

    """ Filter form definition """

    def __init__(self, user, skip=[], *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)

        if 'title' in skip:
            del self.fields['title']
        else:
            self.fields['title'].required = False
            self.fields['title'].label = _("Title")

        if 'stream' in skip:
            del self.fields['stream']
        else:
            self.fields['stream'].queryset = Object.filter_permitted(
                user, MessageStream.objects, mode='x')
            self.fields['stream'].required = False
            self.fields['stream'].label = _("Stream")

        if 'author' in skip:
            del self.fields['author']
        else:
            self.fields['author'].required = False
            self.fields['author'].label = _("Author")
            self.fields['author'].queryset = Object.filter_permitted(
                user, Contact.objects, mode='x')
            self.fields['author'].widget.attrs.update({'class': 'autocomplete',
                                                                'callback': reverse('identities_ajax_contact_lookup')})

    class Meta:

        "Filter"
        model = Message
        fields = ('title', 'author', 'stream')
