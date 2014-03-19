# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

#!/usr/bin/python

OBJECTS_NUM = 100

# setup environment
import sys
import os
sys.path.append('../')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.management import setup_environ
from treeio import settings
from treeio.core.models import Object, User
from treeio.projects.models import Project

setup_environ(settings)

user = User.objects.all()[0]

for i in range(0, OBJECTS_NUM):
    project = Project(name='test' + unicode(i))
    project.set_user(user)
    project.save()
    objects = Object.filter_permitted(user, Project.objects)
    allowed = 0
    for obj in objects:
        if user.has_permission(obj):
            allowed += 1
    print len(list(objects)), ':', allowed
