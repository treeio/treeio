# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Import/Export Contacts API
"""

import csv
from django.http import HttpResponse
import StringIO
import datetime


class ProcessTransactions(object):

    "Import/Export Contacts"

    def export_transactions(self, transactions):
        "Export transactions into CSV file"

        response = HttpResponse(content_type='text/csv')
        response[
            'Content-Disposition'] = 'attachment; filename=Transactions_%s.csv' % datetime.date.today().isoformat()

        writer = csv.writer(response)
        headers = ['name', 'source', 'target', 'liability',
                   'category', 'account', 'datetime', 'value', 'details']
        writer.writerow(headers)
        for transaction in transactions:
            row = [transaction, transaction.source, transaction.target, transaction.liability, transaction.category,
                   transaction.account, transaction.datetime, transaction.get_relative_value(), transaction.details]
            writer.writerow(row)
        return response

    def import_transactions(self, content):
        "Import transactions from CSV file"

        f = StringIO.StringIO(content)
        transactions = csv.DictReader(f, delimiter=',')

        self.parse_transactions(transactions)

    def parse_transactions(self, transactions):
        "Break down CSV file into transactions"
