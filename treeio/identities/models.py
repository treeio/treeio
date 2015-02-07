# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Identities module objects
"""

from django.db import models
from treeio.core.models import AccessEntity, User, Object
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from treeio.core.conf import settings
from django.template import defaultfilters
from unidecode import unidecode


class ContactField(Object):
    "Represents a field within a ContentType"
    FIELD_TYPES = (
        ('text', 'Text'),
        ('textarea', 'Multiline Text'),
        ('details', 'Details'),
        ('url', 'URL'),
        ('email', 'E-mail'),
        ('phone', 'Phone'),
        ('picture', 'Picture'),
        ('date', 'Date')
    )

    name = models.CharField(max_length=256)
    label = models.CharField(max_length=256)
    field_type = models.CharField(max_length=64, choices=FIELD_TYPES)
    required = models.BooleanField(default=False)
    allowed_values = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    searchable = False

    class Meta:
        "ContactField"
        ordering = ['name']

    def __unicode__(self):
        return self.label


class ContactType(Object):
    "Defines a type of Contact entities"
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=256)
    details = models.TextField(blank=True, null=True)
    fields = models.ManyToManyField(ContactField, blank=True, null=True)

    class Meta:
        "ContactType"
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        try:
            return reverse('identities_index_by_type', args=[self.slug])
        except Exception:
            return ""

    def save(self, *args, **kwargs):
        "Override to auto-set slug"
        self.slug = unicode(self.name).replace(" ", "-")
        self.slug = defaultfilters.slugify(unidecode(self.slug))
        super(ContactType, self).save(*args, **kwargs)


class Contact(Object):
    "Information about a company, group or user. By design allows custom fields defined in ContactField"
    contact_type = models.ForeignKey(ContactType)
    name = models.CharField(max_length=256)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='child_set')
    related_user = models.ForeignKey(
        AccessEntity, blank=True, null=True, on_delete=models.SET_NULL)

    access_inherit = ('parent', '*module', '*user')

    class Meta:
        "Contact"
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        try:
            return reverse('identities_contact_view', args=[self.id])
        except Exception:
            return ""

    def get_email(self):
        "Returns the first available e-mail"
        values = self.contactvalue_set.filter(
            field__field_type='email', value__isnull=False)
        if values:
            return values[0].value
        return ''

    def get_picture(self):
        values = self.contactvalue_set.filter(
            field__field_type='picture', value__isnull=False)
        if values and values[0].value:
            return values[0].value

        return reverse('identities_contact_view_picture', args=[self.id])

    def get_or_create_by_email(email, name=None, contact_type=None):
        """
        Using a given email tries to find an existing Contact or create new one if not found.
        If name is not specified the given email address is used for name instead.
        """
        created = False
        if not contact_type:
            try:
                contact_type = ContactType.objects.get(slug='person')
            except ContactType.DoesNotExist:
                try:
                    contact_type = ContactType.objects.all()[0]
                except KeyError:
                    return None, created

        if not name:
            name = email

        contact = Contact.objects.filter(
            contactvalue__value=email, contactvalue__field__field_type='email')[:1]
        if contact:
            return contact[0], created
        else:
            contact = Contact(contact_type=contact_type, name=name)
            contact.save()
            created = True
            try:
                emailfield = contact_type.fields.filter(
                    field_type='email')[:1][0]
                ContactValue(
                    field=emailfield, contact=contact, value=email).save()
            except IndexError:
                pass

        return contact, created

    get_or_create_by_email = staticmethod(get_or_create_by_email)


class ContactValue(models.Model):
    "A value selected for a Contact"
    field = models.ForeignKey(ContactField)
    contact = models.ForeignKey(Contact)
    value = models.CharField(max_length=1024, null=True, blank=True)

    def __unicode__(self):
        return self.value

    def name(self):
        return self.field.name


def contact_autocreate_handler(sender, instance, created, **kwargs):
    "When a User is created, automatically create a Contact of type Person"
    if created:
        try:
            contact_type = ContactType.objects.filter(
                models.Q(name='Person') | models.Q(slug='person'))[0]
            contact = Contact(
                contact_type=contact_type, name=instance.name, related_user=instance)
            contact.save()
        except:
            pass


# Autocreate a Contact when Hardtree user is created
if getattr(settings, 'HARDTREE_SIGNALS_AUTOCREATE_CONTACT', True):
    post_save.connect(contact_autocreate_handler, sender=User)
