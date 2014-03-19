# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core module forms
"""

import os
import sys
from django import forms
from django.db import router
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from treeio.core.models import Object
from captcha.fields import CaptchaField
from django.utils.translation import ugettext as _
from treeio.core.conf import settings
from django.db.models import Q
import django.contrib.auth.models as django_auth
from jinja2.filters import do_striptags, do_truncate
from treeio.core.models import Location, User, Widget, Tag, ConfigSetting
from treeio.core.mail import EmailPassword
from treeio.identities.models import Contact, ContactType, ContactValue


class PermissionForm(forms.ModelForm):

    "Permission Form"

    def __init__(self, *args, **kwargs):
        "Prepare form"
        super(PermissionForm, self).__init__(*args, **kwargs)

        self.fields['read_access'].help_text = ""
        self.fields['read_access'].required = False
        self.fields['read_access'].widget.attrs.update({'class': 'multicomplete',
                                                        'callback': reverse('identities_ajax_access_lookup')})

        self.fields['full_access'].help_text = ""
        self.fields['full_access'].required = False
        self.fields['full_access'].widget.attrs.update({'class': 'multicomplete',
                                                        'callback': reverse('identities_ajax_access_lookup')})

    class Meta:

        "Permission Form"
        model = Object
        fields = ('read_access', 'full_access')


class SubscribeForm(forms.Form):

    "Subscribe Form"

    subscriber = forms.ModelChoiceField(queryset=User.objects.all())

    def __init__(self, instance, *args, **kwargs):
        "Prepare form"
        subscriptions = instance.subscribers.all()

        super(SubscribeForm, self).__init__(*args, **kwargs)
        self.subscriptions = subscriptions
        self.instance = instance

        self.fields['subscriber'].label = ""
        self.fields['subscriber'].queryset = User.objects.exclude(
            pk__in=subscriptions)
        self.fields['subscriber'].widget.attrs.update({'class': 'autocomplete',
                                                       'callback': reverse('identities_ajax_user_lookup')})

    def save(self):
        "Subscribe"

        user = self.cleaned_data['subscriber']
        object = self.instance

        if not user in self.subscriptions:
            object.subscribers.add(user)
        self.subscriptions = object.subscribers.all()

        return self.subscriptions


class ObjectLinksForm(forms.Form):

    """ Object Links Form """

    links = forms.ModelChoiceField(queryset=[], empty_label=None, label='')

    def __init__(self, user, response_format, instance, *args, **kwargs):

        super(ObjectLinksForm, self).__init__(*args, **kwargs)

        queryset = Object.filter_permitted(user, Object.objects)
        self.fields['links'].queryset = queryset

        if not 'ajax' in response_format:
            if instance:
                queryset = queryset.exclude(pk__in=instance.links.all())

            choices = []
            for obj in queryset:
                human_type = obj.get_human_type()
                name = do_truncate(
                    do_striptags(unicode(obj.object_name)), 20, True)
                if human_type:
                    name += u" (" + human_type + u")"
                choices.append((obj.id, name))
            self.fields['links'].choices = choices

        self.fields['links'].label = ""
        self.fields['links'].initial = ""
        self.fields['links'].widget.attrs.update({'class': 'autocomplete',
                                                  'callback': reverse('core_ajax_object_lookup')})


class TagsForm(forms.Form):

    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())

    def __init__(self, tags, *args, **kwargs):
        super(TagsForm, self).__init__(*args, **kwargs)

        self.fields['tags'].label = ""
        self.fields['tags'].initial = [tag.id for tag in tags]
        self.fields['tags'].required = False
        self.fields['tags'].widget.attrs.update({'class': 'multicomplete',
                                                 'callback': reverse('core_ajax_tag_lookup')})

    def save(self):
        return self.cleaned_data['tags']


class LoginForm(forms.Form):

    """ Login form"""

    captcha = CaptchaField(label=_("Enter text from the image"))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        if settings.CAPTCHA_DISABLE:
            del self.fields['captcha']


class PasswordResetForm(forms.Form):

    "Password reset form"

    username = forms.CharField(label=("Username or E-mail"), max_length=75)

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = _("Username or E-mail")

    def clean_username(self):
        """
        Validates that a user exists with the given e-mail address.
        """
        username = self.cleaned_data["username"]
        if '@' in username:
            # The user entered an email, so try to log them in by e-mail
            emails = ContactValue.objects.filter(value=username,
                                                 field__field_type='email',
                                                 contact__trash=False,
                                                 contact__related_user__isnull=False)
            users = [email.contact.related_user.user for email in emails]
        else:
            users = User.objects.filter(user__username=username)
        if len(users) == 0:
            raise forms.ValidationError(
                _("Sorry, we don't know that user or e-mail."))
        else:
            username = users[0]
        return username

    def save(self):
        "Send e-mail"
        user = self.cleaned_data["username"]
        if user:
            toaddr = user.get_contact().get_email()
            if toaddr:
                password = user.generate_new_password()
                email = EmailPassword(toaddr, user.user.username, password)
                email.send_email()


class InvitationForm(forms.Form):

    """ Create account from Invitation form """

    invitation = None

    def __init__(self, invitation=None, *args, **kwargs):

        super(InvitationForm, self).__init__(*args, **kwargs)

        self.fields['username'] = forms.CharField(
            max_length=255, label=_("Username"))
        self.fields['name'] = forms.CharField(
            max_length=255, label=_("Your name"))
        self.fields['password'] = forms.CharField(max_length=255, label=_("Password"),
                                                  widget=forms.PasswordInput(render_value=False))
        self.fields['password_again'] = forms.CharField(max_length=255, label=_("Confirm Password"),
                                                        widget=forms.PasswordInput(render_value=False))

        self.invitation = invitation

    def clean_username(self):
        "Clean Name"
        data = self.cleaned_data['username']
        query = Q(name=data)
        existing = User.objects.filter(query)
        if existing:
            raise forms.ValidationError(
                _("User with username %s already exists.") % data)
        # Check Hardtree Subscription user limit
        user_limit = getattr(settings, 'HARDTREE_SUBSCRIPTION_USER_LIMIT', 0)
        if user_limit > 0:
            user_number = User.objects.filter(disabled=False).count()
            if user_number >= user_limit:
                raise forms.ValidationError(
                    _("Sorry, but your subscription does not allow more than %d users. You're currently at your limit.") % (user_limit))
        return data

    def clean_password_again(self):
        "Clean password again"
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['password_again']
        if not password1 == password2:
            raise forms.ValidationError(_("Passwords do not match"))
        return password2

    def save(self, *args, **kwargs):
        "Form processor"

        profile = None

        if self.invitation:
            # Create DjangoUser
            django_user = django_auth.User(
                username=self.cleaned_data['username'], password='')
            django_user.set_password(self.cleaned_data['password'])
            django_user.save()

            # Crate profile
            try:
                profile = django_user.get_profile()
            except:
                profile = User()
                profile.user = django_user

            profile.name = django_user.username
            profile.default_group = self.invitation.default_group
            profile.save()

            # Create contact
            try:
                contact_type = ContactType.objects.get(
                    Q(name='Person') | Q(slug='person'))
            except:
                contact_type = ContactType.objects.all()[0]

            try:
                # Check if contact has already been created (e.g. by a signals
                contact = profile.get_contact()
                if not contact:
                    contact = Contact()
            except:
                contact = Contact()

            contact.name = self.cleaned_data['name']
            contact.contact_type = contact_type
            contact.related_user = profile
            contact.save()

            # Set email
            try:
                emailfield = contact_type.fields.filter(field_type='email')[0]
                email = ContactValue(
                    value=self.invitation.email, field=emailfield, contact=contact)
                email.save()
            except:
                pass

            # Add quick start widget
            widget = Widget(user=profile,
                            perspective=profile.get_perspective(),
                            module_name='treeio.core',
                            widget_name='widget_welcome')
            widget.save()

        return profile


class LocationForm(forms.ModelForm):

    """ Item location form """

    def __init__(self, user, location_id, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _("Name")

        self.fields['parent'].label = _("Parent")
        self.fields['parent'].queryset = Object.filter_permitted(
            user, Location.objects, mode='x')
        if location_id:
            self.fields['parent'].initial = location_id

    class Meta:

        "Location Form"
        model = Location
        fields = ('name', 'parent')


class SqlSettingsForm(forms.Form):
    sql_engine = forms.ChoiceField(choices=(("postgresql", _('PostgreSQL'),), ("postgresql_psycopg2", _("Psycopg")),
                                            ("sqlite3", _("SQLite")), ("mysql", _('MySql')), ("oracle", _("Oracle"))))
    sql_database = forms.CharField(max_length=256)
    sql_user = forms.CharField(max_length=30)
    sql_password = forms.CharField(
        max_length=128, required=False, widget=forms.PasswordInput)

    def clean_sql_engine(self):
        engine = self.cleaned_data['sql_engine']
        return "django.db.backends.%s" % engine

    def create_database(self):
        if not self._errors:
            from django.db import connections
            from django.core.exceptions import ImproperlyConfigured
            from treeio.core.domains import setup_domain_database
            database = {
                'ENGINE': self.cleaned_data['sql_engine'],
                'NAME': self.cleaned_data['sql_database'],
                'USER': self.cleaned_data['sql_user'],
                'PASSWORD': self.cleaned_data['sql_password'],
            }
            # creates database
            settings.DATABASES['treeio_new_db'] = database
            try:
                setup_domain_database('treeio_new_db', True)
            except ImproperlyConfigured as exc:
                self._errors['sql_engine'] = self.error_class(
                    [_("Can't connect to engine. Error is ") + exc.message])
                del self.cleaned_data['sql_engine']
            except Exception as exc:
                del connections._connections['treeio_new_db']
                raise ValidationError(
                    _("Can't create database. SQL error is") + ' %s' % exc)
            finally:
                del settings.DATABASES['treeio_new_db']

            # save database settings
            settings.DATABASES[router.db_for_read(ConfigSetting)] = database
            connections._connections.clear()
            if not getattr(settings, 'HARDTREE_MULTITENANCY', False):
                settings_filepath = sys.modules[
                    os.environ['DJANGO_SETTINGS_MODULE']].__file__
                if settings_filepath.endswith('.pyc'):
                    settings_filepath = settings_filepath[:-1]
                with open(settings_filepath, 'r') as fl:
                    lines = fl.readlines()
                with open(settings_filepath, 'w') as fl:
                    lines = iter(lines)
                    for line in lines:
                        if 'DATABASES' not in line:
                            fl.write(line)
                        else:
                            fl.write('DATABASES = ')
                            break
                    fl.write(repr(settings.DATABASES))
                    fl.write('\n\n')
                    for line in lines:
                        if '=' in line:
                            fl.write(line)
                            break
                    for line in lines:
                        fl.write(line)
