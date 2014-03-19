# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Administration module forms
"""
from django import forms
from django.forms import ModelChoiceField
from treeio.core.conf import settings
from django.db.models import Q
from django.core.files.storage import default_storage
import django.contrib.auth.models as django_auth
from django.utils.translation import ugettext as _
from treeio.core.decorators import preprocess_form
from treeio.core.models import User, Group, Perspective, ModuleSetting, Page, PageFolder
import hashlib
import random
import re

preprocess_form()

PERMISSION_CHOICES = (
    ('everyone', 'Everyone'),
    ('usergroup', 'Automatic, User and Default Group'),
    ('usergroupreadonly', 'Automatic, User and Default Group. READ ONLY'),
    ('userallgroups', 'Automatic, User and All Their Groups'),
    ('userallgroupsreadonly',
     'Automatic, User and All Their Groups. READ ONLY'),
    ('user', 'Automatic, User Only'),
    ('userreadonly', 'Automatic, User Only. READ ONLY'),
    ('nomoduleusergroup', 'Automatic, Skip Module, User and Default Group'),
    ('nomoduleusergroupreadonly',
     'Automatic, Skip Module, User and Default Group. READ ONLY'),
    ('nomoduleuserallgroups',
     'Automatic, Skip Module, User and All Their Groups'),
    ('nomoduleuserallgroupsreadonly',
     'Automatic, Skip Module, User and All Their Groups. READ ONLY'),
    ('nomoduleuser', 'Automatic, Skip Module, User Only'),
    ('nomoduleuserreadonly', 'Automatic, Skip Module, User Only. READ ONLY'),
    ('forceusergroup', 'Force User and Default Group'),
    ('forceuserallgroups', 'Force User and All Their Groups'),
    ('forceuser', 'Force User Only'),
)


class SettingsForm(forms.Form):

    """ Global settings form """

    default_perspective = forms.ModelChoiceField(
        label='Default Perspective', queryset=[])
    default_permissions = forms.ChoiceField(label='Default Permissions',
                                            choices=PERMISSION_CHOICES)
    language = forms.ChoiceField(label='Language', choices=[])
    default_timezone = forms.ChoiceField(label='Time Zone', choices=[])
    logo = forms.ImageField(
        label='Logo', required=False, widget=forms.FileInput)

    def __init__(self, user, *args, **kwargs):
        "Sets choices and initial value"
        super(SettingsForm, self).__init__(*args, **kwargs)

        self.fields['default_perspective'].queryset = Perspective.objects.all()
        try:
            conf = ModuleSetting.get_for_module(
                'treeio.core', 'default_perspective')[0]
            default_perspective = Perspective.objects.get(pk=long(conf.value))
            self.fields['default_perspective'].initial = default_perspective.id
        except:
            pass

        try:
            conf = ModuleSetting.get_for_module(
                'treeio.core', 'default_permissions')[0]
            self.fields['default_permissions'].initial = conf.value
        except:
            self.fields['default_permissions'].initial = getattr(
                settings, 'HARDTREE_DEFAULT_PERMISSIONS', 'everyone')

        self.fields['default_timezone'].choices = getattr(
            settings, 'HARDTREE_SERVER_TIMEZONE')
        timezone = settings.HARDTREE_SERVER_DEFAULT_TIMEZONE
        try:
            conf = ModuleSetting.get_for_module(
                'treeio.core', 'default_timezone')[0]
            timezone = conf.value
        except Exception:
            pass
        self.fields['default_timezone'].initial = timezone

        self.fields['language'].choices = getattr(
            settings, 'HARDTREE_LANGUAGES', [('en', 'English')])
        language = getattr(settings, 'HARDTREE_LANGUAGES_DEFAULT', '')
        try:
            conf = ModuleSetting.get_for_module('treeio.core', 'language')[0]
            language = conf.value
        except IndexError:
            pass
        self.fields['language'].initial = language

        if getattr(settings, 'HARDTREE_SUBSCRIPTION_CUSTOMIZATION', True):
            logopath = ''
            try:
                conf = ModuleSetting.get_for_module(
                    'treeio.core', 'logopath')[0]
                logopath = conf.value
            except:
                pass

            if logopath:
                match = re.match('.*[a-z0-9]{32}__(?P<filename>.+)$', logopath)
                if match:
                    logopath = match.group('filename')
                form_field = forms.ChoiceField(
                    label=_("Logo"), widget=forms.RadioSelect())
                form_field.choices = ((logopath, _("Keep existing: ") + unicode(logopath)),
                                      ('delete', "Delete "))
                form_field.initial = logopath
                form_field.required = False
                self.fields['logo'] = form_field
            self.fields['logo'].label = _("Logo")
        else:
            del self.fields['logo']

        self.fields['default_perspective'].label = _("Default Perspective")
        self.fields['default_permissions'].label = _("Default Permissions")
        self.fields['default_timezone'].label = _("Time Zone")
        self.fields['language'].label = _("Language")

    def _get_upload_name(self, filename):
        "Returns an upload_to path to a new file"
        while True:
            hasher = hashlib.md5()
            hasher.update(str(random.random()))
            filepath = u"core/" + hasher.hexdigest() + u"__" + filename
            fullpath = settings.MEDIA_ROOT + filepath
            if not default_storage.exists(fullpath):
                return filepath

    def _handle_uploaded_file(self, field_name):
        "Process an uploaded file"
        try:
            file = self.files[field_name]
            filepath = self._get_upload_name(file.name)
        except KeyError:
            return ''
        destination = open(settings.MEDIA_ROOT + filepath, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        return filepath

    def save(self):
        "Form processor"
        try:
            ModuleSetting.set_for_module('default_perspective',
                                         self.cleaned_data[
                                             'default_perspective'].id,
                                         'treeio.core')
            ModuleSetting.set_for_module('default_permissions',
                                         self.cleaned_data[
                                             'default_permissions'],
                                         'treeio.core')
            ModuleSetting.set_for_module('default_timezone',
                                         self.cleaned_data['default_timezone'],
                                         'treeio.core')
            ModuleSetting.set_for_module('language',
                                         self.cleaned_data['language'],
                                         'treeio.core')
            if getattr(settings, 'HARDTREE_SUBSCRIPTION_CUSTOMIZATION', True):
                if isinstance(self.fields['logo'], forms.FileField):
                    logopath = self._handle_uploaded_file('logo')
                    ModuleSetting.set_for_module(
                        'logopath', logopath, 'treeio.core')

                elif isinstance(self.fields['logo'], forms.ChoiceField):
                    if self.cleaned_data['logo'] == 'delete':
                        try:
                            ModuleSetting.get_for_module(
                                'treeio.core', 'logopath').delete()
                        except:
                            pass

            return True

        except:
            return False


class PerspectiveForm(forms.ModelForm):

    """ Perspective form """
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))

    def __init__(self, user, *args, **kwargs):
        super(PerspectiveForm, self).__init__(*args, **kwargs)

        self.fields['modules'].help_text = ""
        self.fields['name'].label = _("Name")
        self.fields['modules'].label = _("Modules")
        self.fields['details'].label = _("Details")

    class Meta:

        "Perspective Form"
        model = Perspective
        fields = ('name', 'modules', 'details')


class UserForm(forms.ModelForm):

    """ User form """
    perspective = ModelChoiceField(
        label='Perspective', queryset=[], required=False)

    def __init__(self, *args, **kwargs):

        super(UserForm, self).__init__(*args, **kwargs)

        if 'instance' in kwargs:
            self.instance = kwargs['instance']
        else:
            self.fields['password'] = forms.CharField(max_length=255, label=_("Password"),
                                                      widget=forms.PasswordInput(render_value=False))
            self.fields['password_again'] = forms.CharField(max_length=255, label=_("Confirm Password"),
                                                            widget=forms.PasswordInput(render_value=False))

        self.fields['name'].label = _("Username")
        self.fields['name'].help_text = _("Used to log in")
        self.fields['default_group'].label = _("Default group")
        self.fields['other_groups'].label = _("Other groups")
        self.fields['other_groups'].help_text = ""
        self.fields['perspective'].label = _("Perspective")
        self.fields['perspective'].queryset = Perspective.objects.all()
        if self.instance:
            try:
                self.fields[
                    'perspective'].initial = self.instance.get_perspective()
            except:
                pass

    def clean_name(self):
        "Clean Name"
        data = self.cleaned_data['name']
        query = Q(name=data)
        if self.instance and self.instance.id:
            query = query & ~Q(id=self.instance.id)
        existing = User.objects.filter(query)
        if existing:
            raise forms.ValidationError(
                _("User with username %s already exists.") % data)
        if self.instance and not self.instance.id:
            # Check Hardtree Subscription user limit
            user_limit = getattr(
                settings, 'HARDTREE_SUBSCRIPTION_USER_LIMIT', 0)
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

    def clean_disabled(self):
        "Ensure the admin does not go over subscription limit by re-enabling users"
        enable = not self.cleaned_data['disabled']
        if self.instance and self.instance.id and enable and self.instance.disabled:
            user_limit = getattr(
                settings, 'HARDTREE_SUBSCRIPTION_USER_LIMIT', 0)
            if user_limit > 0:
                user_number = User.objects.filter(disabled=False).count()
                if user_number >= user_limit:
                    raise forms.ValidationError(
                        _("Sorry, but your subscription does not allow more than %d users. You're currently at your limit.") % (user_limit))
        return self.cleaned_data['disabled']

    def save(self, *args, **kwargs):
        "Form processor"

        if self.instance.id:
            self.instance.user.username = self.instance.name
            self.instance.user.save()
            super(UserForm, self).save(*args, **kwargs)
        else:
            new_user = django_auth.User(
                username=self.cleaned_data['name'], password='')
            new_user.set_password(self.cleaned_data['password'])
            new_user.save()
            self.instance.user = new_user
            super(UserForm, self).save(*args, **kwargs)

        if self.cleaned_data['perspective']:
            self.instance.set_perspective(self.cleaned_data['perspective'])

        return self.instance

    class Meta:

        "User Form"
        model = User
        fields = ('name', 'default_group', 'other_groups', 'disabled')


class PasswordForm(forms.Form):

    """ Password form """

    new_password = forms.CharField(max_length=255, label=_("New Password"),
                                   widget=forms.PasswordInput(render_value=False))
    new_password_again = forms.CharField(max_length=255, label=_("Confirm Password"),
                                         widget=forms.PasswordInput(render_value=False))

    user = None

    def __init__(self, user, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['new_password'].label = _("New Password")
        self.fields['new_password_again'].label = _("Confirm Password")

    def clean_new_password_again(self):
        "Clean New Password Again"
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


class GroupForm(forms.ModelForm):

    """ Group form """
    perspective = ModelChoiceField(
        label=_('Perspective'), queryset=[], required=False)

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)

        self.fields['perspective'].label = _('Perspective')
        self.fields['perspective'].queryset = Perspective.objects.all()
        if self.instance:
            try:
                self.fields[
                    'perspective'].initial = self.instance.get_perspective()
            except:
                pass

    def save(self, *args, **kwargs):
        instance = super(GroupForm, self).save(*args, **kwargs)
        if instance.id and self.cleaned_data['perspective']:
            instance.set_perspective(self.cleaned_data['perspective'])
        return instance

    class Meta:

        "Group Form"
        model = Group
        fields = ('name', 'parent', 'details')


class PageForm(forms.ModelForm):

    """ Static Page form """
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)

    class Meta:

        "Page Form"
        model = Page
        fields = ('name', 'title', 'folder', 'published', 'body')


class PageFolderForm(forms.ModelForm):

    """ PageFolder for Static Pages form """
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))

    def __init__(self, *args, **kwargs):
        super(PageFolderForm, self).__init__(*args, **kwargs)

    class Meta:

        "Page Folder Form"
        model = PageFolder
        fields = ('name', 'details')


class FilterForm(forms.ModelForm):

    """ Filter form for Modules definition """

    def __init__(self, user, type=[], *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)

        if 'perspective' in type:
            del self.fields['name']
            self.fields['modules'].help_text = ""

        if 'module' in type:
            del self.fields['name']
            self.fields['modules'].help_text = ""

    class Meta:

        "Filter"
        model = Perspective
        fields = ('name', 'modules')

from treeio.identities.forms import ContactForm


class ContactSetupForm(ContactForm):

    """ ContactSetupForm """

    name = forms.CharField(
        max_length=256, widget=forms.TextInput(attrs={'size': '50'}))
    instance = None
    files = {}

    def __init__(self, contact_type, instance=None, *args, **kwargs):
        "Populates form with fields from given ContactType"

        if instance:
            self.instance = instance
            values = instance.contactvalue_set.all()

        super(ContactForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = _('Name')

        if 'files' in kwargs:
            self.files = kwargs['files']

        for field in contact_type.fields.all():
            if self.instance:
                initial_field_name = self._get_free_field_name(field)
                self.fields[initial_field_name] = self._get_form_field(field)
                for value in values:
                    if value.field == field:
                        field_name = self._get_free_field_name(field)
                        self.fields[field_name] = self._get_form_field(
                            field, value)
                        if initial_field_name in self.fields:
                            del self.fields[initial_field_name]
            else:
                field_name = self._get_free_field_name(field)
                self.fields[field_name] = self._get_form_field(field)

        if self.instance:
            self.fields['name'].initial = self.instance.name
