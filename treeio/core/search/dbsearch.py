# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

from django.db.models import Q, get_models, CharField, TextField
from treeio.core.models import Object

params = []

for model in get_models():
    if issubclass(model, Object) and getattr(model, 'searcheable', True):
        for field in model._meta.fields:
            if isinstance(field, CharField) or isinstance(field, TextField):
                if 'password' not in field.name and 'object_name' not in field.name and 'object_type' not in field.name \
                        and 'nuvius' not in field.name:
                    params.append('%s__%s' % (model._meta.model_name, field.name))


def search(term):
    "Use database backend for searching"
    query = Q()
    # query_dict = {}
    attr = 'search'
    if term and term[0] == '*':
        attr = 'icontains'
        term = term[1:]
    for param in params:
        kwargs = {'%s__%s' % (param, attr): term}
        # query_dict[param] = term
        query = query | Q(**kwargs)

    # from pprint import pprint
    # pprint(query_dict)

    return Object.objects.filter(query)
