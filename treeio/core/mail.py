# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core Mail Framework
"""
from treeio.core.conf import settings

import re
import time
import base64
import smtplib
import imaplib
import email
import poplib
from datetime import datetime

from email.MIMEText import MIMEText
from email.header import decode_header
from email.MIMEMultipart import MIMEMultipart

from threading import Thread
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _
from django.template.defaultfilters import removetags

EMAIL_SERVER = getattr(settings, 'EMAIL_SERVER', '127.0.0.1')
IMAP_SERVER = getattr(settings, 'IMAP_SERVER', '')
EMAIL_USERNAME = getattr(settings, 'EMAIL_USERNAME', None)
EMAIL_PASSWORD = getattr(settings, 'EMAIL_PASSWORD', None)
EMAIL_FROM = getattr(settings, 'EMAIL_FROM', 'noreply@tree.io')
DEFAULT_SIGNATURE = getattr(settings, 'DEFAULT_SIGNATURE', '')


class BaseEmail(Thread):

    "Generic e-mail class to send any emails"

    def __init__(self, server, username, password, fromaddr,
                 toaddr, subject, body, signature=None, html=None,
                 port=None, ssl=False):
        Thread.__init__(self)
        self.server = server
        self.port = port
        self.ssl = ssl
        self.username = username
        self.password = password
        self.toaddr = toaddr
        self.fromaddr = fromaddr
        self.subject = subject
        self.body = body
        self.signature = signature
        self.html = html
        self.multipart = self.body and self.html

    def run(self):
        "Run"
        self.process_email()

    def send_email(self):
        "Send email"
        self.start()

    def get_smtp_port(self, server):
        "Returns appropriate SMTP port number depending on incoming server name and boolean ssl"
        # http://www.emailaddressmanager.com/tips/mail-settings.html

        port = 25  # default
        ssl = False

        if "gmail.com" in server or "googlemail.com" in server:
            port = 587
            ssl = False
        elif server == "plus.smtp.mail.yahoo.com":
            if hasattr(smtplib, 'SMTP_SSL'):
                port = 465
            ssl = True
        if server == "smtp.live.com" or server == "smtp.isp.netscape.com":
            ssl = True

        return port, ssl

    def process_email(self):
        "Create a message and send it"
        try:
            msg = MIMEMultipart('alternative')

            msg['From'] = self.fromaddr
            msg['To'] = self.toaddr
            msg['Subject'] = self.subject

            text = self.body
            html = self.html

            # adding signature
            if self.signature:
                text += self.signature

            # Record the MIME types of both parts - text/plain and text/html.
            part1 = MIMEText(text.encode('utf-8'), 'plain', 'utf-8')
            msg.attach(part1)

            if html:
                part2 = MIMEText(html.encode('utf-8'), 'html', 'utf-8')
                msg.attach(part2)

            if not self.port:
                self.port, self.ssl = self.get_smtp_port(self.server)

            if self.ssl and hasattr(smtplib, 'SMTP_SSL'):
                s = smtplib.SMTP_SSL(self.server, self.port)
            else:
                s = smtplib.SMTP(self.server, self.port)
            s.set_debuglevel(0)
            s.ehlo()
            try:
                s.starttls()
            except smtplib.SMTPException:
                pass
            s.ehlo()
            if self.username is not None:
                s.login(self.username, self.password)
            s.sendmail(self.fromaddr, self.toaddr, msg.as_string())
            s.close()
            return True
        except:
            if settings.DEBUG:
                raise
            else:
                import traceback
                import sys
                from treeio import core
                from django.core.mail import mail_admins
                exc_type, exc_value, exc_traceback = sys.exc_info()
                domain = getattr(settings, 'CURRENT_DOMAIN', 'default')
                subject = "Exception for %s: %s %s" % (
                    domain, unicode(exc_type), unicode(exc_value))
                body = subject + "\n\n"
                body += unicode(core.__file__) + "\n\n"
                body += u"Server: %s\n\n" % self.server
                body += u"Port: %s\n\n" % unicode(self.port)
                body += u"Username: %s\n\n" % self.username
                body += u"From: %s\n\n" % self.fromaddr
                body += u"To: %s\n\n" % self.toaddr
                for s in traceback.format_tb(exc_traceback):
                    body += s + '\n'
                mail_admins(subject, body)


class SystemEmail(BaseEmail):

    "E-mail class to send messages on behalf of Tree.io team"

    def __init__(self, toaddr, subject, body, signature=None, html=None):

        if not signature:
            signature = _(DEFAULT_SIGNATURE)

        BaseEmail.__init__(self, EMAIL_SERVER, EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_FROM,
                           toaddr, subject, body, signature, html)

#
# Specific email classes
#


class EmailInvitation(SystemEmail):

    "Email Invitation"

    invitation = None
    sender = None

    def __init__(self, invitation, sender, domain):
        self.invitation = invitation
        self.sender = sender
        self.domain = domain

        subject = '%s has invited you to Tree.io' % (self.sender)

        toaddr = self.invitation.email

        signature = """
\r\n
- %s""" % unicode(self.sender)

        body = """
Hi!
\r\n
I've invited you to Tree.io.
\r\n
Tree.io is a new online service that helps you manage your business online.
\r\n
Use this link to join me:
\r\n
http://%s/accounts/invitation/?email=%s&key=%s
        """ % (unicode(self.domain),
               unicode(self.invitation.email),
               unicode(self.invitation.key))

        super(EmailInvitation, self).__init__(toaddr, subject, body, signature)


class EmailPassword(SystemEmail):

    "Email Message"

    def __init__(self, toaddr, username, password):

        subject = "Password reset on Tree.io"

        body = """
Hello!
\r\n
You have requested a password reset for your Tree.io account.
\r\n
New password for: %s\r\n\r\n Password: %s\r\n\r\n
""" % (username, password)

        super(EmailPassword, self).__init__(toaddr, subject, body)


#
# Abstract email receiver
#

def intcmp(a, b):
    try:
        return cmp(int(a), int(b))
    except:
        return cmp(a, b)


class EmailReceiver(Thread):

    """EmailReceiver fetches email from imap and pop email servers.
       This class can be used only as parent. You should redefine
       the process_msg method.
    """

    def __init__(self, server_type, server_name, username, password, folder_name=None):
        Thread.__init__(self)
        self.incoming_server_type = server_type
        self.incoming_server_name = server_name
        self.incoming_server_username = username
        self.incoming_password = password
        self.folder_name = folder_name or getattr(
            settings, 'HARDTREE_MESSAGING_IMAP_DEFAULT_FOLDER_NAME', 'UNSEEN')

        default_timezone = settings.HARDTREE_SERVER_DEFAULT_TIMEZONE
        all_timezones = getattr(settings, 'HARDTREE_SERVER_TIMEZONE', [
                                (1, '(GMT-11:00) International Date Line West')])
        title = all_timezones[int(default_timezone)][1]
        GMT = title[4:10]  # with sign e.g. +06:00
        sign = GMT[0:1]  # + or -
        hours = int(GMT[1:3])  # e.g. 06
        mins = int(GMT[4:6])
        self.tzoffset = hours * 3600 + mins * 60
        if sign == "-":
            self.tzoffset = self.tzoffset * -1

    def run(self):
        "Run"
        self.get_emails()

    def get_pop_port(self):
        "Returns appropriate POP port number depending on incoming server name"

        port = 110  # default
        ssl = False

        if self.incoming_server_type == 'POP3-SSL':
            port = 995
            ssl = True

        return port, ssl

    def get_imap_port(self):
        "Returns appropriate IMAP port number depending on incoming server name"

        port = 143  # default
        ssl = False

        if self.incoming_server_type == 'IMAP-SSL':
            port = 993
            ssl = True

        return port, ssl

    def get_emails(self):
        "Fetches emails"

        if self.incoming_server_type == 'IMAP' or self.incoming_server_type == 'IMAP-SSL':

            HARDTREE_MESSAGING_IMAP_LIMIT = getattr(
                settings, 'HARDTREE_MESSAGING_IMAP_LIMIT', 100)
            # connect to the server
            port, ssl = self.get_imap_port()

            if ssl:
                M = imaplib.IMAP4_SSL(self.incoming_server_name, port)
            else:
                M = imaplib.IMAP4(self.incoming_server_name, port)
            M.login(self.incoming_server_username, self.incoming_password)
            M.select()

            msgnums = []
            try:
                # fetch mail from ALL or UNSEEN]
                typ, data = M.sort('REVERSE DATE', 'UTF-8', self.folder_name)
                msgnums = data[0].split() if data[0] else []
            except:
                # fetch mail from ALL or UNSEEN]
                typ, data = M.search(None, self.folder_name)
                msgnums = data[0].split() if data[0] else []
                msgnums = sorted(msgnums, cmp=intcmp, reverse=True)

            for num in msgnums[:HARDTREE_MESSAGING_IMAP_LIMIT]:
                resp, msg = M.fetch(num, '(RFC822)')
                mail = email.message_from_string(msg[0][1])
                self.process_mail(mail)
                if self.folder_name == 'UNSEEN':
                    M.store(num, '+FLAGS', '\\Seen')

            M.close()
            M.logout()

        if self.incoming_server_type == 'POP3' or self.incoming_server_type == 'POP3-SSL':

            HARDTREE_MESSAGING_POP3_LIMIT = getattr(
                settings, 'HARDTREE_MESSAGING_POP3_LIMIT', 100)
            # connect to the server
            port, ssl = self.get_pop_port()

            if ssl:
                M = poplib.POP3_SSL(self.incoming_server_name, port)
            else:
                M = poplib.POP3(self.incoming_server_name, port)
            M.user(self.incoming_server_username)
            M.pass_(self.incoming_password)

            numMessages = len(M.list()[1])

            # Select correct limit for range(limit, numMessages)
            if numMessages >= HARDTREE_MESSAGING_POP3_LIMIT:
                limit = numMessages - HARDTREE_MESSAGING_POP3_LIMIT
            else:
                limit = 0

            # select new emails
            for i in range(limit, numMessages):
                lines = M.retr(i)[1]
                mail = email.message_from_string("\n".join(lines))
                self.process_mail(mail)
            M.quit()

    def process_mail(self, mail):
        # process message
        body = None
        attachments = []

        if mail.is_multipart():
            text = None
            html = None
            for part in mail.walk():
                # multipart are just containers, so we skip them
                if part.get_content_maintype() == 'multipart':
                    continue

                if part.get_filename() and part.get('Content-Transfer-Encoding', '') == 'base64':
                    attachments.append(part)
                    continue

                if part.get_content_type() == 'text/plain':
                    text = part.get_payload(decode=True)

                if part.get_content_type() == 'text/html':
                    html = part.get_payload(decode=True)

            body = html if html else text
        else:
            body = mail.get_payload(decode=True)

        class MailAttrs:
            pass
        attrs = MailAttrs()
        attrs.subject, encoding = self.decode_subject(mail['subject'])
        # replace annoying characters
        attrs.body = self.decode(body, encoding)
        if not mail.is_multipart() and not mail.get_content_type().endswith('html'):
            attrs.body = attrs.body.replace('&', '&amp;').replace('<', '&lt;').replace(
                '>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')
        attrs.body = self.parse_email_body(attrs.body)
        attrs.author_name, attrs.author_email = self.get_email_author(mail)

        attrs.email_date = None
        try:
            date_tuple = email.utils.parsedate_tz(mail['Date'])
            email_ts = time.mktime(
                date_tuple[:9]) - int(date_tuple[9]) + self.tzoffset
            attrs.email_date = datetime.fromtimestamp(email_ts)
        except:
            pass

        self.process_msg(mail, attrs, attachments)

    def process_msg(self, msg, attrs, attachments):
        raise NotImplementedError

    def decode(self, string, encoding):
        if encoding:
            return smart_unicode(string, encoding, errors='ignore')
        else:
            return self.make_unicode(string)

    def make_unicode(self, string):
        "Detects string encoding and make it unicode"

        utf8_detector = re.compile(r"""^(?:
            [\x09\x0A\x0D\x20-\x7E]            # ASCII
          | [\xC2-\xDF][\x80-\xBF]             # non-overlong 2-byte
          |  \xE0[\xA0-\xBF][\x80-\xBF]        # excluding overlongs
          | [\xE1-\xEC\xEE\xEF][\x80-\xBF]{2}  # straight 3-byte
          |  \xED[\x80-\x9F][\x80-\xBF]        # excluding surrogates
          |  \xF0[\x90-\xBF][\x80-\xBF]{2}     # planes 1-3
          | [\xF1-\xF3][\x80-\xBF]{3}          # planes 4-15
          |  \xF4[\x80-\x8F][\x80-\xBF]{2}     # plane 16
         )*$""", re.X)

        cp1252_detector = re.compile(r'^(?:[\x80-\xBF])*$', re.X)
        xa4_detector = re.compile(r'^(?:\xA4)*$', re.X)

        try:
            if re.match(utf8_detector, string):
                return unicode(string, 'utf_8')
            if re.match(cp1252_detector, string):
                if re.match(xa4_detector, string):
                    return smart_unicode(string, 'iso8859_15')
                else:
                    return smart_unicode(string, 'cp1252')
            return smart_unicode(string, 'koi8-r', errors='ignore')
        except:
            return smart_unicode(string, 'utf-8', errors='ignore')

    def decode_subject(self, subject):
        "Decodes email subjects"
        if not subject:
            subject = 'No subject'
            encoding = None
        else:
            subject, encoding = decode_header(subject)[0]
            subject = self.decode(subject, encoding)
        return subject, encoding

    def decode_body(self, body):
        "Decodes Base64-encoded string"
        if body is None:
            body = 'No message'
        else:
            body = str(body)
            body = base64.b64decode(body)

        return body

    def parse_email_body(self, body):
        "Removes all the dangerous and useless staff"

        # Replace annoying characters
        body = body.replace('\r', '').replace('=\n', '').replace('=\n\r', '')
        body = body.replace('=20\n', '\n\n')

        HARDTREE_MESSAGING_UNSAFE_BLOCKS = getattr(settings, 'HARDTREE_MESSAGING_UNSAFE_BLOCKS',
                                                   ('head', 'object', 'embed', 'applet', 'noframes',
                                                    'noscript', 'noembed', 'iframe', 'frame', 'frameset'))

        # Strip unsafe tags
        tags_str = ' '.join(HARDTREE_MESSAGING_UNSAFE_BLOCKS)
        body = removetags(body, tags_str)

        # Remove multiple <br /> tags
        rules = [
            {r'\s*<br\s*/?>\s*': u'\n'}
        ]

        for rule in rules:
            for (k, v) in rule.items():
                regex = re.compile(k)
                body = regex.sub(v, body)

        # displaying messages correctly
        if body.startswith('<!DOCTYPE') or body.startswith('<html') or body.startswith('<meta'):
            body = body.replace('\n\n\n', '\n').replace(
                '\n\n', '\n').replace('>\n<', '><')
        elif not '<html' in body:
            body = body.replace('\n', '<br />\n')

        return body

    def get_email_author(self, msg):
        "Returns author's name and email if any"
        try:
            header_from = msg['From']
            splits = header_from.split('<', 1)
            name, email = splits if len(splits) == 2 else ('', header_from)
            email = email.split('>', 1)[0]
            if name:
                name, encoding = decode_header(name.strip(' "\''))[0]
                name = self.decode(name, encoding)
                name = name.strip(' \'"')
        except:
            email = name = None

        if not email:
            try:
                email = msg['Return-path']
                email.strip(' \'"<>')
            except Exception:
                email = None

        return name, email
