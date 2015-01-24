# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

from distutils.util import strtobool
from django.core.management.base import BaseCommand, CommandError
from treeio.core.conf import settings
import json
import subprocess
from os import path, makedirs
import sys

PROJECT_ROOT = getattr(settings, 'PROJECT_ROOT')
HARDTREE_DB_SETTINGS_FILE = path.join(PROJECT_ROOT, 'core/db/dbsettings.json')
if not path.exists(path.dirname(HARDTREE_DB_SETTINGS_FILE)):
    makedirs(path.dirname(HARDTREE_DB_SETTINGS_FILE))


class Command(BaseCommand):
    args = ''
    help = 'Installs the database prompting the user for all details'

    def handle(self, *args, **options):

        initial_db = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': './initial.db',
            'HOST': '',
            'USER': '',
            'PASSWORD': ''
        }

        db = {}

        dbengine = raw_input(
            'Enter database engine <mysql,postgresql,postgresql_psycopg2,oracle,sqlite3> (defaults to postgres): ')
        if not dbengine:
            dbengine = 'postgresql_psycopg2'
        if dbengine in ('mysql', 'postgresql', 'postgresql_psycopg2', 'oracle', 'sqlite3'):
            dbengine = 'django.db.backends.' + dbengine
        else:
            raise CommandError('Unknown database engine: %s' % dbengine)

        if dbengine.endswith('sqlite3'):
            dbname = raw_input(
                'Enter database name (defaults to treeio.db): ')
            if not dbname:
                dbname = 'treeio.db'
        else:
            dbname = raw_input(
                'Enter database name (defaults to treeio): ')
            if not dbname:
                dbname = 'treeio'

            dbuser = raw_input('Database user (defaults to treeio): ')
            if not dbuser:
                dbuser = 'treeio'

            dbpassword = raw_input('Database password: ')

            dbhost = raw_input('Hostname (defaults to 127.0.0.1): ')
            if not dbhost:
                dbhost = '127.0.0.1'
            dbport = raw_input('Port (empty for default): ')

        self.stdout.write('\n-- Saving database configuration...\n')
        self.stdout.flush()
        settings.CONF.set('db', 'ENGINE', dbengine)
        settings.CONF.set('db', 'NAME', dbname)
        if not dbengine.endswith('sqlite3'):
            settings.CONF.set('db', 'USER', dbuser)
            settings.CONF.set('db', 'PASSWORD', dbpassword)
            settings.CONF.set('db', 'HOST', dbhost)
            settings.CONF.set('db', 'PORT', dbport)

        with open(settings.USER_CONFIG_FILE, 'w') as f:
            settings.CONF.write(f)

        answer = raw_input(
            'Would you like to create the tables (say no to use an existing database) [y/n] (defaults to yes): ')
        if not len(answer):
            answer = True
        else:
            answer = strtobool(answer)

        if answer:
            exit_code = subprocess.call(
                [sys.executable, 'manage.py', 'syncdb', '--all', '--noinput'])
            if not exit_code == 0:
                self.stdout.flush()
                f = open(HARDTREE_DB_SETTINGS_FILE, 'w')
                json.dump({'default': initial_db}, f)
                f.close()
                raise CommandError('Failed to install database.')

            exit_code = subprocess.call(
                [sys.executable, 'manage.py', 'migrate', '--all', '--fake', '--noinput', '--no-initial-data'])

            self.stdout.write(
                '\n-- Successfully installed database. \n-- You\'re ready to go!\n\n')
