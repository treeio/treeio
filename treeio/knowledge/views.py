# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Knowledge Base module views
"""
from django.db.models import Q
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from treeio.knowledge.models import KnowledgeFolder, KnowledgeItem, KnowledgeCategory
from treeio.core.models import Object
from treeio.core.views import user_denied
from treeio.core.rendering import render_to_response
from treeio.core.decorators import treeio_login_required, handle_response_format
from treeio.knowledge.forms import KnowledgeFolderForm, KnowledgeItemForm, KnowledgeCategoryForm, \
    FilterForm, MassActionForm
from django.http import Http404


def _get_filter_query(args):
    "Creates a query to filter Knowledge Items based on FilterForm arguments"
    query = Q()

    for arg in args:
        if hasattr(KnowledgeItem, arg) and args[arg]:
            kwargs = {str(arg + '__id'): long(args[arg])}
            query = query & Q(**kwargs)

    return query


def _get_default_context(request):
    "Returns default context as a dict()"

    folders = Object.filter_permitted(manager=KnowledgeFolder.objects.filter(parent__isnull=True),
                                      user=request.user.get_profile(), mode='r')

    massform = MassActionForm(request.user.get_profile())
    context = {'folders': folders,
               'massform': massform}

    return context


def _process_mass_form(f):
    "Pre-process request to handle mass action form for Knowledge Items"

    def wrap(request, *args, **kwargs):
        "Wrap"
        user = request.user.get_profile()
        if 'massform' in request.POST:
            for key in request.POST:
                if 'mass-item' in key:
                    try:
                        item = KnowledgeItem.objects.get(pk=request.POST[key])
                        form = MassActionForm(user, request.POST, instance=item)
                        if form.is_valid() and user.has_permission(item, mode='w'):
                            form.save()
                    except Exception:
                        pass

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__

    return wrap


@handle_response_format
@treeio_login_required
@_process_mass_form
def index(request, response_format='html'):
    "Knowledge base index page"

    if request.GET:
        query = _get_filter_query(request.GET)
        items = Object.filter_by_request(
            request, KnowledgeItem.objects.filter(query))
    else:
        items = Object.filter_by_request(request, KnowledgeItem.objects)

    filters = FilterForm(request.user.get_profile(), 'name', request.GET)

    context = _get_default_context(request)
    context.update({'filters': filters,
                    'items': items})

    return render_to_response('knowledge/index', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def index_categories(request, response_format='html'):
    "Knowledge base categories page"

    if request.GET:
        query = _get_filter_query(request.GET)
        items = Object.filter_by_request(
            request, KnowledgeItem.objects.filter(query))
    else:
        items = Object.filter_by_request(request, KnowledgeItem.objects)

    filters = FilterForm(request.user.get_profile(), 'category', request.GET)
    categories = Object.filter_by_request(request, KnowledgeCategory.objects)

    context = _get_default_context(request)
    context.update({'filters': filters,
                    'items': items,
                    'categories': categories})

    return render_to_response('knowledge/index_categories', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def folder_add(request, response_format='html'):
    "New folder form"

    if request.POST:
        if not 'cancel' in request.POST:
            folder = KnowledgeFolder()
            form = KnowledgeFolderForm(
                request.user.get_profile(), None, request.POST, instance=folder)
            if form.is_valid():
                folder = form.save()
                folder.set_user_from_request(request)
                return HttpResponseRedirect(reverse('knowledge_folder_view', args=[folder.treepath]))
        else:
            return HttpResponseRedirect(reverse('knowledge'))
    else:
        form = KnowledgeFolderForm(request.user.get_profile(), None)

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('knowledge/folder_add', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def folder_add_folder(request, folderPath, response_format='html'):
    "Add new knowledge folder to preselected folder"

    try:
        folder = KnowledgeFolder.by_path(folderPath)
        knowledgeType_id = folder.id
    except KnowledgeFolder.DoesNotExist:
        raise Http404

    parent = None
    if knowledgeType_id:
        parent = get_object_or_404(KnowledgeFolder, pk=knowledgeType_id)
        if not request.user.get_profile().has_permission(parent, mode='x'):
            parent = None

    if request.POST:
        if not 'cancel' in request.POST:
            folder = KnowledgeFolder()
            form = KnowledgeFolderForm(request.user.get_profile(), knowledgeType_id,
                                       request.POST, instance=folder)
            if form.is_valid():
                folder = form.save()
                folder.set_user_from_request(request)
                return HttpResponseRedirect(reverse('knowledge_folder_view', args=[folder.treepath]))
        else:
            return HttpResponseRedirect(reverse('knowledge'))
    else:
        form = KnowledgeFolderForm(
            request.user.get_profile(), knowledgeType_id)

    context = _get_default_context(request)
    context.update({'form': form,
                    'parent': parent})

    return render_to_response('knowledge/folder_add_folder', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def folder_view(request, folderPath, response_format='html'):
    "Single knowledge folder view page"

    folder = KnowledgeFolder.by_path(folderPath)
    if not folder:
        raise Http404

    if not request.user.get_profile().has_permission(folder):
        return user_denied(request, message="You don't have access to this Knowledge Type")

    items = Object.filter_by_request(
        request, manager=KnowledgeItem.objects.filter(folder=folder))
    subfolders = KnowledgeFolder.objects.filter(parent=folder)

    context = _get_default_context(request)
    context.update({'items': items,
                    'folder': folder,
                    'subfolders': subfolders})

    return render_to_response('knowledge/folder_view', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def folder_edit(request, knowledgeType_id, response_format='html'):
    "Knowledge folder edit page"

    folder = get_object_or_404(KnowledgeFolder, pk=knowledgeType_id)
    items = Object.filter_by_request(
        request, manager=KnowledgeItem.objects.filter(folder=folder))

    if not request.user.get_profile().has_permission(folder, mode="w"):
        return user_denied(request, message="You don't have access to this Knowledge Type")

    if request.POST:
        if not 'cancel' in request.POST:
            form = KnowledgeFolderForm(
                request.user.get_profile(), None, request.POST, instance=folder)
            if form.is_valid():
                folder = form.save()
                return HttpResponseRedirect(reverse('knowledge_folder_view', args=[folder.treepath]))
        else:
            return HttpResponseRedirect(reverse('knowledge_folder_view', args=[folder.treepath]))
    else:
        form = KnowledgeFolderForm(
            request.user.get_profile(), None, instance=folder)

    context = _get_default_context(request)
    context.update({'items': items,
                    'folder': folder,
                    'form': form})

    return render_to_response('knowledge/folder_edit', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def folder_delete(request, knowledgeType_id, response_format='html'):
    "Type delete"

    folder = get_object_or_404(KnowledgeFolder, pk=knowledgeType_id)
    items = Object.filter_by_request(
        request, manager=KnowledgeItem.objects.filter(folder=folder))

    if not request.user.get_profile().has_permission(folder, mode='w'):
        return user_denied(request, message="You don't have access to this Knowledge Type")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                folder.trash = True
                folder.save()
            else:
                folder.delete()
            return HttpResponseRedirect(reverse('knowledge_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('knowledge_folder_view', args=[folder.treepath]))

    context = _get_default_context(request)
    context.update({'items': items,
                    'folder': folder})

    return render_to_response('knowledge/folder_delete', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def item_add(request, response_format='html'):
    "Add new knowledge item"
    items = Object.filter_permitted(
        manager=KnowledgeItem.objects, user=request.user.get_profile(), mode='r')

    if request.POST:
        if not 'cancel' in request.POST:
            item = KnowledgeItem()
            form = KnowledgeItemForm(
                request.user.get_profile(), None, request.POST, instance=item)
            if form.is_valid():
                item = form.save()
                item.set_user_from_request(request)
                return HttpResponseRedirect(reverse('knowledge_item_view',
                                                    args=[item.folder.treepath, item.treepath]))
        else:
            return HttpResponseRedirect(reverse('knowledge'))
    else:
        form = KnowledgeItemForm(request.user.get_profile(), None)

    context = _get_default_context(request)
    context.update({'items': items,
                    'form': form})

    return render_to_response('knowledge/item_add', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def item_add_folder(request, folderPath, response_format='html'):
    "Add new knowledge item to preselected folder"
    items = Object.filter_permitted(
        manager=KnowledgeItem.objects, user=request.user.get_profile(), mode='r')

    try:
        folder = KnowledgeFolder.by_path(folderPath)
        knowledgeType_id = folder.id
    except KnowledgeFolder.DoesNotExist:
        raise Http404

    if request.POST:
        if not 'cancel' in request.POST:
            item = KnowledgeItem()
            form = KnowledgeItemForm(
                request.user.get_profile(), knowledgeType_id, request.POST, instance=item)
            if form.is_valid():
                item = form.save()
                item.set_user_from_request(request)
                return HttpResponseRedirect(reverse('knowledge_item_view',
                                                    args=[item.folder.treepath, item.treepath]))
        else:
            return HttpResponseRedirect(reverse('knowledge'))
    else:
        form = KnowledgeItemForm(request.user.get_profile(), knowledgeType_id)

    context = _get_default_context(request)
    context.update({'items': items,
                    'form': form,
                    'folder': folder})

    return render_to_response('knowledge/item_add_folder', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def item_view(request, folderPath, itemPath, response_format='html'):
    "Single knowledge item view page"

    try:
        item = KnowledgeItem.by_path(folderPath, itemPath)
    except KnowledgeItem.DoesNotExist:
        raise Http404
    if not item:
        raise Http404

    items = Object.filter_permitted(
        manager=KnowledgeItem.objects, user=request.user.get_profile(), mode='r')

    if not request.user.get_profile().has_permission(item):
        return user_denied(request, message="You don't have access to this Knowledge Item")

    context = _get_default_context(request)
    context.update({'items': items,
                    'item': item})

    return render_to_response('knowledge/item_view', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def item_edit(request, knowledgeItem_id, response_format='html'):
    "Knowledge item edit page"
    item = get_object_or_404(KnowledgeItem, pk=knowledgeItem_id)
    items = Object.filter_permitted(
        manager=KnowledgeItem.objects, user=request.user.get_profile(), mode='r')

    if not request.user.get_profile().has_permission(item, mode="w"):
        return user_denied(request, message="You don't have access to this Knowledge Item")

    if request.POST:
        if not 'cancel' in request.POST:
            form = KnowledgeItemForm(
                request.user.get_profile(), None, request.POST, instance=item)
            if form.is_valid():
                item = form.save()
                return HttpResponseRedirect(reverse('knowledge_item_view',
                                                    args=[item.folder.treepath, item.treepath]))
        else:
            return HttpResponseRedirect(reverse('knowledge_item_view',
                                                args=[item.folder.treepath, item.treepath]))
    else:
        form = KnowledgeItemForm(
            request.user.get_profile(), None, instance=item)

    context = _get_default_context(request)
    context.update({'form': form,
                    'item': item,
                    'items': items})

    return render_to_response('knowledge/item_edit', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def item_delete(request, knowledgeItem_id, response_format='html'):
    "Item delete"

    item = get_object_or_404(KnowledgeItem, pk=knowledgeItem_id)
    items = Object.filter_permitted(
        manager=KnowledgeItem.objects, user=request.user.get_profile(), mode='r')

    if not request.user.get_profile().has_permission(item, mode="w"):
        return user_denied(request, message="You don't have access to this Knowledge Item")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                item.trash = True
                item.save()
            else:
                item.delete()
            return HttpResponseRedirect(reverse('knowledge_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('knowledge_item_view',
                                                args=[item.folder.treepath, item.treepath]))

    context = _get_default_context(request)
    context.update({'item': item,
                    'items': items})

    return render_to_response('knowledge/item_delete', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def category_add(request, response_format='html'):
    "Add new knowledge category"

    if request.POST:
        if not 'cancel' in request.POST:
            category = KnowledgeCategory()
            form = KnowledgeCategoryForm(request.POST, instance=category)
            if form.is_valid():
                category = form.save()
                category.set_user_from_request(request)
                return HttpResponseRedirect(reverse('knowledge_category_view', args=[category.treepath]))
        else:
            return HttpResponseRedirect(reverse('knowledge_categories'))
    else:
        form = KnowledgeCategoryForm()

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('knowledge/category_add', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def category_view(request, categoryPath, response_format='html'):
    "Single knowledge category view page"

    try:
        category = KnowledgeCategory.by_path(categoryPath)
    except KnowledgeCategory.DoesNotExist:
        raise Http404

    items = Object.filter_permitted(
        manager=KnowledgeItem.objects, user=request.user.get_profile(), mode='r')

    if not request.user.get_profile().has_permission(category):
        return user_denied(request, message="You don't have access to this Knowledge Category")

    context = _get_default_context(request)
    context.update({'category': category,
                    'items': items})

    return render_to_response('knowledge/category_view', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def category_edit(request, knowledgeCategory_id, response_format='html'):
    "Knowledge category edit page"
    category = get_object_or_404(KnowledgeCategory, pk=knowledgeCategory_id)
    items = Object.filter_permitted(
        manager=KnowledgeItem.objects, user=request.user.get_profile(), mode='r')

    if not request.user.get_profile().has_permission(category, mode="w"):
        return user_denied(request, message="You don't have access to this Knowledge Category")

    if request.POST:
        if not 'cancel' in request.POST:
            form = KnowledgeCategoryForm(request.POST, instance=category)
            if form.is_valid():
                category = form.save()
                return HttpResponseRedirect(reverse('knowledge_category_view', args=[category.treepath]))
        else:
            return HttpResponseRedirect(reverse('knowledge_category_view', args=[category.treepath]))
    else:
        form = KnowledgeCategoryForm(instance=category)

    context = _get_default_context(request)
    context.update({'form': form,
                    'category': category,
                    'items': items})

    return render_to_response('knowledge/category_edit', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def category_delete(request, knowledgeCategory_id, response_format='html'):
    "Knowledge Category delete"

    category = get_object_or_404(KnowledgeCategory, pk=knowledgeCategory_id)
    items = Object.filter_permitted(
        manager=KnowledgeItem.objects, user=request.user.get_profile(), mode='r')

    if not request.user.get_profile().has_permission(category, mode="w"):
        return user_denied(request, message="You don't have access to this Knowledge Category")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                category.trash = True
                category.save()
            else:
                category.delete()
            return HttpResponseRedirect(reverse('knowledge_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('knowledge_category_view', args=[category.treepath]))

    context = _get_default_context(request)
    context.update({'category': category,
                    'items': items})

    return render_to_response('knowledge/category_delete', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)
