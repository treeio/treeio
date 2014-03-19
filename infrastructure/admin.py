# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Infrastructure: backend admin definitions
"""
from treeio.infrastructure.models import Item, ItemStatus, ItemType, ItemField, ItemValue
from django.contrib import admin


class ItemAdmin(admin.ModelAdmin):

    "Item backend definition"
    list_display = ('name', 'item_type')
    list_filter = ['item_type']


class ItemStatusAdmin(admin.ModelAdmin):

    "ItemStatus backend definition"
    list_display = ('name', 'active', 'hidden')


class ItemTypeAdmin(admin.ModelAdmin):

    "ItemType backend definition"
    list_display = ['name']


class ItemFieldAdmin(admin.ModelAdmin):

    "ItemField backend definition"
    list_display = ('label', 'name', 'field_type')
    list_filter = ['field_type']


class ItemValueAdmin(admin.ModelAdmin):

    "ItemValue backend definition"
    list_display = ['field', 'value']


admin.site.register(Item, ItemAdmin)
admin.site.register(ItemStatus, ItemStatusAdmin)
admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(ItemField, ItemFieldAdmin)
admin.site.register(ItemValue, ItemValueAdmin)
