# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Object-related Core templatetags
"""
from coffin import template
from django.template import RequestContext
from jinja2 import contextfunction, Markup
from treeio.core.models import Object, Comment, Tag, UpdateRecord, Attachment
from treeio.core.forms import PermissionForm, ObjectLinksForm, SubscribeForm, TagsForm
from treeio.core.rendering import render_to_string
from treeio.core.ajax import converter
from treeio.core.conf import settings
import re
import urllib

register = template.Library()


@contextfunction
def permission_block(context, object):
    "Block with objects permissions"
    request = context['request']
    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    response_format_tags = response_format
    if 'response_format_tags' in context:
        response_format_tags = context['response_format_tags']

    if 'permission' in request.GET:
        if request.user.get_profile().has_permission(object, mode='w'):
            if request.POST:
                if 'cancel' in request.POST:
                    request.redirect = request.path
                    return Markup(render_to_string('core/tags/permission_block',
                                                   {'object': object,
                                                       'path': request.path},
                                                   context_instance=RequestContext(
                                                       request),
                                                   response_format=response_format))
                form = PermissionForm(request.POST, instance=object)
                if form.is_valid():
                    form.save()
                    request.redirect = request.path
                    return Markup(render_to_string('core/tags/permission_block',
                                                   {'object': object,
                                                       'path': request.path},
                                                   context_instance=RequestContext(
                                                       request),
                                                   response_format=response_format))
            else:
                form = PermissionForm(instance=object)

            context = {'object': object, 'path': request.path, 'form': form}

            if 'ajax' in response_format_tags:
                context = converter.preprocess_context(context)

            return Markup(render_to_string('core/tags/permission_block_edit',
                                           context,
                                           context_instance=RequestContext(
                                               request),
                                           response_format=response_format))

    return Markup(render_to_string('core/tags/permission_block',
                                   {'object': object, 'path': request.path},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(permission_block)


@contextfunction
def link_block(context, object):
    "Block with objects links"

    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    response_format_tags = response_format
    if 'response_format_tags' in context:
        response_format_tags = context['response_format_tags']

    if request.GET and 'link_add' in request.GET:
        if request.POST:

            if 'cancel' in request.POST:
                links = Object.filter_by_request(
                    context['request'], object.links)
                return Markup(render_to_string('core/tags/link_block',
                                               {'object': object, 'links': links,
                                                   'request': request, 'path': request.path},
                                               context_instance=RequestContext(
                                                   request),
                                               response_format=response_format))

            form = ObjectLinksForm(
                request.user.get_profile(), response_format_tags, object, request.POST)

            if form.is_valid() and request.user.get_profile().has_permission(object, mode='w'):
                object.links.add(form.cleaned_data['links'])
                links = Object.filter_by_request(
                    context['request'], object.links)
                return Markup(render_to_string('core/tags/link_block',
                                               {'object': object, 'links': links,
                                                   'request': request, 'path': request.path},
                                               context_instance=RequestContext(
                                                   request),
                                               response_format=response_format))

        links = Object.filter_by_request(context['request'], object.links)
        form = ObjectLinksForm(
            request.user.get_profile(), response_format_tags, instance=object)

        context = {'object': object, 'path': request.path,
                   'form': form, 'links': links}

        if 'ajax' in response_format_tags:
            context = converter.preprocess_context(context)

        rendered_string = render_to_string('core/tags/link_block_edit', context,
                                           context_instance=RequestContext(
                                               request),
                                           response_format=response_format)

        return Markup(rendered_string)

    elif request.GET and 'link_delete' in request.GET:

        if request.user.get_profile().has_permission(object, mode='w'):
            try:
                link = Object.objects.get(pk=request.GET['link_delete'])
                object.links.remove(link)
            except Exception:
                pass

    links = Object.filter_by_request(context['request'], object.links)

    return Markup(render_to_string('core/tags/link_block',
                                   {'object': object, 'links': links, 'request': request,
                                    'path': request.path},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(link_block)


@contextfunction
def subscription_block(context, object):
    "Block with objects subscriptions"

    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    response_format_tags = response_format
    if 'response_format_tags' in context:
        response_format_tags = context['response_format_tags']

    subscriptions = object.subscribers.all()

    subscribed = False
    if request.user.get_profile() in subscriptions:
        subscribed = True

    if 'subscribe_add' in request.GET and request.user.get_profile().has_permission(object, mode='w'):
        if request.POST and 'subscriber' in request.POST:
            if 'cancel' in request.POST:
                request.redirect = request.path
                return Markup(render_to_string('core/tags/subscription_block',
                                               {'object': object, 'subscriptions': subscriptions,
                                                'request': request, 'path': request.path,
                                                'subscribed': subscribed},
                                               context_instance=RequestContext(
                                                   request),
                                               response_format=response_format))
            else:
                form = SubscribeForm(object, request.POST)
                if form.is_valid():
                    subscriptions = form.save()

                request.redirect = request.path
                return Markup(render_to_string('core/tags/subscription_block',
                                               {'object': object, 'subscriptions': subscriptions,
                                                'request': request, 'path': request.path,
                                                'subscribed': subscribed},
                                               context_instance=RequestContext(
                                                   request),
                                               response_format=response_format))

        else:
            form = SubscribeForm(instance=object)

            context = {'object': object, 'subscriptions': subscriptions,
                       'request': request, 'path': request.path,
                       'subscribed': subscribed, 'form': form}

            if 'ajax' in response_format_tags:
                context = converter.preprocess_context(context)

            return Markup(render_to_string('core/tags/subscription_block_add', context,
                          context_instance=RequestContext(request),
                          response_format=response_format))

    if 'subscribe' in request.GET:
        if not subscribed:
            object.subscribers.add(request.user.get_profile())
            subscriptions = object.subscribers.all()
            subscribed = True
    elif 'unsubscribe' in request.GET and request.GET['unsubscribe']:
        user_id = int(request.GET['unsubscribe'])
        try:
            if request.user.get_profile().id == user_id or \
                    request.user.get_profile().has_permission(object, mode='w'):
                object.subscribers.remove(subscriptions.get(pk=user_id))
                subscriptions = object.subscribers.all()
                if user_id == request.user.get_profile().id:
                    subscribed = False
        except Exception:
            pass

    return Markup(render_to_string('core/tags/subscription_block',
                                   {'object': object, 'subscriptions': subscriptions,
                                    'request': request, 'path': request.path,
                                    'subscribed': subscribed},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(subscription_block)


@contextfunction
def comments_likes(context, object, expand=True):
    "Comments and Likes/Dislikes box for an object"

    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    update = isinstance(object, UpdateRecord)
    profile = request.user.get_profile()

    if request.POST.get('like', 0) == unicode(object.id):
        object.likes.add(profile)
        if hasattr(object, 'score'):
            object.score += 1
            object.save()

    elif request.POST.get('unlike', 0) == unicode(object.id):
        object.likes.remove(profile)
        if hasattr(object, 'score'):
            object.score -= 1
            object.save()

    elif request.POST.get('dislike', 0) == unicode(object.id):
        object.dislikes.add(profile)
        if hasattr(object, 'score'):
            object.score += 1
            object.save()

    elif request.POST.get('undislike', 0) == unicode(object.id):
        object.dislikes.remove(profile)
        if hasattr(object, 'score'):
            object.score -= 1
            object.save()

    elif request.POST.get('commentobject', 0) == unicode(object.id) and 'comment' in request.POST:
        comment = Comment(author=profile,
                          body=request.POST.get('comment'))
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

    return Markup(render_to_string('core/tags/comments_likes',
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
                                   response_format=response_format))

register.object(comments_likes)


@contextfunction
def tags_box(context, object):

    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    response_format_tags = response_format
    if 'response_format_tags' in context:
        response_format_tags = context['response_format_tags']

    tags = object.tags.all()
    form = None
    if 'tags-edit' in request.GET:
        if request.POST.get('tags_object', 0) == unicode(object.id):
            form = TagsForm(tags, request.POST)
            if form.is_valid():
                if 'multicomplete_tags' in request.POST:
                    tag_names = request.POST.get(
                        'multicomplete_tags').split(',')
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
               'form': form,
               'editlink': request.path + '?tags-edit'}

    if 'ajax' in response_format_tags:
        context = converter.preprocess_context(context)

    return Markup(render_to_string('core/tags/tags_box', context,
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(tags_box)


@contextfunction
def help_link(context, link=''):
    "Block with objects permissions"
    request = context['request']
    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    if not link:
        url = request.path
        match = re.match('/(?P<url>\w+)(/)?.*', url)
        if match:
            link = match.group('url') + "/"

    link = getattr(settings, 'HARDTREE_HELP_LINK_PREFIX', '/help/') + link

    return Markup(render_to_string('core/tags/help_link_block',
                                   {'link': link},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(help_link)


@contextfunction
def core_generic_list(context, objects, skip_group=False, tag=None):
    "Print a list of objects"

    if tag:
        return tag(context, objects)

    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('core/tags/generic_list',
                                   {'objects': objects,
                                       'skip_group': skip_group},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(core_generic_list)


@contextfunction
def core_watchlist(context, objects=None, skip_group=False, paginate=False):
    "Print a list of objects a user is subscribed to"

    request = context['request']
    profile = request.user.get_profile()

    if not objects:
        objects = profile.subscriptions.all()

    if 'unsubscribe' in request.GET:
        for object in objects.filter(pk=request.GET.get('unsubscribe')):
            object.subscribers.remove(profile)
        objects = profile.subscriptions.all()

    pathurl = request.path + '?'
    if request.GET:
        params = request.GET.copy()
        if 'unsubscribe' in params:
            del params['unsubscribe']
        pathurl += urllib.urlencode(params) + '&'

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('core/tags/watchlist',
                                   {'objects': objects,
                                    'skip_group': skip_group,
                                    'dopaginate': paginate,
                                    'pathurl': pathurl},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(core_watchlist)


@contextfunction
def attachments(context, object=None):
    "Attachments for an object or update record"

    request = context['request']

    profile = request.user.get_profile()

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    update = isinstance(object, UpdateRecord)

    if not update:
        attachments = Attachment.objects.filter(attached_object=object)
        if profile.has_permission(object, mode='w'):
            template = 'core/tags/attachments'
        else:
            template = 'core/tags/attachments_block'

    else:
        attachments = Attachment.objects.filter(attached_record=object)
        if profile == object.author:
            template = 'core/tags/attachments_record'
        else:
            template = 'core/tags/attachments_record_block'

    return Markup(render_to_string(template,
                                   {'object': object,
                                    'attachments': attachments,
                                    },
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(attachments)


@contextfunction
def attachments_block(context, object=None):
    "Attachments for an object or update record"

    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    update = isinstance(object, UpdateRecord)

    if not update:
        attachments = Attachment.objects.filter(attached_object=object)
        template = 'core/tags/attachments_block'
    else:
        attachments = Attachment.objects.filter(attached_record=object)
        template = 'core/tags/attachments_record_block'

    return Markup(render_to_string(template,
                                   {'object': object,
                                    'attachments': attachments,
                                    },
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(attachments_block)


@contextfunction
def attachments_count(context, object=None):
    "Number of Attachments associated with an object"

    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    update = isinstance(object, UpdateRecord)

    if not update:
        count = Attachment.objects.filter(attached_object=object).count()
    else:
        count = Attachment.objects.filter(attached_record=object).count()

    if count:
        return Markup(render_to_string('core/tags/attachments_count',
                                       {'count': count},
                                       context_instance=RequestContext(
                                           request),
                                       response_format=response_format))
    else:
        return('')

register.object(attachments_count)


@contextfunction
def last_updated(context, object=None, verbose=False):
    "The humanized datetime of the last update to an object"

    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    updated = object.last_updated
    return Markup(render_to_string('core/tags/last_updated',
                                   {'updated': updated,
                                    'verbose': verbose},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))


register.object(last_updated)


@contextfunction
def easy_invite_block(context, emails=[]):
    "The humanized datetime of the last update to an object"

    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('core/tags/easy_invite',
                                   {'emails': emails, },
                                   context_instance=RequestContext(request),
                                   response_format=response_format))


register.object(easy_invite_block)
