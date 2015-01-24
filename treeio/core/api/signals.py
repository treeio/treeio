# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license


def consumer_post_save(sender, instance, created, **kwargs):
    pass


def consumer_post_delete(sender, instance, **kwargs):
    instance.status = 'canceled'
    pass
