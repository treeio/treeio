# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Infrastructure module objects
"""
from django.db import models
from django.core.urlresolvers import reverse
from treeio.core.models import Object, Location
from treeio.identities.models import Contact
from treeio.finance.models import Transaction, Asset
import datetime


class ItemField(Object):

    """ ItemField model """
    name = models.CharField(max_length=256)
    label = models.CharField(max_length=256)
    field_type = models.CharField(max_length=64, choices=(('text', 'Text'),
                                                          ('details',
                                                           'Details'),
                                                          ('url', 'URL'),
                                                          ('picture',
                                                           'Picture'),
                                                          ('date', 'Date')
                                                          ))
    required = models.BooleanField(default=False)
    allowed_values = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    searchable = False

    class Meta:

        "ItemField"
        ordering = ['name']

    def __unicode__(self):
        return self.label


class ItemType(Object):

    """ ItemType model """
    name = models.CharField(max_length=512)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='child_set')
    fields = models.ManyToManyField(ItemField, blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    access_inherit = ('parent', '*module', '*user')

    class Meta:

        "ItemType"
        ordering = ['name']

    def __unicode__(self):
        return self.name


class ItemStatus(Object):

    "State information about an infrastructure Item"
    name = models.CharField(max_length=256)
    details = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    hidden = models.BooleanField(default=False)

    class Meta:

        "ItemStatus"
        ordering = ('hidden', '-active', 'name')

    def __unicode__(self):
        return self.name


class Item(Object):

    """ Item model """
    name = models.CharField(max_length=512)
    item_type = models.ForeignKey(ItemType)
    status = models.ForeignKey(ItemStatus)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='child_set')
    manufacturer = models.ForeignKey(
        Contact, blank=True, null=True, related_name='items_manufactured', on_delete=models.SET_NULL)
    supplier = models.ForeignKey(
        Contact, blank=True, null=True, related_name='items_supplied', on_delete=models.SET_NULL)
    location = models.ForeignKey(
        Location, blank=True, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(
        Contact, blank=True, null=True, related_name='items_owned', on_delete=models.SET_NULL)
    asset = models.ForeignKey(
        Asset, blank=True, null=True, on_delete=models.SET_NULL)

    access_inherit = ('parent', 'item_type', '*module', '*user')

    class Meta:

        "Item"
        ordering = ['name']

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        try:
            return reverse('infrastructure_item_view', args=[self.id])
        except Exception:
            return ""

    def get_servicing(self):
        "Returns a QuerySet of all ItemServicing records"

        return self.itemservicing_set.filter()

    def get_active_servicing(self):
        "Returns a QuerySet of active ItemServicing records with expiry date in the future"
        now = datetime.datetime.now()
        return self.itemservicing_set.filter(expiry_date__gte=now.date())

    def __unicode__(self):
        return self.name


class ItemValue(models.Model):

    """ ItemValue model """
    field = models.ForeignKey(ItemField)
    item = models.ForeignKey(Item)
    value = models.TextField(blank=True)

    def name(self):
        return self.field.name

    def __unicode__(self):
        return self.value


class ItemServicing(Object):

    """ ServiceRecord model """
    name = models.CharField(max_length=256)
    items = models.ManyToManyField(Item, blank=True, null=True)
    supplier = models.ForeignKey(
        Contact, blank=True, null=True, related_name='itemservice_supplied', on_delete=models.SET_NULL)
    start_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    payments = models.ManyToManyField(Transaction, blank=True, null=True)
    details = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    class Meta:

        "ItemServicing"
        ordering = ['-expiry_date']

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        try:
            return reverse('infrastructure_service_record_view', args=[self.id])
        except Exception:
            return ""
