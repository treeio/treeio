# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#!/usr/bin/env python
import sys
import shutil
try:
    import virtualenv
except ImportError:
    print 'Error: virtualenv module not found. Please install virtualenv (e.g. pip install virtualenv)'
import subprocess
from os import path

PROJECT_ROOT = path.abspath(path.dirname(__file__))
REQUIREMENTS = path.join(PROJECT_ROOT, 'requirements.pip')

VE_ROOT = path.join(PROJECT_ROOT, '.ve')
VE_TIMESTAMP = path.join(VE_ROOT, 'timestamp')
VE_ACTIVATE = path.join(VE_ROOT, 'bin', 'activate_this.py')

envtime = path.exists(VE_ROOT) and path.getmtime(VE_ROOT) or 0
envreqs = path.exists(VE_TIMESTAMP) and path.getmtime(VE_TIMESTAMP) or 0
envspec = path.getmtime(REQUIREMENTS)

def go_to_ve():
    # going into ve
    if not VE_ROOT in sys.prefix:
        if sys.platform == 'win32':
            python = path.join(VE_ROOT, 'Scripts', 'python.exe')
        else:
            python = path.join(VE_ROOT, 'bin', 'python')
        try:
            retcode = subprocess.call([python, __file__] + sys.argv[1:])
        except KeyboardInterrupt:
            retcode = 1
        sys.exit(retcode)

update_ve = 'update_ve' in sys.argv
if update_ve or envtime < envspec or envreqs < envspec:
    if update_ve:
        # install ve
        if envtime < envspec:
            if path.exists(VE_ROOT):
                shutil.rmtree(VE_ROOT)
            virtualenv.logger = virtualenv.Logger(consumers=[])
            virtualenv.create_environment(VE_ROOT, site_packages=True)

        go_to_ve()

        # check requirements
        if update_ve or envreqs < envspec:
            import pip
            pip.main(initial_args=['install', '-r', REQUIREMENTS, '--upgrade'])
            file(VE_TIMESTAMP, 'w').close()
        sys.exit(0)
    else:
        print "VirtualEnv need to be updated"
        print "Run ./manage.py update_ve"
        sys.exit(1)

go_to_ve()

from django.core.management import execute_manager
import imp
try:
    imp.find_module('settings') # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)

import settings

if __name__ == "__main__":
    execute_manager(settings)
