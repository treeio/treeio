# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core Search module model hooks
"""

import os
from django.db.models import signals
from treeio.core.conf import settings
from treeio.core.models import Object
from whoosh import index


def create_index(sender=None, **kwargs):
    "Create initial (empty) search index"
    if not os.path.exists(settings.WHOOSH_INDEX):
        os.mkdir(settings.WHOOSH_INDEX)
    index.create_in(settings.WHOOSH_INDEX, schema=settings.WHOOSH_SCHEMA)

if not settings.SEARCH_DISABLED and getattr(settings, 'SEARCH_ENGINE', 'whoosh') == 'whoosh':
    signals.post_syncdb.connect(create_index)


def update_index(sender, instance, created, **kwargs):
    "Add Object to search index"
    if isinstance(instance, Object) and instance.is_searchable():
        search_item = instance.get_search_item()
        ix = index.open_dir(settings.WHOOSH_INDEX)
        try:
            writer = ix.writer()
            try:
                if created:
                    writer.add_document(id=search_item['id'],
                                        name=search_item['name'],
                                        type=search_item['type'],
                                        content=search_item['content'],
                                        url=unicode(search_item['url']))
                    writer.commit()
                else:
                    writer.update_document(id=search_item['id'],
                                           name=search_item['name'],
                                           type=search_item['type'],
                                           content=search_item['content'],
                                           url=search_item['url'])
                    writer.commit()
            except:
                writer.cancel()
        except:
            pass

if not settings.SEARCH_DISABLED and getattr(settings, 'SEARCH_ENGINE', 'whoosh') == 'whoosh':
    signals.post_save.connect(update_index)


def delete_index(sender, instance, **kwargs):
    "Delete Object from search index"

    if isinstance(instance, Object) and instance.is_searchable():
        ix = index.open_dir(settings.WHOOSH_INDEX)
        try:
            writer = ix.writer()
            try:
                writer.delete_by_term(u'id', unicode(instance.id))
                writer.commit()
            except:
                writer.cancel()
        except:
            pass

if not settings.SEARCH_DISABLED and getattr(settings, 'SEARCH_ENGINE', 'whoosh') == 'whoosh':
    signals.post_delete.connect(delete_index)
