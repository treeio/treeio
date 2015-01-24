# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Multitenancy settings
"""

from django.conf import LazySettings
from pandora import box


class Settings(LazySettings):

    def __getattr__(self, key):
        if key in box:
            return box[key]
        else:
            return super(Settings, self).__getattr__(key)

settings = Settings()
