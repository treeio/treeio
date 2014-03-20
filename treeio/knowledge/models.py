# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Knowledge base module objects
"""
from django.db import models
from treeio.core.models import Object
from django.core.urlresolvers import reverse
from django.template import defaultfilters
from unidecode import unidecode

# KnowledgeFolder model


class KnowledgeFolder(Object):

    """ KnowledgeFolder """
    name = models.CharField(max_length=255)
    details = models.TextField(max_length=255, null=True, blank=True)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='child_set')
    treepath = models.CharField(max_length=800)

    access_inherit = ('parent', '*module', '*user')

    def __unicode__(self):
        return self.name

    class Meta:

        " Type "
        ordering = ['name']

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        try:
            return reverse('knowledge_folder_view', args=[self.treepath])
        except Exception:
            return ""

    def treewalk(self, save=True):
        "Walks up the tree to construct Type treepath"
        treepath = ''

        for folder in self.get_tree_path():
            slug = unicode(folder.name).replace(" ", "-")
            slug = defaultfilters.slugify(unidecode(slug))
            treepath += slug + "/"
        self.treepath = treepath

        if save:
            self.save()
        return self

    def by_path(treePath):
        "Returns a KnowledgeFolder instance matching the given treepath"
        folder = KnowledgeFolder.objects.filter(treepath=unicode(treePath))
        if folder:
            folder = folder[0]
        else:
            folder = None

        return folder
    by_path = staticmethod(by_path)

    def save(self, *args, **kwargs):
        "Overridden save() method to compute treepath and full names"
        self.treewalk(save=False)
        super(KnowledgeFolder, self).save(*args, **kwargs)


# KnowledgeCategory model
class KnowledgeCategory(Object):

    """ Knowledge Category that contains Knowledge Items"""
    name = models.CharField(max_length=255)
    details = models.TextField(max_length=255, null=True, blank=True)
    treepath = models.CharField(max_length=800)

    def __unicode__(self):
        return self.name

    class Meta:

        " Category "
        ordering = ['name']

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        try:
            return reverse('knowledge_category_view', args=[self.treepath])
        except Exception:
            return ""

    def treewalk(self, save=True):
        "Walks up the tree to construct Category"
        slug = unicode(self.name).replace(" ", "-")
        slug = defaultfilters.slugify(unidecode(slug))
        treepath = slug + "/"

        self.treepath = treepath

        if save:
            self.save()
        return self

    def by_path(path):
        "Returns a Knowledge Category instance matching the given treepath"
        category = KnowledgeCategory.objects.filter(treepath=unidecode(path))

        if category:
            category = category[0]
        else:
            category = None

        return category
    by_path = staticmethod(by_path)

    def save(self, *args, **kwargs):
        "Overridden save() method to compute treepath and full names"
        self.treewalk(save=False)
        super(KnowledgeCategory, self).save(*args, **kwargs)

# KnowledgeItem model


class KnowledgeItem(Object):

    """" A readable piece of knowledge """
    name = models.CharField(max_length=255)
    folder = models.ForeignKey(KnowledgeFolder)
    category = models.ForeignKey(
        KnowledgeCategory, blank=True, null=True, on_delete=models.SET_NULL)
    body = models.TextField(null=True, blank=True)
    treepath = models.CharField(max_length=800)

    access_inherit = ('folder', '*module', '*user')

    def __unicode__(self):
        return self.name

    class Meta:

        " Item "
        ordering = ['-last_updated']

    def get_absolute_url(self):
        "Returns absolute URL of the object"
        try:
            return reverse('knowledge_item_view', args=[self.folder.treepath, self.treepath])
        except Exception:
            return ""

    def treewalk(self, save=True):
        "Walks up the tree to construct both Item treepath and item.name from database"
        slug = unicode(self.name).replace(" ", "-")
        slug = defaultfilters.slugify(unidecode(slug))
        treepath = slug + "/"

        self.treepath = treepath

        if save:
            self.save()
        return self

    def by_path(treePath, itemPath):
        "Returns a Knowledge Item instance matching the given treepath"
        folder = KnowledgeFolder.by_path(unidecode(treePath))
        item = KnowledgeItem.objects.filter(
            treepath=unidecode(itemPath), folder=folder)

        if item:
            item = item[0]
        else:
            item = None

        return item
    by_path = staticmethod(by_path)

    def save(self, *args, **kwargs):
        "Overridden save() method to compute treepath and full names"
        self.treewalk(save=False)
        super(KnowledgeItem, self).save(*args, **kwargs)
