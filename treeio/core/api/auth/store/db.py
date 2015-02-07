# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

import oauth2 as oauth

from treeio.core.api.auth.store import InvalidConsumerError, InvalidTokenError, Store
from treeio.core.api.models import Nonce, Token, Consumer, VERIFIER_SIZE
from treeio.core.conf import settings


class ModelStore(Store):

    """
    Store implementation using the Django models defined in `piston.models`.
    """

    def get_consumer(self, request, oauth_request, consumer_key):
        try:
            consumer_db = getattr(
                settings, 'HARDTREE_API_CONSUMER_DB', 'default')
            return Consumer.objects.using(consumer_db).get(key=consumer_key)
        except Consumer.DoesNotExist:
            raise InvalidConsumerError()

    def get_consumer_for_request_token(self, request, oauth_request, request_token):
        consumer_db = getattr(settings, 'HARDTREE_API_CONSUMER_DB', 'default')
        return Consumer.objects.using(consumer_db).get(pk=request_token.consumer_id)

    def get_consumer_for_access_token(self, request, oauth_request, access_token):
        consumer_db = getattr(settings, 'HARDTREE_API_CONSUMER_DB', 'default')
        return Consumer.objects.using(consumer_db).get(pk=access_token.consumer_id)

    def create_request_token(self, request, oauth_request, consumer, callback):
        consumer_db = getattr(settings, 'HARDTREE_API_CONSUMER_DB', 'default')
        token = Token.objects.create_token(
            token_type=Token.REQUEST,
            consumer_id=Consumer.objects.using(consumer_db).get(
                key=oauth_request['oauth_consumer_key']).id,
            timestamp=oauth_request['oauth_timestamp'],
            using=consumer_db
        )
        token.set_callback(callback)
        token.save()

        return token

    def fetch_request_token(self, request, oauth_request, request_token_key):
        try:
            consumer_db = getattr(
                settings, 'HARDTREE_API_CONSUMER_DB', 'default')
            token = Token.objects.using(consumer_db).get(
                key=request_token_key, token_type=Token.REQUEST)
            token.save(
                using=getattr(settings, 'CURRENT_DATABASE_NAME', 'default'))
            return token
        except Token.DoesNotExist:
            raise InvalidTokenError()

    def get_request_token(self, request, oauth_request, request_token_key):
        try:
            consumer_db = getattr(
                settings, 'HARDTREE_API_CONSUMER_DB', 'default')
            return Token.objects.using(consumer_db).get(key=request_token_key, token_type=Token.REQUEST)
        except Token.DoesNotExist:
            raise InvalidTokenError()

    def authorize_request_token(self, request, oauth_request, request_token):
        request_token.is_approved = True
        request_token.user = request.user
        request_token.verifier = oauth.generate_verifier(VERIFIER_SIZE)
        request_token.save()
        return request_token

    def create_access_token(self, request, oauth_request, consumer, request_token):
        consumer_db = getattr(settings, 'HARDTREE_API_CONSUMER_DB', 'default')
        access_token = Token.objects.create_token(
            token_type=Token.ACCESS,
            timestamp=oauth_request['oauth_timestamp'],
            consumer_id=Consumer.objects.using(
                consumer_db).get(key=consumer.key).id,
            user=request_token.user,
        )
        request_token.delete()
        return access_token

    def get_access_token(self, request, oauth_request, consumer, access_token_key):
        try:
            return Token.objects.get(key=access_token_key, token_type=Token.ACCESS)
        except Token.DoesNotExist:
            raise InvalidTokenError()

    def get_user_for_access_token(self, request, oauth_request, access_token):
        return access_token.user

    def get_user_for_consumer(self, request, oauth_request, consumer):
        return consumer.user

    def check_nonce(self, request, oauth_request, nonce):
        nonce, created = Nonce.objects.get_or_create(
            consumer_key=oauth_request['oauth_consumer_key'],
            token_key=oauth_request.get('oauth_token', ''),
            key=nonce
        )
        return created
