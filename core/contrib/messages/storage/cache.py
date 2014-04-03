# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

# -*- coding:utf-8 -*-

from treeio.core.conf import settings
from django.contrib.messages.storage.base import BaseStorage
from django.core.cache import cache
import cPickle


def lock(key):
    while True:
        if cache.add(key + '_lock', '1', 10):  # lifetime lock 10 seconds
            break


def unlock(key):
    cache.delete(key + '_lock')


class CacheStorage(BaseStorage):

    """
    Stores messages in a cache.
    """

    def __init__(self, request, *args, **kwargs):
        super(CacheStorage, self).__init__(request, *args, **kwargs)
        self.user = request.user.id
        self.domain = getattr(settings, 'CURRENT_DOMAIN', 'default')
        self.prefix = 'treeio_%s_storage_messages_%s'
        self.key = self.prefix % (self.domain, self.user)

    def _get(self, *args, **kwargs):
        """
        Retrieves a list of stored messages. Returns a tuple of the messages
        and a flag indicating whether or not all the messages originally
        intended to be stored in this storage were, in fact, stored and
        retrieved; e.g., ``(messages, all_retrieved)``.
        """
        lock(self.key)
        try:
            data = cache.get(self.key)
            if not data:
                data = cPickle.dumps([])
            messages = cPickle.loads(data)
        except:
            pass
        unlock(self.key)
        return messages, True

    def update(self, response, *args, **kwargs):
        "Update flew by - don't pass response to avoid Exceptions being thrown by Django middleware"
        super(CacheStorage, self).update(response, *args, **kwargs)
        return []

    def _store(self, messages, *args, **kwargs):
        """
        Stores a list of messages, returning a list of any messages which could
        not be stored.

        One type of object must be able to be stored, ``Message``.
        """
        lock(self.key)
        try:
            if messages:
                data = cache.get(self.key)
                if not data:  # if not data in cache
                    data = cPickle.dumps(([], True))
                data = cPickle.loads(data)
                data.append(messages)
                cache.set(self.key, cPickle.dumps(messages), 2592000)
            else:
                cache.set(self.key, cPickle.dumps([]), 2592000)
        except:
            pass
        unlock(self.key)
        return messages

    def _add(self, messages, *args, **kwargs):
        """
        adds to the message store
        """
        lock(self.key)
        try:
            if messages:
                data = cache.get(self.key)
                if not data:
                    data = cPickle.dumps([])
                data = cPickle.loads(data)
                data.append(messages)
                cache.set(self.key, cPickle.dumps(data), 2592000)
        except:
            pass
        unlock(self.key)
