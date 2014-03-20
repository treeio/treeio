# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Custom storage for Documents to allow dynamic MEDIA_ROOT paths
"""
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import SuspiciousOperation
from django.utils._os import safe_join
from treeio.core.conf import settings
import os


class FileStorage(FileSystemStorage):

    def path(self, name):
        try:
            path = safe_join(getattr(settings, 'MEDIA_ROOT'), name)
        except ValueError:
            raise SuspiciousOperation(
                "Attempted access to '%s' denied." % name)
        return os.path.normpath(path)
