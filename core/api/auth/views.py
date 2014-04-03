# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

from urllib import urlencode

from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import RequestSite
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from treeio.core.rendering import render_to_response
from treeio.core.api.auth.forms import AuthorizeRequestTokenForm
from treeio.core.api.auth.store import store, InvalidConsumerError, InvalidTokenError
from treeio.core.api.auth.utils import verify_oauth_request, get_oauth_request, require_params


@csrf_exempt
def get_request_token(request):
    oauth_request = get_oauth_request(request)

    missing_params = require_params(oauth_request, ('oauth_callback',))
    if missing_params is not None:
        return missing_params

    try:
        consumer = store.get_consumer(
            request, oauth_request, oauth_request['oauth_consumer_key'])
    except InvalidConsumerError:
        return HttpResponseBadRequest('Invalid Consumer.')

    if not verify_oauth_request(request, oauth_request, consumer):
        return HttpResponseBadRequest('Could not verify OAuth request.')

    request_token = store.create_request_token(
        request, oauth_request, consumer, oauth_request['oauth_callback'])

    ret = urlencode({
        'oauth_token': request_token.key,
        'oauth_token_secret': request_token.secret,
        'oauth_callback_confirmed': 'true'
    })
    return HttpResponse(ret, content_type='application/x-www-form-urlencoded')


@login_required
def authorize_request_token(request, form_class=AuthorizeRequestTokenForm, template_name='core/api/auth/authorize', verification_template_name='core/api/auth/authorize_verification_code'):
    if 'oauth_token' not in request.REQUEST:
        return HttpResponseBadRequest('No request token specified.')

    oauth_request = get_oauth_request(request)

    try:
        request_token = store.fetch_request_token(
            request, oauth_request, request.REQUEST['oauth_token'])
    except InvalidTokenError:
        return HttpResponseBadRequest('Invalid request token.')

    consumer = store.get_consumer_for_request_token(
        request, oauth_request, request_token)

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid() and form.cleaned_data['authorize_access']:
            request_token = store.authorize_request_token(
                request, oauth_request, request_token)
            if request_token.callback is not None and request_token.callback != 'oob':
                domain = RequestSite(request).domain
                return HttpResponseRedirect('%s&%s' % (request_token.get_callback_url(), urlencode({'oauth_token': request_token.key, 'domain': domain})))
            else:
                return render_to_response(verification_template_name,
                                          {'consumer': consumer,
                                              'verification_code': request_token.verifier},
                                          context_instance=RequestContext(request), response_format='html')
    else:
        form = form_class(initial={'oauth_token': request_token.key})

    return render_to_response(template_name, {'consumer': consumer, 'form': form},
                              context_instance=RequestContext(request), response_format='html')


@csrf_exempt
def get_access_token(request):
    oauth_request = get_oauth_request(request)

    missing_params = require_params(
        oauth_request, ('oauth_token', 'oauth_verifier'))
    if missing_params is not None:
        return missing_params

    try:
        consumer = store.get_consumer(
            request, oauth_request, oauth_request['oauth_consumer_key'])
        request_token = store.get_request_token(
            request, oauth_request, oauth_request['oauth_token'])
    except InvalidTokenError:
        return HttpResponseBadRequest('Invalid consumer.')
    except InvalidConsumerError:
        return HttpResponseBadRequest('Invalid request token.')

    if not verify_oauth_request(request, oauth_request, consumer, request_token):
        return HttpResponseBadRequest('Could not verify OAuth request.')

    if oauth_request.get('oauth_verifier', None) != request_token.verifier:
        return HttpResponseBadRequest('Invalid OAuth verifier.')

    access_token = store.create_access_token(
        request, oauth_request, consumer, request_token)

    ret = urlencode({
        'oauth_token': access_token.key,
        'oauth_token_secret': access_token.secret
    })
    return HttpResponse(ret, content_type='application/x-www-form-urlencoded')
