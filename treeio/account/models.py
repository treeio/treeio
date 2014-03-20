# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Account module objects
"""

import calendar
from django.db import models
from treeio.core.models import User, Module
from datetime import datetime, date, timedelta
from django.utils.translation import ugettext as _

notification_types = (('d', _('Daily')),
                      ('w', _('Weekly')),
                      ('m', _('Monthly')))


class Notification(models.Model):
    recipient = models.ForeignKey(User)
    body = models.TextField(default='', blank=True, null=True)
    ntype = models.CharField(max_length=1, choices=notification_types)
    date_created = models.DateTimeField(default=datetime.now)


class NotificationSetting(models.Model):
    owner = models.ForeignKey(User, unique=True)
    modules = models.ManyToManyField(Module)
    ntype = models.CharField(
        max_length=1, choices=notification_types, verbose_name='Type')
    next_date = models.DateField(null=True, blank=True)
    last_datetime = models.DateTimeField(default=datetime.now)
    enabled = models.BooleanField(default=True)

    def __unicode__(self):
        if self.module:
            return '%s of %s' % (self.get_ntype_display(), self.module.title)
        return self.get_ntype_display()

    def save(self, *args, **kwargs):
        if not (self.id and self.next_date):
            self.next_date = date.today() + timedelta(days=1)
        return super(NotificationSetting, self).save(*args, **kwargs)

    def update_date(self, now):
        if isinstance(now, datetime):
            today = now.date()
            self.last_datetime = now
        elif isinstance(now, date):
            today = now
        else:
            raise ValueError('now must be datetime or date')
        if self.ntype == 'd':
            self.next_date = today + timedelta(days=1)
        elif self.ntype == 'w':
            self.next_date = today + timedelta(days=7 - today.weekday())
        elif self.ntype == 'm':
            self.next_date = today + \
                timedelta(days=calendar.mdays[today.month] - today.day + 1)
        self.save()

    def title(self):
        if self.ntype == 'd':
            return '<h1>Today</h1>'
        elif self.ntype == 'w':
            return '<h1>%s week</h1>' % self.next_date.isocalendar()[1]
        elif self.ntype == 'm':
            return '<h1>%s</h1>' % calendar.month_name[self.next_date.month]
