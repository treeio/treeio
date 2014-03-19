# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Conversion rules for AJAX response
"""

import re


def title(page, response):
    "Extract <title></title>"

    regexp = r"<head>.*?<title>(?P<title>.*?)</title>.*?</head>"
    blocks = re.finditer(regexp, page, re.DOTALL)
    for block in blocks:
        response['title'] = block.group('title')

    return response


def module_content(page, response):
    "Extract module_content"

    regexp = r"<!-- module_content -->(?P<module_content>.*?)<!-- /module_content -->"
    blocks = re.finditer(regexp, page, re.DOTALL)
    for block in blocks:
        response['module_content'] = block.group('module_content').strip()

    return response

RULESET = [title,
           module_content,
           ]


def apply_rules(page, response={}):
    "Applies all rules"

    for rule in RULESET:
        response = rule(page, response)

    return response
