# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

import oauth2 as oauth
from django.conf import settings
from django.http import HttpResponse

from treeio.core.api.auth.store import store, InvalidConsumerError, InvalidTokenError
from treeio.core.api.auth.utils import get_oauth_request, verify_oauth_request, require_params


class OAuthAuthentication(object):

    def __init__(self, realm='API', two_legged=False):
        self.realm = realm
        self.two_legged = two_legged

    def is_authenticated(self, request):
        oauth_request = get_oauth_request(request)
        missing_params = require_params(oauth_request)
        if missing_params is not None:
            return False

        if self.two_legged:
            return self._authenticate_two_legged(request, oauth_request)
        else:
            return self._authenticate_three_legged(request, oauth_request)

    def _authenticate_two_legged(self, request, oauth_request):
        #missing_params = require_params(oauth_request)
        # if missing_params is not None:
        #   return missing_params

        try:
            consumer = store.get_consumer(
                request, oauth_request, oauth_request['oauth_consumer_key'])
        except InvalidConsumerError:
            return False

        if not verify_oauth_request(request, oauth_request, consumer):
            return False

        request.user = store.get_user_for_consumer(
            request, oauth_request, consumer)
        request.consumer = consumer
        request.throttle_extra = consumer.key

        return True

    def _authenticate_three_legged(self, request, oauth_request):
        #missing_params = require_params(oauth_request, ('oauth_token',))
        # if missing_params is not None:
        #    return missing_params

        try:
            consumer = store.get_consumer(
                request, oauth_request, oauth_request['oauth_consumer_key'])
            access_token = store.get_access_token(
                request, oauth_request, consumer, oauth_request['oauth_token'])
        except (InvalidConsumerError, InvalidTokenError):
            return False

        if not verify_oauth_request(request, oauth_request, consumer, access_token):
            return False

        request.user = store.get_user_for_access_token(
            request, oauth_request, access_token)
        request.consumer = store.get_consumer_for_access_token(
            request, oauth_request, access_token)
        request.throttle_extra = request.consumer.key

        return True

    def challenge(self):
        """
        Returns a 401 response with a small bit on
        what OAuth is, and where to learn more about it.

        When this was written, browsers did not understand
        OAuth authentication on the browser side, and hence
        the helpful template we render. Maybe some day in the
        future, browsers will take care of this stuff for us
        and understand the 401 with the realm we give it.
        """
        response = HttpResponse()
        response.status_code = 401

        for k, v in oauth.build_authenticate_header(realm=self.realm).iteritems():
            response[k] = v

        response.content = """
            Unable to authenticate.
            Make sure you use oAuth 1.0 authentication and a valid consumer key.
             """

        return response


auth_engine_name = getattr(settings, 'HARDTREE_API_AUTH_ENGINE', 'oauth')
if auth_engine_name == 'oauth':
    auth_engine = OAuthAuthentication()
else:
    from piston.authentication import HttpBasicAuthentication
    auth_engine = HttpBasicAuthentication(realm='My sample API')
