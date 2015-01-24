# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
News: test suites
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, Perspective, ModuleSetting


class NewsViewsTest(TestCase):

    "Finance functional tests for views"

    username = "test"
    password = "password"
    prepared = False

    def setUp(self):
        "Initial Setup"
        if not self.prepared:
            self.group, created = Group.objects.get_or_create(name='test')
            duser, created = DjangoUser.objects.get_or_create(
                username=self.username)
            duser.set_password(self.password)
            duser.save()
            self.user, created = User.objects.get_or_create(user=duser)
            self.user.save()
            perspective, created = Perspective.objects.get_or_create(
                name='default')
            perspective.set_default_user()
            perspective.save()
            ModuleSetting.set('default_perspective', perspective.id)

            self.client = Client()

            self.prepared = True

    ######################################
    # Testing views when user is logged in
    ######################################
    def test_news_index_login(self):
        "Test index page with login at /news/all/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('news_index'))
        self.assertEquals(response.status_code, 200)

    def test_news_top(self):
        "Test index page with login at /news/top/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('news_top'))
        self.assertEquals(response.status_code, 200)

    def test_news_my_activity(self):
        "Test index page with login at /news/my/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('news_my_activity'))
        self.assertEquals(response.status_code, 200)

    def test_news_watchlist(self):
        "Test index page with login at /news/watchlist/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('news_my_watchlist'))
        self.assertEquals(response.status_code, 200)

    ######################################
    # Testing views when user is not logged in
    ######################################
    def test_news_index(self):
        "Testing /news/"
        response = self.client.get(reverse('news'))
        # Redirects as unauthenticated
        self.assertRedirects(response, "/accounts/login")

    def test_news_top_out(self):
        "Testing /news/top/"
        response = self.client.get(reverse('news_top'))
        self.assertRedirects(response, reverse('user_login'))

    def test_news_my_activity_out(self):
        "Testing /news/my/"
        response = self.client.get(reverse('news_my_activity'))
        self.assertRedirects(response, reverse('user_login'))

    def test_news_watchlist_out(self):
        "Testing /news/watchlist/"
        response = self.client.get(reverse('news_my_watchlist'))
        self.assertRedirects(response, reverse('user_login'))
