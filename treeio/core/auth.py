# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Hardtree support authentication backend
"""
from django.contrib.auth.models import User
from treeio.identities.models import ContactValue


class EmailBackend:

    "Log a user in using email instead of their username"

    def authenticate(self, username, password):
        # The user entered an email, so try to log them in by e-mail
        emails = ContactValue.objects.filter(value=username,
                                             field__field_type='email',
                                             contact__trash=False,
                                             contact__related_user__isnull=False)
        for email in emails:
            try:
                user = email.contact.related_user.user.user
                if user.check_password(password):
                    return user
            except:
                pass
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class HashBackend:

    "Log a user in using their password as a hash"

    def authenticate(self, authkey):
        try:
            return User.objects.get(password=authkey)
        except:
            pass
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
