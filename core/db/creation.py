# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#-*- encoding: utf-8 -*-
"""
Database creator
"""
__author__ = 'Kirill Yakovenko, crystalnix'
__email__ = 'kirill.yakovenko@gmail.com'

from django.conf import settings
from django.db import connections
from django.utils.importlib import import_module


def DatabaseCreation(domain):
    connection = connections[domain]
    try:
        BaseDatabaseCreation = import_module(
            '.creation', connection.settings_dict['ENGINE']).DatabaseCreation
    except:
        BaseDatabaseCreation = import_module(
            '.creation', 'django.db.backends').BaseDatabaseCreation

    class DBCreation(BaseDatabaseCreation):

        def __init__(self, connection):
            super(DBCreation, self).__init__(connection)
            self.database_name = self.connection.settings_dict.get(
                'NAME') or super(DBCreation, self)._get_test_db_name()

        def _get_test_db_name(self):
            return self.database_name

        def create_db(self, load_initial):
            from django.core.management import call_command

            # Deletes database name because if database doesn't exist,
            # django orm isn't able to connect to it.
            self.connection.settings_dict["NAME"] = None
            self._create_test_db(0, True)
            self.connection.settings_dict["NAME"] = self.database_name

            self.connection.close()
            # Confirm the feature set of the database
            self.connection.features.confirm()

            # Report syncdb messages at one level lower than that requested.
            # This ensures we don't get flooded with messages during testing
            # (unless you really ask to be flooded)
            call_command('syncdb',
                         verbosity=0,
                         interactive=False,
                         database=domain,
                         load_initial_data=load_initial,
                         migrate_all=True)

            from django.core.cache import get_cache
            from django.core.cache.backends.db import BaseDatabaseCache
            for cache_alias in settings.CACHES:
                cache = get_cache(cache_alias)
                if isinstance(cache, BaseDatabaseCache):
                    from django.db import router
                    if router.allow_syncdb(self.connection.alias, cache.cache_model_class):
                        call_command(
                            'createcachetable', cache._table, database=self.connection.alias)

            # Get a cursor (even though we don't need one yet). This has
            # the side effect of initializing the test database.
            cursor = self.connection.cursor()  # NOQA
            return self.database_name

    return DBCreation(connection)
