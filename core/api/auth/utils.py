# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

import oauth2 as oauth
from django.http import HttpResponse


def get_oauth_request(request):
    """ Converts a Django request object into an `oauth2.Request` object. """
    headers = {}
    if 'HTTP_AUTHORIZATION' in request.META:
        headers['Authorization'] = request.META['HTTP_AUTHORIZATION']
    return oauth.Request.from_request(request.method, request.build_absolute_uri(request.path), headers, dict(request.REQUEST))


def verify_oauth_request(request, oauth_request, consumer, token=None):
    """ Helper function to verify requests. """
    from treeio.core.api.auth.store import store

    # Check nonce
    if not store.check_nonce(request, oauth_request, oauth_request['oauth_nonce']):
        return False

    # Verify request
    try:
        oauth_server = oauth.Server()
        oauth_server.add_signature_method(oauth.SignatureMethod_HMAC_SHA1())
        oauth_server.add_signature_method(oauth.SignatureMethod_PLAINTEXT())

        # Ensure the passed keys and secrets are ascii, or HMAC will complain.
        consumer = oauth.Consumer(consumer.key.encode(
            'ascii', 'ignore'), consumer.secret.encode('ascii', 'ignore'))
        if token is not None:
            token = oauth.Token(
                token.key.encode('ascii', 'ignore'), token.secret.encode('ascii', 'ignore'))

        oauth_server.verify_request(oauth_request, consumer, token)
    except oauth.Error:
        return False

    return True


def require_params(oauth_request, parameters=[]):
    """ Ensures that the request contains all required parameters. """
    params = [
        'oauth_consumer_key',
        'oauth_nonce',
        'oauth_signature',
        'oauth_signature_method',
        'oauth_timestamp'
    ]
    params.extend(parameters)

    missing = list(
        param for param in params if not oauth_request or param not in oauth_request)
    if missing:
        response = HttpResponse(
            'Missing OAuth parameters: %s' % (', '.join(missing)))
        response.status_code = 401
        return response

    return None
