# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Documents module objects
"""
from django.db import models
from django.core.urlresolvers import reverse
from treeio.core.models import Object
from treeio.core.conf import settings
from treeio.documents.files import FileStorage
import os
import time
import re

# Folder model


class Folder(Object):

    """ Every folder may have a parent folder """
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='child_set')

    access_inherit = ('parent', '*module', '*user')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        try:
            return reverse('documents_folder_view', args=[self.id])
        except Exception:
            return ""


def generate_filename(instance, old_filename):
    """ Generate filename """
    extension = os.path.splitext(old_filename)[1]
    filename = str(time.time()) + extension
    return 'documents/files/' + filename


# File model
class File(Object):

    """ A binary or other non-renderable file (i.e. an image) """
    name = models.CharField(max_length=255)
    folder = models.ForeignKey(Folder)
    content = models.FileField(
        upload_to=generate_filename, storage=FileStorage())

    access_inherit = ('folder', '*module', '*user')

    def __unicode__(self):
        return self.name

    def get_file_type(self):
        match = re.match('.*\.(?P<extension>[a-z]+)', unicode(self.content))
        if match:
            return unicode(match.group('extension')).upper()
        else:
            return ''

    def can_preview(self):
        filetype = self.get_file_type()
        for ext in ('PNG', 'JPG', 'JPEG', 'BMP', 'GIF', 'SVG'):
            if filetype == ext:
                return True
        return False

    def get_preview_url(self):
        return getattr(settings, 'MEDIA_URL', '/static/media/') + unicode(self.content)

    class Meta:

        " File "
        ordering = ['-last_updated']

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        try:
            return reverse('documents_file_view', args=[self.id])
        except Exception:
            return ""


# Document model
class Document(Object):

    """ A readable document, i.e. HTML, which may be rendered directly """
    title = models.CharField(max_length=255)
    folder = models.ForeignKey(Folder)
    body = models.TextField(null=True, blank=True)

    access_inherit = ('folder', '*module', '*user')

    def __unicode__(self):
        return self.title

    class Meta:

        " File "
        ordering = ['-last_updated']

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        try:
            return reverse('documents_document_view', args=[self.id])
        except Exception:
            return ""

# WebLink model


class WebLink(Object):

    """ A web link """
    title = models.CharField(max_length=255)
    folder = models.ForeignKey(Folder)
    url = models.CharField(max_length=255)

    access_inherit = ('folder', '*module', '*user')

    def __unicode__(self):
        return self.title

    class Meta:

        " File "
        ordering = ['-last_updated']

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        try:
            return reverse('documents_weblink_view', args=[self.id])
        except Exception:
            return ""
