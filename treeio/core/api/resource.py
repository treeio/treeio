# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- coding: utf-8 -*-

import sys
import utils
sys.modules['piston.utils'] = utils

from piston.resource import Resource


class CsrfExemptResource(Resource):

    """A Custom Resource that is csrf exempt"""

    def __init__(self, handler, authentication=None):
        super(CsrfExemptResource, self).__init__(handler, authentication)
        self.csrf_exempt = getattr(self.handler, 'csrf_exempt', True)

    def __call__(self, request, *args, **kwargs):
        res = super(CsrfExemptResource, self).__call__(
            request, *args, **kwargs)
        if hasattr(self.handler, 'status'):
            res.status_code = self.handler.status
            del self.handler.status
        return res
