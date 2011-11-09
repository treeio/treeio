# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Nuvius profile views
"""
from treeio.core.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from nuconnector import Connector
from treeio.core.models import ModuleSetting
from treeio.core.decorators import treeio_login_required, handle_response_format
import simplejson as json

@treeio_login_required
def profile_check(request):
    "If nuvius_id within GET parameters of the request, store the ID within Django session"
    nuvius_id = request.GET.get('nuvius_id', None)
    if nuvius_id:
        nuvius_key = request.GET.get('profile_key', None)
        if nuvius_key:
            con = Connector(profile_id=nuvius_id, profile_key=nuvius_key)
            profile = con.get_profile()
            try:
                if profile['key_valid']:
                    request.session['nuvius_id'] = nuvius_id
                    request.session['nuvius_profile_key'] = nuvius_key
            except KeyError:
                pass
        else:
            request.session['nuvius_id'] = nuvius_id
    
    response = HttpResponse(json.dumps(profile), mimetype='application/json')
    
    # Hardtree code
    if 'applications' in profile:
        del profile['applications']
    if 'bindings' in profile:
        del profile['bindings']
    user = request.user.get_profile()
    conf = ModuleSetting.set('nuvius_profile', '', user=user)
    conf.dumps(profile).save()
    # End of Hardtree code
    
    return response

@treeio_login_required
@handle_response_format
def profile_reset(request, response_format='html'):
    "Resets Nuvius_profile for the current account"
    
    next = '/'
    if 'next' in request.GET:
        next = request.GET.get('next')
    
    user = request.user.get_profile()
    conf = ModuleSetting.get('nuvius_profile', user=user)
    if conf:
        conf.delete()
    
    return HttpResponseRedirect(next)
    
    
