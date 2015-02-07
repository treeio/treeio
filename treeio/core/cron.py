# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core Cron jobs
"""

import re
import random

from os.path import join
from treeio.core.conf import settings
from treeio.core.views import save_upload
from treeio.core.mail import EmailReceiver
from treeio.identities.models import Contact
from treeio.core.models import Object, UpdateRecord, Attachment


class EmailReplier(EmailReceiver):
    subject_regex = re.compile(
        "(Re:\s*)*\[Tree.io \#(?P<id>\d+)\] .+: .+ '.+' - .+", re.IGNORECASE | re.MULTILINE)

    def process_msg(self, msg, attrs, attachments):
        # get user profile by author email
        contact = Contact.objects.filter(contactvalue__value=attrs.author_email, contactvalue__field__field_type='email',
                                         related_user__isnull=False)[:1]
        contact = contact[0] if contact else None
        author = contact.related_user if contact else None

        # check subject and get Object, subject should be fit subject's regex
        # in Object.notify_subscribers
        regex = self.subject_regex.match(attrs.subject)
        if regex and author:
            try:
                obj = Object.objects.get(id=regex.group('id'))
                # create UpdateRecord sceleton
                note, created = UpdateRecord.objects.get_or_create(author=author.user, sender=contact,
                                                                   record_type='manual', date_created=attrs.email_date)
                if created:
                    # find and wrap a quotation into div container
                    def find_quotation(string):
                        n = 0
                        i = iter(string)
                        try:
                            while i.next() == u'>':
                                n += 1
                        except StopIteration:
                            pass
                        return n
                    body = []
                    nesting = 0
                    lines = re.split(
                        u'<br\s*/?>\n?', attrs.body, re.IGNORECASE | re.MULTILINE | re.VERBOSE)
                    for line in lines:
                        line_start = find_quotation(line)
                        if line_start > nesting:
                            for i in range(line_start - nesting):
                                body.append(u'<div class="reply-quote">\n')
                        elif line_start < nesting:
                            for i in range(nesting - line_start):
                                body.append(u'</div>\n')
                        else:
                            body.append(u'<br />\n')
                        body.append(line[line_start:])
                        nesting = line_start
                    note.url = obj.get_absolute_url()
                    note.body = u''.join(body)
                    note.save()
                    # associate new UpdateRecord with object
                    for subscriber in obj.subscribers.all():
                        note.recipients.add(subscriber)
                    note.recipients.add(author)
                    note.about.add(obj)
                    # append attachments
                    for file in attachments:
                        random.seed()
                        filehash = str(random.getrandbits(128))
                        savefile = join(
                            getattr(settings, 'MEDIA_ROOT'), 'attachments', filehash)
                        # save a file
                        file_body = file.get_payload(decode=True)
                        success = save_upload(file_body, savefile, True)
                        if success:
                            Attachment(uploaded_by=author.user, filename=file.get_filename(), attached_file=filehash,
                                       attached_record=note, attached_object=obj).save()

            except (Object.DoesNotExist, UpdateRecord.DoesNotExist):
                pass


def email_reply():
    "Fetches emails"
    from treeio.core.mail import IMAP_SERVER, EMAIL_USERNAME, EMAIL_PASSWORD
    emailreplier = EmailReplier('IMAP-SSL', IMAP_SERVER, EMAIL_USERNAME, EMAIL_PASSWORD,
                                getattr(settings, 'HARDTREE_MESSAGING_IMAP_DEFAULT_FOLDER_NAME', 'UNSEEN'))
    emailreplier.get_emails()
