# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core forms
"""
from django import forms
from treeio.account.models import NotificationSetting, notification_types
from treeio.core.models import User, Object, ModuleSetting, Perspective, Module
from django.utils.translation import ugettext as _
from treeio.core.decorators import preprocess_form
from treeio.core.conf import settings
from datetime import date

preprocess_form()


class MassActionForm(forms.Form):
    """ Mass action form for Accounts """

    delete = forms.ChoiceField(label=_("With selected"),
        choices=(('', '-----'), ('delete', _('Delete Completely')),
                 ('trash', _('Move to Trash'))), required=False)

    instance = None

    def __init__(self, user, *args, **kwargs):
        if 'instance' in kwargs:
            self.instance = kwargs['instance']
            del kwargs['instance']

        super(MassActionForm, self).__init__(*args, **kwargs)
        self.fields['delete'] = forms.ChoiceField(label=_("With selected"),
            choices=(('', '-----'), ('delete', _('Delete Completely')),
                     ('trash', _('Move to Trash'))), required=False)

    def save(self, *args, **kwargs):
        "Process form"
        if self.instance:
            if self.is_valid():
                if self.cleaned_data['delete']:
                    if self.cleaned_data['delete'] == 'delete':
                        self.instance.delete()
                    if self.cleaned_data['delete'] == 'trash':
                        self.instance.trash = True
                        self.instance.save()


class AccountForm(forms.ModelForm):

    """ Account form """

    def __init__(self, *args, **kwargs):
        self.instance = kwargs['instance']
        super(AccountForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Username")

    def save(self, *args, **kwargs):
        "Form processor"
        super(AccountForm, self).save(*args, **kwargs)

        self.instance.user.username = self.instance.name
        self.instance.user.save()

    def clean_name(self):
        "Clean name"
        data = self.cleaned_data['name']
        existing = User.objects.filter(name=data).exclude(pk=self.instance.id)
        if existing:
            raise forms.ValidationError(
                _("User with username %s already exists.") % data)
        return data

    class Meta:

        "Account Form"
        model = User
        fields = ('name', 'default_group', 'other_groups')


class AccountPasswordForm(forms.Form):

    """ Password form """

    old_password = forms.CharField(max_length=255,
                                   widget=forms.PasswordInput(render_value=False))
    new_password = forms.CharField(max_length=255,
                                   widget=forms.PasswordInput(render_value=False))
    new_password_again = forms.CharField(max_length=255,
                                         widget=forms.PasswordInput(render_value=False))

    user = None

    def __init__(self, user, *args, **kwargs):
        super(AccountPasswordForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = _("Current Password")
        self.fields['new_password'].label = _("New Password")
        self.fields['new_password_again'].label = _("Confirm Password")

        self.user = user

    def clean_old_password(self):
        "Clean old password"
        data = self.cleaned_data['old_password']
        if not self.user.check_password(data):
            raise forms.ValidationError(_("Current password is wrong"))
        return data

    def clean_new_password_again(self):
        "Clean new password again"
        password1 = self.cleaned_data['new_password']
        password2 = self.cleaned_data['new_password_again']
        if not password1 == password2:
            raise forms.ValidationError(_("Passwords do not match"))
        return password2

    def save(self):
        "Save"
        password1 = self.cleaned_data['new_password']
        self.user.set_password(password1)
        return self.user.save()


class SettingsForm(forms.Form):

    """ User Account settings form """

    default_perspective = forms.ModelChoiceField(
        label='Default Perspective', queryset=[])
    language = forms.ChoiceField(label='Language', choices=[])
    default_timezone = forms.ChoiceField(label='Time Zone', choices=[])
    user = None
    email_notifications = forms.ChoiceField(
        label="E-mail Notifications", choices=(('never', _('Never (disabled)')), ('True', _('As-it-happens'))) + notification_types, required=False)
    notifications_for_modules = forms.MultipleChoiceField(
        label="Receive notifications for modules", required=False)

    def __init__(self, user, *args, **kwargs):
        "Sets choices and initial value"
        super(SettingsForm, self).__init__(*args, **kwargs)

        self.fields['default_perspective'].label = _("Default Perspective")
        self.fields['language'].label = _("Language")
        self.fields['default_timezone'].label = _("Time Zone")
        self.fields['email_notifications'].label = _("E-mail Notifications")

        self.user = user

        self.fields['default_perspective'].queryset = Object.filter_permitted(
            user, Perspective.objects)
        try:
            conf = ModuleSetting.get_for_module(
                'treeio.core', 'default_perspective', user=self.user)[0]
            default_perspective = Perspective.objects.get(pk=long(conf.value))
            self.fields['default_perspective'].initial = default_perspective.id
        except:
            pass

        self.fields['default_timezone'].choices = getattr(
            settings, 'HARDTREE_SERVER_TIMEZONE')
        timezone = settings.HARDTREE_SERVER_DEFAULT_TIMEZONE
        try:
            conf = ModuleSetting.get('default_timezone', user=user)[0]
            timezone = conf.value
        except:
            pass
        self.fields['default_timezone'].initial = timezone

        self.fields['language'].choices = getattr(
            settings, 'HARDTREE_LANGUAGES', [('en', 'English')])
        language = getattr(settings, 'HARDTREE_LANGUAGES_DEFAULT', '')
        try:
            conf = ModuleSetting.get('language', user=user)[0]
            language = conf.value
        except IndexError:
            pass
        self.fields['language'].initial = language

        try:
            conf = ModuleSetting.get('email_notifications', user=user)[0]
            self.fields['email_notifications'].initial = conf.value
        except:
            self.fields[
                'email_notifications'].initial = settings.HARDTREE_ALLOW_EMAIL_NOTIFICATIONS

        perspective = user.get_perspective()

        modules = perspective.modules.filter(display=True).order_by('title')
        if not modules:
            modules = Module.objects.filter(display=True).order_by('title')
        self.fields['notifications_for_modules'].choices = [
            (module.pk, module.title) for module in modules]

        try:
            modules = NotificationSetting.objects.get(
                owner=self.user).modules.all()
            self.fields['notifications_for_modules'].initial = [
                m.pk for m in modules]
        except (NotificationSetting.DoesNotExist, NotificationSetting.MultipleObjectsReturned):
            pass

    def save(self):
        "Form processor"
        try:
            ModuleSetting.set_for_module('default_perspective',
                                         self.cleaned_data[
                                             'default_perspective'].id,
                                         'treeio.core', user=self.user)
            ModuleSetting.set_for_module('default_timezone',
                                         self.cleaned_data['default_timezone'],
                                         'treeio.core', user=self.user)
            ModuleSetting.set_for_module('language',
                                         self.cleaned_data['language'],
                                         'treeio.core', user=self.user)
            # notification settings
            email_notifications = self.cleaned_data['email_notifications']
            notification, created = NotificationSetting.objects.get_or_create(
                owner=self.user)
            if email_notifications in ('d', 'w', 'm'):
                notification.ntype = email_notifications
                if not notification.enabled:
                    notification.enabled = True
                    notification.update_date(date.today())
                notification.save()
                notification.modules.clear()
                for m in Module.objects.filter(pk__in=self.cleaned_data['notifications_for_modules']):
                    notification.modules.add(m)
            else:
                notification.enabled = False
                notification.save()
            ModuleSetting.set_for_module('email_notifications',
                                         email_notifications,
                                         'treeio.core', user=self.user)
            return True

        except:
            return False
