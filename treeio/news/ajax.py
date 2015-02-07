# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
News ajax views
"""


from dajaxice.core import dajaxice_functions
from dajax.core import Dajax
from django.template import RequestContext
from django.db.models import Q
from treeio.core.rendering import render_to_string
from treeio.core.models import UpdateRecord
from treeio.news.views import _get_filter_query


def get_more(request, target='#more-news', skip=20):
    dajax = Dajax()

    profile = request.user.get_profile()
    query = _get_filter_query(profile) & (
        ~Q(author=profile) | Q(record_type='share') | Q(score__gt=0))
    updates = UpdateRecord.objects.filter(query).distinct()[skip:skip + 20]

    output = render_to_string('news/ajax/index',
                              {'updates': updates, 'skip': skip + 20},
                              context_instance=RequestContext(request),
                              response_format='html')

    dajax.add_data({'target': target, 'content': output}, 'treeio.add_data')
    return dajax.json()

dajaxice_functions.register(get_more)
