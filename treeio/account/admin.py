# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Account: backend admin definitions
"""

from treeio.account.models import NotificationSetting, Notification
from django.contrib import admin


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'ntype', 'date_created')


class NotificationSettingAdmin(admin.ModelAdmin):

    "NotificationSetting backend definition"
    list_display = ('owner', 'ntype',)

admin.site.register(NotificationSetting, NotificationSettingAdmin)
admin.site.register(Notification, NotificationAdmin)
