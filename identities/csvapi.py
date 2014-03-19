# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Import/Export Contacts API
"""

import csv
import StringIO
from treeio.identities.models import Contact, ContactType, ContactValue
import re
import urlparse


class ProcessContacts():

    "Import/Export Contacts"

    """
    def export_contacts(self, contacts):
        "Export contacts into CSV file"

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Contacts.csv'

        writer = csv.writer(response)
        headers = ['name', 'type']

        fields = ContactField.objects.filter(trash=False)
        for field in fields:
            headers.append(field.name)
        writer.writerow(headers)
        for contact in contacts:
            row = []
            row.append(contact)
            row.append(contact.contact_type)
            vals = contact.contactvalue_set.all()
            for field in fields:
                inserted = False
                for val in vals:
                    if val.field == field:
                        row.append(val.value)
                        inserted = True
                if not inserted:
                    row.append('')
            writer.writerow(row)
        return response
    """

    def import_contacts(self, content):
        "Import contacts from CSV file"

        f = StringIO.StringIO(content)
        contacts = csv.DictReader(f, delimiter=',')

        self.parse_contacts(contacts)

    def verify_email(self, email):
        "Verify email format"
        try:
            email_matched = re.findall(
                '[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+', email)
            if email_matched:
                return email  # Contact Email Address
        except Exception:
            return None

    def verify_url(self, url):
        "Verify url"
        if url:
            if '://' not in url:
                # If no URL scheme given, assume http://
                url = u'http://%s' % url
            url_fields = list(urlparse.urlsplit(url))
            if not url_fields[2]:
                # the path portion may need to be added before query params
                url_fields[2] = '/'
                url = urlparse.urlunsplit(url_fields)
        return url

    def parse_contacts(self, contacts):
        "Break down CSV file into fields"

        for row in contacts:

            # Tidy up keys (iterkeys strip())

            try:
                type = row['type']
            except Exception:
                pass  # Set type to default type

            try:
                name = row['name']
            except Exception:
                try:
                    firstname = row['firstname']
                    surname = row['surname']
                    name = firstname + " " + surname
                except Exception:
                    continue

            contact_type = ContactType.objects.filter(name=type)
            if contact_type:
                contact_type = contact_type[0]

            # Create a new contact if it doesn't exist
            contact_exists = Contact.objects.filter(
                name=name, contact_type__name=type, trash=False)

            # TODO: If one does exist then append the data on that contact

            if not contact_exists:

                contact = Contact()
                contact.name = name
                contact.contact_type = contact_type
                contact.auto_notify = False
                contact.save()

                fields = contact_type.fields.filter(trash=False)

                for field in fields:
                    if field.name in row:
                        x = row[field.name]
                        if field.field_type == 'email':
                            x = self.verify_email(x)
                        if field.field_type == 'url':
                            x = self.verify_url(x)
                        if x:
                            contact_value = ContactValue()
                            contact_value.field = field
                            contact_value.contact = contact
                            contact_value.value = x
                            contact_value.save()
