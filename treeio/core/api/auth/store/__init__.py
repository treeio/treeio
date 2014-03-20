# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import importlib


class Error(Exception):

    """Base class for Store exceptions."""


class InvalidConsumerError(Error):

    """Invalid consumer."""


class InvalidTokenError(Error):

    """Invalid token."""


class Store(object):

    """
    The Store class is the backbone of piston's OAuth implementation. It is used
    by the views and the authentication backend to get consumers and tokens, and
    to create tokens. The following terms are used in the documentation of the
    API:

    Consumer:
        A class defining at minimum `key` and `secret` attributes. Both of these
        attributes must be either str or unicode.

    Token:
        A class defining at minimum `key` and `secret` attributes. Both of these
        attributes must be either str or unicode.

    User:
        A `django.contrib.auth.models.User` instance.

    Any API that takes a consumer or token will be passed a Consumer or Token
    instance it itself returned at an earlier stage from one of the methods that
    take a key and return a Consumer or Token. This means if your store
    implementation uses tokens that keep a reference to its Consumer on the
    Token itself, `get_consumer_for_request_token` can simply return
    `request_token.consumer`.
    """

    def get_consumer(self, request, oauth_request, consumer_key):
        """
        Return the Consumer for `consumer_key` or raise `InvalidConsumerError`.

        `request`: The Django request object.
        `oauth_request`: The `oauth2.Request` object.
        `consumer_key`: The consumer key.
        """
        raise NotImplementedError

    def get_consumer_for_request_token(self, request, oauth_request, request_token):
        """
        Return the Consumer associated with the `request_token` Token.

        `request`: The Django request object.
        `oauth_request`: The `oauth2.Request` object.
        `request_token`: The request token to get the consumer for.
        """
        raise NotImplementedError

    def get_consumer_for_access_token(self, request, oauth_request, access_token):
        """
        Return the Consumer associated with the `access_token` Token.

        `request`: The Django request object.
        `oauth_request`: The `oauth2.Request` object.
        `access_token`: The access Token to get the consumer for.
        """
        raise NotImplementedError

    def create_request_token(self, request, oauth_request, consumer, callback):
        """
        Generate and return a Token.

        `request`: The Django request object.
        `oauth_request`: The `oauth2.Request` object.
        `consumer`: The Consumer that made the request.
        """
        raise NotImplementedError

    def get_request_token(self, request, oauth_request, request_token_key):
        """
        Return the Token for `request_token_key` or raise `InvalidTokenError`.

        `request`: The Django request object.
        `oauth_request`: The `oauth2.Request` object.
        `consumer`: The Consumer that made the request.
        `request_token_key`: The request token key.
        """
        raise NotImplementedError

    def authorize_request_token(self, request, oauth_request, request_token):
        """
        Authorize the `request_token` Token and return it.

        `request`: The Django request object.
        `oauth_request`: The `oauth2.Request` object.
        `request_token`: The request token to authorize.
        """
        raise NotImplementedError

    def create_access_token(self, request, oauth_request, consumer, request_token):
        """
        Generate and return a Token.

        `request`: The Django request object.
        `oauth_request`: The `oauth2.Request` object.
        `consumer`: The Consumer that made the request.
        `request_token`: The Token used to make the request.
        """
        raise NotImplementedError

    def get_access_token(self, request, oauth_request, consumer, access_token_key):
        """
        Return the Token for `access_token_key` or raise `InvalidTokenError`.

        `request`: The Django request object.
        `oauth_request`: The `oauth2.Request` object.
        `consumer`: The Consumer that made the request.
        `access_token_key`: The token key used to make the request.
        """
        raise NotImplementedError

    def get_user_for_access_token(self, request, oauth_request, access_token):
        """
        Return the associated User for `access_token`.

        `request`: The Django request object.
        `oauth_request`: The `oauth2.Request` object.
        `consumer`: The Consumer that made the request.
        `access_token`: The Token used to make the request.
        """
        raise NotImplementedError

    def get_user_for_consumer(self, request, oauth_request, consumer):
        """
        Return the associated User for `consumer`.

        `request`: The Django request object.
        `oauth_request`: The `oauth2.Request` object.
        `consumer`: The Consumer that made the request.
        """
        raise NotImplementedError

    def check_nonce(self, request, oauth_request, nonce):
        """
        Return `True` if the nonce has not yet been used, `False` otherwise.

        `request`: The Django request object.
        `oauth_request`: The `oauth2.Request` object.
        `nonce`: The nonce to check.
        """
        raise NotImplementedError


def get_store(path='treeio.core.api.auth.store.db.ModelStore'):
    """
    Load the piston oauth store. Should not be called directly unless testing.
    """
    path = getattr(settings, 'PISTON_OAUTH_STORE', path)

    try:
        module, attr = path.rsplit('.', 1)
        store_class = getattr(importlib.import_module(module), attr)
    except ValueError:
        raise ImproperlyConfigured(
            'Invalid piston oauth store string: "%s"' % path)
    except ImportError, e:
        raise ImproperlyConfigured(
            'Error loading piston oauth store module "%s": "%s"' % (module, e))
    except AttributeError:
        raise ImproperlyConfigured(
            'Module "%s" does not define a piston oauth store named "%s"' % (module, attr))

    return store_class()


store = get_store()
