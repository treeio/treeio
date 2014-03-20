# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Service Support: back-end administrator definitions
"""
from django.contrib import admin
from treeio.services.models import Ticket, TicketStatus, TicketQueue
from treeio.services.models import Service, ServiceAgent, ServiceLevelAgreement


class TicketAdmin(admin.ModelAdmin):

    "Ticket backend definition"
    list_display = ['name']
    search_fields = ['name']


class TicketStatusAdmin(admin.ModelAdmin):

    "TicketStatus backend definition"
    list_display = ['name', 'active', 'hidden']
    search_fields = ['name']


class TicketQueueAdmin(admin.ModelAdmin):

    "TicketQueue backend definition"
    list_display = ['name', 'parent', 'default_ticket_status']
    search_fields = ['name']

admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketStatus, TicketStatusAdmin)
admin.site.register(TicketQueue, TicketQueueAdmin)


class ServiceAdmin(admin.ModelAdmin):

    "Service backend definition"
    list_display = ['name']
    search_fields = ['name']


class ServiceAgentAdmin(admin.ModelAdmin):

    "ServiceAgent backend definition"
    list_display = ['related_user', 'available_from', 'available_to', 'active']
    list_filter = ['active']


class ServiceLevelAgreementAdmin(admin.ModelAdmin):

    "ServiceLevelAgreement backend definition"
    list_display = ['name', 'response_time', 'uptime_rate']
    search_fields = ['name']

admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceAgent, ServiceAgentAdmin)
admin.site.register(ServiceLevelAgreement, ServiceLevelAgreementAdmin)
