# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core module URLs
"""

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('treeio.core.views',
                       url(r'^logout(\.(?P<response_format>\w+))?/?$',
                           'user_logout', name='user_logout'),
                       url(r'^login(\.(?P<response_format>\w+))?/?$',
                           'user_login', name='user_login'),
                       url(r'^denied(\.(?P<response_format>\w+))?/?$',
                           'user_denied', name='user_denied'),
                       url(r'setup(\.(?P<response_format>\w+))?/?$',
                           'database_setup', name='database_setup'),

                       # Switch perspective
                       url(r'^perspective(\.(?P<response_format>\w+))?/?$',
                           'user_perspective', name='user_perspective'),

                       # Popup handler
                       url(r'^popup(\.json)?/(?P<popup_id>[a-z0-9\-_]+)/url=(?P<url>.+)/?$',
                           'ajax_popup', name='core_ajax_popup'),

                       # AJAX handlers
                       url(r'^ajax/objects(\.(?P<response_format>\w+))?/?$',
                           'ajax_object_lookup', name='core_ajax_object_lookup'),
                       url(r'^ajax/tags(\.(?P<response_format>\w+))?/?$',
                           'ajax_tag_lookup', name='core_ajax_tag_lookup'),

                       # Attachments
                       url(r'^ajax/upload/(?P<object_id>\d+)?/?$',
                           'ajax_upload', name="ajax_upload"),
                       url(r'^ajax/upload/record/(?P<record_id>\d+)?/?$',
                           'ajax_upload_record', name="ajax_upload_record"),
                       url(r'^attachment/download/(?P<attachment_id>\d+)/?$',
                           'attachment_download', name='core_attachment_download'),

                       # Reset password
                       url(r'^password_reset/$', 'password_reset',
                           name='password_reset'),
                       url(r'^password_reset/done/$', 'password_reset_done',
                           name='password_reset_done'),
                       url(r'^invitation/$', 'invitation_retrieve',
                           name='invitation_retrieve'),

                       # Custom logo
                       url(r'^logo/image/$', 'logo_image',
                           name='core_logo_image', kwargs={'gif': False}),
                       url(r'^logo/image/ie/$', 'logo_image',
                           name='core_logo_image_ie', kwargs={'gif': True}),


                       )
