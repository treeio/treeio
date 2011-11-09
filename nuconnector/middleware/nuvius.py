# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Nuvius middleware: saves nuvius_id for the session when specified
"""
from treeio.core.conf import settings
from nuconnector.connector import Connector

class NuviusMiddleware():
    "Stores nuvius_id within the session when possible"
    
    def process_request(self, request):
        "If nuvius_id within GET parameters of the request, store the ID within Django session"
        nuvius_id = request.GET.get('nuvius_id', None)
        if nuvius_id:
            if getattr(settings, 'NUVIUS_CHECK_USER_KEYS', True):
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
