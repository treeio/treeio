# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core: backend admin definitions
"""

from treeio.core.models import User, Group, Object, Module, Perspective, ModuleSetting
from treeio.core.models import PageFolder, Page, UpdateRecord, Widget
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):

    "User backend definition"
    list_display = ('user', 'default_group')


class GroupAdmin(admin.ModelAdmin):

    "Group backend definition"
    list_display = ['name']


class ObjectAdmin(admin.ModelAdmin):

    "Object backend definition"
    list_display = ('__unicode__', 'object_type', 'last_updated')
    list_filter = ['object_type']


class ModuleAdmin(admin.ModelAdmin):

    "Module backend definition"
    list_display = ('name', 'title', 'url', 'display', 'system')
    list_filter = ['display']


class PerspectiveAdmin(admin.ModelAdmin):

    "Perspective backend definition"
    list_display = ['name']


class ModuleSettingAdmin(admin.ModelAdmin):

    "Module settings backend definition"
    list_display = ('label', 'name', 'user', 'perspective', 'module')
    list_filter = ['perspective', 'module']


class PageFolderAdmin(admin.ModelAdmin):

    "PageFolder backend definition"
    list_display = ['name']


class PageAdmin(admin.ModelAdmin):

    "Page backend definition"
    list_display = ('name', 'title', 'folder', 'published')
    list_filter = ['folder', 'published']


class UpdateRecordAdmin(admin.ModelAdmin):

    "UpdateRecord backend definition"
    list_display = ('record_type', 'body')
    list_filter = ['recipients']


class WidgetAdmin(admin.ModelAdmin):

    "Widget backend definition"
    list_display = ('widget_name', 'module_name', 'user', 'perspective')
    list_filter = ['widget_name', 'perspective']


admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Object, ObjectAdmin)

admin.site.register(Module, ModuleAdmin)
admin.site.register(Perspective, PerspectiveAdmin)
admin.site.register(ModuleSetting, ModuleSettingAdmin)

admin.site.register(PageFolder, PageFolderAdmin)
admin.site.register(Page, PageAdmin)

admin.site.register(UpdateRecord, UpdateRecordAdmin)
admin.site.register(Widget, WidgetAdmin)
