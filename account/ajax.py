# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core Ajax views
"""

from django.template import RequestContext
import re
from core.mail import EmailInvitation
from django.contrib.sites.models import RequestSite
from core.models import Attachment, Invitation
from core.views import user_denied
from treeio.core.rendering import render_to_string
from treeio.core.models import Comment, Object, UpdateRecord, Tag
from treeio.core.forms import TagsForm
from treeio.core.ajax import converter
from dajaxice.core import dajaxice_functions
from dajax.core import Dajax


def comments_likes(request, target, form, expand=True):
    dajax = Dajax()

    response_format = 'html'

    object_id = form.get('object_id', 0)
    update = form.get('update', 0)
    object = None
    if update:
        object = UpdateRecord.objects.get(pk=object_id)
    else:
        object = Object.objects.get(pk=object_id)

    profile = request.user.get_profile()

    if object:
        if form.get('like', 0) == unicode(object.id):
            object.likes.add(profile)
            if hasattr(object, 'score'):
                object.score += 1
                object.save()

        elif form.get('unlike', 0) == unicode(object.id):
            object.likes.remove(profile)
            if hasattr(object, 'score'):
                object.score -= 1
                object.save()

        elif form.get('dislike', 0) == unicode(object.id):
            object.dislikes.add(profile)
            if hasattr(object, 'score'):
                object.score += 1
                object.save()

        elif form.get('undislike', 0) == unicode(object.id):
            object.dislikes.remove(profile)
            if hasattr(object, 'score'):
                object.score -= 1
                object.save()

        elif form.get('commentobject', 0) == unicode(object.id) and 'comment' in form:
            comment = Comment(author=profile,
                              body=form.get('comment'))
            comment.save()
            if hasattr(object, 'score'):
                object.score += 1
                object.save()
            object.comments.add(comment)

    likes = object.likes.all()
    dislikes = object.dislikes.all()
    comments = object.comments.all()

    ilike = profile in likes
    idislike = profile in dislikes
    icommented = comments.filter(author=profile).exists() or \
        comments.filter(author__default_group__in=[
                        profile.default_group_id] + [i.id for i in profile.other_groups.all().only('id')]).exists()

    output = render_to_string('core/tags/comments_likes',
                              {'object': object,
                               'is_update': update,
                               'profile': profile,
                               'likes': likes,
                               'dislikes': dislikes,
                               'comments': comments,
                               'ilike': ilike,
                               'idislike': idislike,
                               'icommented': icommented,
                               'expand': expand},
                              context_instance=RequestContext(request),
                              response_format=response_format)

    dajax.add_data({'target': target, 'content': output}, 'treeio.add_data')
    return dajax.json()

dajaxice_functions.register(comments_likes)


def tags(request, target, object_id, edit=False, formdata={}):
    dajax = Dajax()

    response_format = 'html'
    object = Object.objects.get(pk=object_id)

    tags = object.tags.all()
    form = None
    if 'tags' in formdata and not type(formdata['tags']) == list:
        formdata['tags'] = [formdata['tags']]

    if edit or formdata:
        if formdata.get('tags_object', 0) == unicode(object.id):
            form = TagsForm(tags, formdata)
            if form.is_valid():
                if 'multicomplete_tags' in formdata:
                    tag_names = formdata.get('multicomplete_tags').split(',')
                    new_tags = []
                    for name in tag_names:
                        name = name.strip()
                        if name:
                            try:
                                tag = Tag.objects.get(name=name)
                            except Tag.DoesNotExist:
                                tag = Tag(name=name)
                                tag.save()
                            new_tags.append(tag)
                else:
                    new_tags = form.is_valid()

                object.tags.clear()
                for tag in new_tags:
                    object.tags.add(tag)
                tags = object.tags.all()
                form = None
        else:
            form = TagsForm(tags)

    context = {'object': object,
               'tags': tags,
               'form': form}

    context = converter.preprocess_context(context)

    output = render_to_string('core/ajax/tags_box', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)

    dajax.add_data({'target': target, 'content': output}, 'treeio.add_data')
    return dajax.json()

dajaxice_functions.register(tags)


def attachment(request, object_id, update_id=None):
    dajax = Dajax()

    try:

        if object_id:
            attachments = Attachment.objects.filter(
                attached_object__id=object_id)
            template = 'core/tags/attachments_block'

            object_markup = render_to_string(template,
                                             {'object_id': object_id,
                                                 'attachments': attachments},
                                             context_instance=RequestContext(
                                                 request),
                                             response_format='html')

            dajax.add_data(
                {'target': 'div.attachment-block[object="%s"]' % object_id, 'content': object_markup}, 'treeio.add_data')

        if update_id:
            attachments = Attachment.objects.filter(
                attached_record__id=update_id)
            template = 'core/tags/attachments_record_block'
            update_markup = render_to_string(template,
                                             {'update_id': update_id,
                                                 'attachments': attachments},
                                             context_instance=RequestContext(
                                                 request),
                                             response_format='html')
            dajax.add_data(
                {'target': 'div.attachment-record-block[object="%s"]' % update_id, 'content': update_markup}, 'treeio.add_data')

    except Exception, e:
        print e

    return dajax.json()

dajaxice_functions.register(attachment)


def attachment_delete(request, attachment_id):

    try:
        a = Attachment.objects.get(pk=attachment_id)
    except Attachment.DoesNotExist:
        return

    profile = request.user.get_profile()

    if a.attached_object:
        object_id = a.attached_object.id
        object = Object.objects.get(pk=object_id)
    else:
        object_id = None

    update_id = None
    if a.attached_record:
        update_id = a.attached_record.id
        update = UpdateRecord.objects.get(pk=update_id)
        if not update.author == profile:
            return user_denied(request, message="Only the author of this Update can delete attachments.")

    elif not profile.has_permission(object, mode='w'):
        return user_denied(request, message="You don't have full access to this Object")

    a.delete()

    return attachment(request, object_id, update_id)

dajaxice_functions.register(attachment_delete)


def easy_invite(request, emails=None):

    dajax = Dajax()

    try:
        emails_original = emails
        emails = emails.split(',')

        sender = request.user.get_profile()
        default_group = sender.default_group
        domain = RequestSite(request).domain

        invited = []

        for email in emails:
            email = email.strip()
            if len(email) > 7 and re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is not None:
                invitation = Invitation(
                    sender=request.user.get_profile(), email=email, default_group=default_group)
                invitation.save()
                EmailInvitation(
                    invitation=invitation, sender=sender, domain=domain).send_email()
                invited.append(email)

        if invited:
            template = 'core/tags/easy_invite_success'
        else:
            template = 'core/tags/easy_invite_failure'
    except:
        template = 'core/tags/easy_invite_failure'

    invite_markup = render_to_string(template,
                                     {},
                                     context_instance=RequestContext(request),
                                     response_format='html')

    dajax.add_data({'target': "div.easy-invite[emails='%s']" %
                   (emails_original), 'content': invite_markup}, 'treeio.add_data')
    return dajax.json()

dajaxice_functions.register(easy_invite)
