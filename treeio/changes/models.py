# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Change Control models
"""
from django.db import models
from django.core.urlresolvers import reverse
from treeio.core.models import User, Object
from datetime import datetime


class ChangeSetStatus(Object):

    "State information about a ChangeSet"
    name = models.CharField(max_length=256)
    details = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    hidden = models.BooleanField(default=False)

    searchable = False

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        return reverse('changes_status_view', args=[self.id])

    class Meta:

        "ChangeSetStatus"
        ordering = ('hidden', '-active', 'name')

# ChangeSet model


class ChangeSet(models.Model):

    """ Change Set model"""
    name = models.CharField(max_length=255)
    object = models.ForeignKey(Object, related_name='changeset_object_set')
    author = models.ForeignKey(
        User, null=True, blank=True, related_name='author', on_delete=models.SET_NULL)
    resolved_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    resolved_on = models.DateTimeField(null=True, blank=True)
    status = models.ForeignKey(ChangeSetStatus)
    details = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        return reverse('changes_set_view', args=[self.id])

    class Meta:

        "ChangeSet"
        ordering = ('-date_created', 'name')

# Change Model


class Change(models.Model):

    """ Change model """
    change_set = models.ForeignKey(ChangeSet)
    change_type = models.CharField(max_length=255, null=True, blank=True)
    field = models.CharField(max_length=255, null=True, blank=True)
    change_from = models.TextField(null=True, blank=True)
    change_to = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.status

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        return reverse('changes_change_view', args=[self.id])

    class Meta:

        "Change"
        ordering = ['-date_created']
