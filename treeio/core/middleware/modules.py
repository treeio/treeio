# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Modules middleware: handles modular behavior of the system
"""

from treeio.core.conf import settings
from treeio.core.models import Module

# This must be fired after Django processes request
# i.e. after Django's own middleware has been fired


class ModuleDetect():

    "Handles Hardtree automatic modules detection"

    def process_request(self, request):
        "Process request"
        hmodules = dict()
        for module in settings.INSTALLED_APPS:
            import_name = str(
                module) + "." + settings.HARDTREE_MODULE_IDENTIFIER
            try:
                hmodule = __import__(import_name, fromlist=[str(module)])
                hmodules[str(module)] = hmodule.PROPERTIES
            except ImportError:
                pass
            except AttributeError:
                pass

        dbmodules = Module.objects.all()

        for dbmodule in dbmodules:
            if dbmodule.name not in hmodules:
                dbmodule.delete()
            else:
                differ = False
                hmodule = dbmodule.name
                if dbmodule.title != hmodules[hmodule]['title']:
                    dbmodule.title = hmodules[hmodule]['title']
                    differ = True
                if dbmodule.url != hmodules[hmodule]['url']:
                    dbmodule.url = hmodules[hmodule]['url']
                    differ = True
                if dbmodule.details != hmodules[hmodule]['details']:
                    dbmodule.details = hmodules[hmodule]['details']
                    differ = True
                if dbmodule.system != hmodules[hmodule]['system']:
                    dbmodule.system = hmodules[hmodule]['system']
                    differ = True
                if differ:
                    dbmodule.save()

        for hmodule in hmodules:
            dbmodule = None
            try:
                dbmodule = Module.objects.get(name=hmodule)
            except Module.DoesNotExist:
                pass
            except Module.MultipleObjectsReturned:
                # Broken database, delete all matching modules
                Module.objects.filter(name=hmodule).delete()
            if not dbmodule:
                dbmodule = Module(name=hmodule, title=hmodules[hmodule]['title'],
                                  url=hmodules[hmodule]['url'],
                                  details=hmodules[hmodule]['details'], system=hmodules[hmodule]['system'])
                dbmodule.save()
                dbmodule.set_default_user()

    def process_response(self, request, response):
        "Process response"

        if settings.QUERY_DEBUG:
            from django.db import connection
            totaltime = float(0)
            for q in connection.queries:
                totaltime += float(q['time'])
            if len(connection.queries) > 3:
                if settings.QUERY_DEBUG_FULL:
                    print "=== DB Queries:"
                    for q in connection.queries:
                        print q
                print "=== DB Query report:"
                print "---  Total time: " + str(totaltime)
                print "---  Total queries: " + str(len(connection.queries))
        return response
