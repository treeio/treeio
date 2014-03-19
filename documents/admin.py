# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Documents Admin
"""
from treeio.documents.models import Folder, File, Document, WebLink
from django.contrib import admin


class FolderAdmin(admin.ModelAdmin):

    "FolderAdmin"
    list_display = ('name', 'parent')
    search_fields = ['name']


class FileAdmin(admin.ModelAdmin):

    "FileAdmin"
    list_display = ('name', 'folder')
    list_filter = ['folder']
    search_fields = ['name']


class DocumentAdmin(admin.ModelAdmin):

    "DocumentAdmin"
    list_display = ('title', 'folder')
    list_filter = ['folder']
    search_fields = ['title']


class WebLinkAdmin(admin.ModelAdmin):

    "WeblinkAdmin"
    list_display = ('title', 'folder', 'url')
    list_filter = ['folder']
    search_fields = ['title']

admin.site.register(Folder, FolderAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(WebLink, WebLinkAdmin)
