# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Project Management

The PM module allows to manage projects, their milestones and tasks.
Tasks may be assigned to one or more users registered within Hardtree.

Each Task and Milestone is assigned a Status, one of TaskStatus instances,
which may be dynamically defined. Those Tasks and Milestones which are assigned
a Status with .hidden field set to True won't be displayed, unless the Status
is selected in Filters or an appropriate view.

"""
