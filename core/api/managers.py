# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

from django.db import models
from django.contrib.auth.models import User
from treeio.core.conf import settings

KEY_SIZE = 18
SECRET_SIZE = 32

CONSUMER_DB = getattr(settings, 'HARDTREE_API_CONSUMER_DB', 'default')


class KeyManager(models.Manager):

    '''Add support for random key/secret generation
    '''

    def generate_random_codes(self):
        key = User.objects.make_random_password(length=KEY_SIZE)
        secret = User.objects.make_random_password(length=SECRET_SIZE)

        while self.filter(key__exact=key, secret__exact=secret).count():
            secret = User.objects.make_random_password(length=SECRET_SIZE)

        return key, secret


class ConsumerManager(KeyManager):

    def create_consumer(self, name, description=None, user=None, using=CONSUMER_DB):
        """
        Shortcut to create a consumer with random key/secret.
        """
        consumer, created = self.using(using).get_or_create(name=name)

        if user:
            consumer.user = user

        if description:
            consumer.description = description

        if created:
            consumer.key, consumer.secret = self.generate_random_codes()
            consumer.save()

        return consumer

    _default_consumer = None


class ResourceManager(models.Manager):
    _default_resource = None

    def get_default_resource(self, name):
        """
        Add cache if you use a default resource.
        """
        if not self._default_resource:
            self._default_resource = self.get(name=name)

        return self._default_resource


class TokenManager(KeyManager):

    def create_token(self, consumer_id, token_type, timestamp, user=None, using=None):
        """
        Shortcut to create a token with random key/secret.
        """
        if using:
            manager = self.using(using)
        else:
            manager = self

        token, created = manager.get_or_create(consumer_id=consumer_id,
                                               token_type=token_type,
                                               timestamp=timestamp,
                                               user=user)

        if created:
            token.key, token.secret = self.generate_random_codes()
            token.save()

        return token
