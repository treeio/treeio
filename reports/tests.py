# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Reports: test suites
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from treeio.core.models import User, Group, Perspective, ModuleSetting
from treeio.reports.models import Report, Chart


class ReportsModelsTest(TestCase):

    "Reports Models Tests"

    def test_model_report(self):
        "Test Report Model"
        obj = Report(name='test')
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()

    def test_model_chart(self):
        "Test Chart Model"
        report = Report(name='test')
        report.save()
        obj = Chart(name='test', report=report)
        obj.save()
        self.assertEquals('test', obj.name)
        self.assertNotEquals(obj.id, None)
        obj.delete()


class ReportsViewsTest(TestCase):

    "Reports functional tests for views"

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

            self.report = Report(name='test')
            self.report.set_default_user()
            self.report.save()

            self.chart = Chart(name='test_chart', report=self.report)
            self.chart.set_default_user()
            self.chart.save()

            self.client = Client()

            self.prepared = True

    ######################################
    # Testing views when user is logged in
    ######################################
    def test_reports_login(self):
        "Testing /reports/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('reports'))
        self.assertEquals(response.status_code, 200)

    def test_index_login(self):
        "Testing /reports/index/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('reports_index'))
        self.assertEquals(response.status_code, 200)

    def test_index_owned(self):
        "Testing /reports/owned/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('reports_index'))
        self.assertEquals(response.status_code, 200)

    # Charts
    def test_chart_add(self):
        "Testing /reports/chart/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('reports_chart_add'))
        self.assertEquals(response.status_code, 200)

    def test_chart_delete_login(self):
        "Testing /reports/chart/delete/<chart_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('reports_chart_delete', args=[self.chart.id]))
        self.assertEquals(response.status_code, 200)

    # Reports
    def test_report_add(self):
        "Testing /reports/report/add/"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('reports_report_add'))
        self.assertEquals(response.status_code, 200)

    def test_report_delete_login(self):
        "Testing /reports/report/delete/<report_id>"
        response = self.client.post('/accounts/login',
                                    {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        response = self.client.get(
            reverse('reports_report_delete', args=[self.report.id]))
        self.assertEquals(response.status_code, 200)

    ######################################
    # Testing views when user is not logged in
    ######################################
    def test_reports_out(self):
        "Testing /reports/"
        response = self.client.get(reverse('reports'))
        self.assertRedirects(response, reverse('user_login'))

    def test_index_out(self):
        "Testing /reports/index/"
        response = self.client.get(reverse('reports_index'))
        self.assertRedirects(response, reverse('user_login'))

    def test_index_owned_out(self):
        "Testing /reports/owned/"
        response = self.client.get(reverse('reports_index'))
        self.assertRedirects(response, reverse('user_login'))

    # Charts
    def test_chart_add_out(self):
        "Testing /reports/chart/add/"
        response = self.client.get(reverse('reports_chart_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_chart_add_typed_out(self):
        "Testing /reports/chart/add/<report_id>"
        response = self.client.get(
            reverse('reports_chart_add', args=[self.report.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_chart_edit_out(self):
        "Testing /reports/chart/edit/<chart_id>"
        response = self.client.get(
            reverse('reports_chart_edit', args=[self.chart.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_chart_delete_out(self):
        "Testing /reports/chart/delete/<chart_id>"
        response = self.client.get(
            reverse('reports_chart_delete', args=[self.chart.id]))
        self.assertRedirects(response, reverse('user_login'))

    # Reports
    def test_report_add_out(self):
        "Testing /reports/report/add/"
        response = self.client.get(reverse('reports_report_add'))
        self.assertRedirects(response, reverse('user_login'))

    def test_report_view_out(self):
        "Testing /reports/report/view/<report_id>"
        response = self.client.get(
            reverse('reports_report_view', args=[self.report.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_report_edit_out(self):
        "Testing /reports/report/edit/<report_id>"
        response = self.client.get(
            reverse('reports_report_edit', args=[self.report.id]))
        self.assertRedirects(response, reverse('user_login'))

    def test_report_delete_out(self):
        "Testing /reports/report/delete/<report_id>"
        response = self.client.get(
            reverse('reports_report_delete', args=[self.report.id]))
        self.assertRedirects(response, reverse('user_login'))
