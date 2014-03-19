# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Database manipulations

Dynamically identifies the correct database to use for the current domain
"""
from pandora import box
from django.utils import simplejson as json
import UserDict

from os import path

FILE_ROOT = path.abspath(path.dirname(__file__))

HARDTREE_DB_SETTINGS_FILE = path.join(FILE_ROOT, 'dbsettings.json')
NO_DEFAULT = False


class DatabaseNotFound(Exception):
    pass


class DatabaseDict(UserDict.DictMixin, dict):

    """A dictionary which applies an arbitrary key-altering function before accessing the keys"""

    def _ensure_defaults(self):
        for db in self.values():
            db.setdefault('ENGINE', 'django.db.backends.dummy')
            if db['ENGINE'] == 'django.db.backends.' or not db['ENGINE']:
                db['ENGINE'] = 'django.db.backends.dummy'
            db.setdefault('OPTIONS', {})
            db.setdefault('TEST_CHARSET', None)
            db.setdefault('TEST_COLLATION', None)
            db.setdefault('TEST_NAME', None)
            db.setdefault('TEST_MIRROR', None)
            db.setdefault('TIME_ZONE', 'UTC0')
            for setting in ('NAME', 'USER', 'PASSWORD', 'HOST', 'PORT'):
                db.setdefault(setting, '')

    def __init__(self, *args, **kwargs):
        self._load_databases(*args, **kwargs)

    def _load_databases(self, *args, **kwargs):
        dbfile = open(HARDTREE_DB_SETTINGS_FILE, 'r')
        self.store = json.load(dbfile)
        self.update(dict(*args, **kwargs))  # use the free update to set keys
        self._ensure_defaults()

    def _save_databases(self):
        f = open(HARDTREE_DB_SETTINGS_FILE, 'w')
        json.dump(self.store, f)
        f.close()

    def __getitem__(self, key):
        try:
            return self.store[key]
        except KeyError:
            self._load_databases()
            try:
                return self.store[key]
            except KeyError:
                try:
                    if NO_DEFAULT:
                        raise DatabaseNotFound(
                            'No database found for %s' % key)
                    return self.store['default']
                except KeyError:
                    raise RuntimeError(
                        'Default database is not specified in the config file and the current database is unavailable')

    def __setitem__(self, key, value):
        self.store[key] = value
        self._save_databases()

    def __delitem__(self, key):
        del self.store[key]
        self._save_databases()

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)


class DBRouter(object):

    """A router to control all database operations and dynamically select the correct database"""

    def _get_current_database(self):
        "Returns the database that should be used for the current request"
        if 'request' in box and not 'CURRENT_DATABASE_NAME' in box:
            current_db = box['request'].get_host().split('.')[0]
        else:
            current_db = box.get('CURRENT_DATABASE_NAME', 'default')
        return current_db

    def db_for_read(self, model, **hints):
        "Point all operations to the current database"
        if hints.has_key('instance'):
            return hints['instance']._state.db
        return self._get_current_database()

    def db_for_write(self, model, **hints):
        "Point all operations to the current database"
        return self._get_current_database()

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation"
        return True

    def allow_syncdb(self, db, model):
        "Allow syncdb"
        return True
