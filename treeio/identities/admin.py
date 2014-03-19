# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Identities: backend admin definitions
"""

from treeio.identities.models import Contact, ContactType, ContactField, ContactValue
from django.contrib import admin


class ContactAdmin(admin.ModelAdmin):

    "Contact backend definition"
    list_display = ('name', 'contact_type')
    list_filter = ['contact_type']


class ContactTypeAdmin(admin.ModelAdmin):

    "ContactType backend definition"
    list_display = ['name']


class ContactFieldAdmin(admin.ModelAdmin):

    "ContactField backend definition"
    list_display = ('name', 'label', 'field_type')
    list_filter = ['field_type']


class ContactValueAdmin(admin.ModelAdmin):

    "ContactValue backend definition"
    list_display = ('field', 'contact')
    list_filter = ['field']


admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactType, ContactTypeAdmin)
admin.site.register(ContactField, ContactFieldAdmin)
admin.site.register(ContactValue, ContactValueAdmin)
