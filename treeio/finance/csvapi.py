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


class ProcessTransactions():

    "Import/Export Contacts"

    def export_transactions(self, transactions):
        "Export transactions into CSV file"

        response = HttpResponse(mimetype='text/csv')
        response[
            'Content-Disposition'] = 'attachment; filename=Transactions_%s.csv' % datetime.date.today().isoformat()

        writer = csv.writer(response)
        headers = ['name', 'source', 'target', 'liability',
                   'category', 'account', 'datetime', 'value', 'details']
        writer.writerow(headers)
        for transaction in transactions:
            row = []
            row.append(transaction)
            row.append(transaction.source)
            row.append(transaction.target)
            row.append(transaction.liability)
            row.append(transaction.category)
            row.append(transaction.account)
            row.append(transaction.datetime)
            row.append(transaction.get_relative_value())
            row.append(transaction.details)
            writer.writerow(row)
        return response

    def import_transactions(self, content):
        "Import transactions from CSV file"

        f = StringIO.StringIO(content)
        transactions = csv.DictReader(f, delimiter=',')

        self.parse_transactions(transactions)

    def parse_transactions(self, transactions):
        "Break down CSV file into transactions"
