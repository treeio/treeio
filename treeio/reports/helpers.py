# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

import re
import pickle
import base64


def loads(value):
    "Unpickle a value"
    result = None
    try:
        result = pickle.loads(base64.b64decode((value)))
    except pickle.PickleError:
        pass
    return result


def dumps(value):
    "Pickle a value"
    return base64.b64encode(pickle.dumps(value, pickle.HIGHEST_PROTOCOL))


def average(values):
    """Computes the arithmetic mean of a list of numbers.

    >>> print average([20, 30, 70])
    40.0
    """
    return sum(values) / len(values) if values else 0


number_field_regex = re.compile('(Integer|Float|Decimal)Field$')

aggregate_functions = {'avg': {'description': 'AVG', 'function': average},
                       'sum': {'description': 'SUM', 'function': sum},
                       'max': {'description': 'MAX', 'function': max},
                       'min': {'description': 'MIN', 'function': min},
                       }
