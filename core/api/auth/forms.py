# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

from django import forms


class AuthorizeRequestTokenForm(forms.Form):
    oauth_token = forms.CharField(widget=forms.HiddenInput)
    authorize_access = forms.BooleanField(required=True)
