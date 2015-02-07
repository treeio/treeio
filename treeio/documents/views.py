# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Documents module views
"""
from django.shortcuts import get_object_or_404
from treeio.core.rendering import render_to_response
from treeio.documents.forms import FolderForm, DocumentForm, FileForm, FilterForm, WebLinkForm, \
    MassActionForm
from django.template import RequestContext
from treeio.documents.models import Document, Folder, File, WebLink
from treeio.core.models import Object
from treeio.core.views import user_denied
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from treeio.core.decorators import treeio_login_required, handle_response_format
from django.http import HttpResponse
from treeio.core.conf import settings
from django.utils.encoding import smart_str


def _get_filter_query(args):
    "Creates a generic query to filter Documents, Files and Weblinks based on FilterForm arguments"
    query = Q()

    for arg in args:
        if hasattr(Document, arg) and args[arg]:
            append = Q(**{str('document__' + arg + '__id'): long(args[arg])})
            append = append | Q(
                **{str('file__' + arg + '__id'): long(args[arg])})
            append = append | Q(
                **{str('weblink__' + arg + '__id'): long(args[arg])})
            query = query & append

    return query


def _get_direct_filter_query(args):
    "Creates a query to filter Documents, Files or Weblinks based on FilterForm arguments"
    query = Q()

    for arg in args:
        if hasattr(Document, arg) and args[arg]:
            append = Q(**{str(arg + '__id'): long(args[arg])})
            query = query & append

    return query


def _get_default_context(request):
    "Returns default context as a dict()"

    folders = Object.filter_by_request(request, Folder.objects, mode="r")
    massform = MassActionForm(request.user.get_profile())

    context = {'folders': folders,
               'massform': massform}

    return context


def _process_mass_form(f):
    "Pre-process request to handle mass action form for Document items"

    def wrap(request, *args, **kwargs):
        "Wrap"
        user = request.user.get_profile()
        if 'massform' in request.POST:
            for key in request.POST:
                if 'mass-object' in key:
                    try:
                        query = Q(object_type='treeio.documents.models.Document') | \
                            Q(object_type='treeio.documents.models.File') | \
                            Q(object_type='treeio.documents.models.WebLink')
                        objects = Object.filter_by_request(
                            request, Object.objects.filter(query))
                        object = objects.get(pk=request.POST[key])
                        form = MassActionForm(
                            user, request.POST, instance=object)
                        if form.is_valid() and user.has_permission(object, mode='w'):
                            form.save()
                    except Exception:
                        pass
                if 'mass-file' in key:
                    try:
                        file = File.objects.get(pk=request.POST[key])
                        form = MassActionForm(
                            user, request.POST, instance=file)
                        if form.is_valid() and user.has_permission(file, mode='w'):
                            form.save()
                    except Exception:
                        pass
                if 'mass-weblink' in key:
                    try:
                        link = WebLink.objects.get(pk=request.POST[key])
                        form = MassActionForm(
                            user, request.POST, instance=link)
                        if form.is_valid() and user.has_permission(link, mode='w'):
                            form.save()
                    except Exception:
                        pass
                if 'mass-document' in key:
                    try:
                        document = Document.objects.get(pk=request.POST[key])
                        form = MassActionForm(
                            user, request.POST, instance=document)
                        if form.is_valid() and user.has_permission(document, mode='w'):
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
    "Index page: displays all Documents"

    query = Q(object_type='treeio.documents.models.Document') | \
        Q(object_type='treeio.documents.models.File') | \
        Q(object_type='treeio.documents.models.WebLink')
    if request.GET:
        query = _get_filter_query(request.GET) & query
        objects = Object.filter_by_request(
            request, Object.objects.filter(query).order_by('-last_updated'))
    else:
        objects = Object.filter_by_request(
            request, Object.objects.filter(query).order_by('-last_updated'))

    filters = FilterForm(request.user.get_profile(), 'title', request.GET)

    context = _get_default_context(request)
    context.update({'filters': filters,
                    'objects': objects})

    return render_to_response('documents/index', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def index_files(request, response_format='html'):
    "Index_files page: displays all Files"

    if request.GET:
        query = _get_direct_filter_query(request.GET)
        files = Object.filter_by_request(
            request, File.objects.filter(query).order_by('-last_updated'))
    else:
        files = Object.filter_by_request(
            request, File.objects.order_by('-last_updated'))

    filters = FilterForm(request.user.get_profile(), 'title', request.GET)

    context = _get_default_context(request)
    context.update({'filters': filters,
                    'files': files})

    return render_to_response('documents/index_files', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def index_weblinks(request, response_format='html'):
    "Index_weblinks page: displays all WebLinks"

    if request.GET:
        query = _get_direct_filter_query(request.GET)
        links = Object.filter_by_request(
            request, WebLink.objects.filter(query).order_by('-last_updated'))
    else:
        links = Object.filter_by_request(
            request, WebLink.objects.order_by('-last_updated'))

    filters = FilterForm(request.user.get_profile(), 'title', request.GET)

    context = _get_default_context(request)
    context.update({'filters': filters,
                    'links': links})

    return render_to_response('documents/index_weblinks', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def index_documents(request, response_format='html'):
    "Index_documents page: displays all Documents"

    if request.GET:
        query = _get_direct_filter_query(request.GET)
        documents = Object.filter_by_request(
            request, Document.objects.filter(query).order_by('-last_updated'))
    else:
        documents = Object.filter_by_request(
            request, Document.objects.order_by('-last_updated'))

    filters = FilterForm(request.user.get_profile(), 'title', request.GET)

    context = _get_default_context(request)
    context.update({'filters': filters,
                    'documents': documents})

    return render_to_response('documents/index_documents', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def folder_add(request, response_format='html'):
    "New folder form"

    if request.POST:
        if not 'cancel' in request.POST:
            folder = Folder()
            form = FolderForm(
                request.user.get_profile(), None, request.POST, instance=folder)
            if form.is_valid():
                folder = form.save()
                folder.set_user_from_request(request)
                return HttpResponseRedirect(reverse('documents_folder_view', args=[folder.id]))
        else:
            return HttpResponseRedirect(reverse('document_index'))
    else:
        form = FolderForm(request.user.get_profile(), None)

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('documents/folder_add', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def folder_add_typed(request, folder_id=None, response_format='html'):
    "Folder add to preselected folder"

    folder = None
    if folder_id:
        folder = get_object_or_404(Folder, pk=folder_id)
        if not request.user.get_profile().has_permission(folder, mode='x'):
            folder = None

    if request.POST:
        if not 'cancel' in request.POST:
            folder = Folder()
            form = FolderForm(
                request.user.get_profile(), folder_id, request.POST, instance=folder)
            if form.is_valid():
                folder = form.save()
                folder.set_user_from_request(request)
                return HttpResponseRedirect(reverse('documents_folder_view', args=[folder.id]))
        else:
            return HttpResponseRedirect(reverse('document_index'))
    else:
        form = FolderForm(request.user.get_profile(), folder_id)

    context = _get_default_context(request)
    context.update({'form': form,
                    'folder': folder})

    return render_to_response('documents/folder_add_typed', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
@_process_mass_form
def folder_view(request, folder_id, response_format='html'):
    "Single folder view page"

    folder = get_object_or_404(Folder, pk=folder_id)

    if not request.user.get_profile().has_permission(folder):
        return user_denied(request, message="You don't have access to this Folder")

    query = Q(
        object_type='treeio.documents.models.Document') | Q(
        object_type='treeio.documents.models.File') | Q(
        object_type='treeio.documents.models.WebLink')
    query = query & (Q(document__folder=folder) | Q(
        file__folder=folder) | Q(weblink__folder=folder))

    if request.GET:
        query = query & _get_filter_query(request.GET)
        objects = Object.filter_by_request(
            request, Object.objects.filter(query).order_by('-last_updated'))
    #    objects = objects.order_by('-last_updated')
    else:
        objects = Object.filter_by_request(
            request, Object.objects.filter(query).order_by('-last_updated'))
    #    objects = objects.order_by('-last_updated')

    subfolders = Folder.objects.filter(parent=folder)
    filters = FilterForm(request.user.get_profile(), 'title', request.GET)

    context = _get_default_context(request)
    context.update({'folder': folder,
                    'objects': objects,
                    'subfolders': subfolders,
                    'filters': filters})

    return render_to_response('documents/folder_view', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def folder_edit(request, folder_id, response_format='html'):
    "Folder edit page"

    folder = get_object_or_404(Folder, pk=folder_id)

    if not request.user.get_profile().has_permission(folder, mode='w'):
        return user_denied(request, message="You don't have access to this Folder")

    if request.POST:
        if not 'cancel' in request.POST:
            form = FolderForm(
                request.user.get_profile(), folder_id, request.POST, instance=folder)
            if form.is_valid():
                folder = form.save()
                return HttpResponseRedirect(reverse('documents_folder_view', args=[folder.id]))
        else:
            return HttpResponseRedirect(reverse('documents_folder_view', args=[folder.id]))

    else:
        form = FolderForm(
            request.user.get_profile(), folder_id, instance=folder)

    context = _get_default_context(request)
    context.update({'form': form,
                    'folder': folder})

    return render_to_response('documents/folder_edit', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def folder_delete(request, folder_id, response_format='html'):
    "Folder delete"

    folder = get_object_or_404(Folder, pk=folder_id)

    if not request.user.get_profile().has_permission(folder, mode='w'):
        return user_denied(request, message="You don't have access to this Folder")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                folder.trash = True
                folder.save()
            else:
                folder.delete()
            return HttpResponseRedirect(reverse('document_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('documents_folder_view', args=[folder.id]))

    query = Q(object_type='treeio.documents.models.Document') | Q(
        object_type='treeio.documents.models.File') | Q(
        object_type='treeio.documents.models.WebLink')
    query = query & (Q(document__folder=folder) | Q(
        file__folder=folder) | Q(weblink__folder=folder))

    if request.GET:
        query = _get_filter_query(request.GET)
        objects = Object.filter_by_request(
            request, Object.objects.filter(query))
   #     objects = objects.order_by('-last_updated')
    else:
        objects = Object.filter_by_request(
            request, Object.objects.filter(query))
   #     objects = objects.order_by('-last_updated')

    context = _get_default_context(request)
    context.update({'folder': folder,
                    'objects': objects})

    return render_to_response('documents/folder_delete', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def document_add(request, response_format='html'):
    "new document form"

    if request.POST:
        if not 'cancel' in request.POST:
            document = Document()
            form = DocumentForm(
                request.user.get_profile(), None, request.POST, instance=document)
            if form.is_valid():
                document = form.save()
                document.set_user_from_request(request)
                return HttpResponseRedirect(reverse('documents_document_view', args=[document.id]))
        else:
            return HttpResponseRedirect(reverse('document_index'))

    else:
        form = DocumentForm(request.user.get_profile(), None)

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('documents/document_add', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def document_add_typed(request, folder_id=None, response_format='html'):
    "Document add to preselected folder"

    folder = None
    if folder_id:
        folder = get_object_or_404(Folder, pk=folder_id)
        if not request.user.get_profile().has_permission(folder, mode='x'):
            folder = None

    document = Document()
    if request.POST:
        if not 'cancel' in request.POST:
            form = DocumentForm(
                request.user.get_profile(), folder_id, request.POST, instance=document)
            if form.is_valid():
                document = form.save()
                document.set_user_from_request(request)
                return HttpResponseRedirect(reverse('documents_document_view', args=[document.id]))
        else:
            return HttpResponseRedirect(reverse('document_index'))
    else:
        form = DocumentForm(request.user.get_profile(), folder_id)

    context = _get_default_context(request)
    context.update({'form': form,
                    'folder': folder})

    return render_to_response('documents/document_add_typed', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def document_view(request, document_id, response_format='html'):
    "Single document view page"

    document = get_object_or_404(Document, pk=document_id)

    if not request.user.get_profile().has_permission(document):
        return user_denied(request, message="You don't have access to this Document")

    context = _get_default_context(request)
    context.update({'document': document})

    return render_to_response('documents/document_view', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def document_edit(request, document_id, response_format='html'):
    "Document edit page"

    document = get_object_or_404(Document, pk=document_id)

    if not request.user.get_profile().has_permission(document, mode='w'):
        return user_denied(request, message="You don't have access to this Document")

    if request.POST:
        if not 'cancel' in request.POST:
            form = DocumentForm(
                request.user.get_profile(), None, request.POST, instance=document)
            if form.is_valid():
                document = form.save()
                return HttpResponseRedirect(reverse('documents_document_view', args=[document.id]))
        else:
            return HttpResponseRedirect(reverse('documents_document_view', args=[document.id]))
    else:
        form = DocumentForm(
            request.user.get_profile(), None, instance=document)

    context = _get_default_context(request)
    context.update({'form': form,
                    'document': document})

    return render_to_response('documents/document_edit', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def document_delete(request, document_id, response_format='html'):
    "Document delete"

    document = get_object_or_404(Document, pk=document_id)

    if not request.user.get_profile().has_permission(document, mode='w'):
        return user_denied(request, message="You don't have access to this Document")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                document.trash = True
                document.save()
            else:
                document.delete()
            return HttpResponseRedirect(reverse('document_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('documents_document_view', args=[document.id]))

    context = _get_default_context(request)
    context.update({'document': document})

    return render_to_response('documents/document_delete', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def file_upload(request, response_format='html'):
    "New file form"

    if request.POST:
        if not 'cancel' in request.POST:
            file = File()
            form = FileForm(
                request.user.get_profile(), None, request.POST, request.FILES, instance=file)
            if form.is_valid():
                file = form.save()
                file.set_user_from_request(request)
                return HttpResponseRedirect(reverse('documents_file_view', args=[file.id]))
        else:
            return HttpResponseRedirect(reverse('document_index'))
    else:
        form = FileForm(request.user.get_profile(), None)

    context = _get_default_context(request)
    context.update({'form': form})

    return render_to_response('documents/file_upload', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def file_upload_typed(request, folder_id=None, response_format='html'):
    "File upload to preselected folder"

    folder = None
    if folder_id:
        folder = get_object_or_404(Folder, pk=folder_id)
        if not request.user.get_profile().has_permission(folder, mode='x'):
            folder = None

    if request.POST:
        if not 'cancel' in request.POST:
            form = FileForm(
                request.user.get_profile(), folder_id, request.POST, request.FILES)
            if form.is_valid():
                file = form.save()
                file.set_user_from_request(request)
                return HttpResponseRedirect(reverse('documents_file_view', args=[file.id]))
        else:
            return HttpResponseRedirect(reverse('document_index'))
    else:
        form = FileForm(request.user.get_profile(), folder_id)

    context = _get_default_context(request)
    context.update({'form': form,
                    'folder': folder})

    return render_to_response('documents/file_upload_typed', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def file_view(request, file_id, response_format='html'):
    "Single file view page"

    file = get_object_or_404(File, pk=file_id)

    if not request.user.get_profile().has_permission(file):
        return user_denied(request, message="You don't have access to this File")

    if request.GET and 'download' in request.GET:
        "Return url to download a file"
        fullpath = getattr(settings, 'MEDIA_ROOT', './static/media/')

        data = ''

        try:
            data = open(fullpath + str(file.content)).read()
        except IOError:
            pass

        response = HttpResponse(data, content_type='application/x-download')
        response[
            'Content-Disposition'] = 'attachment; filename="%s"' % smart_str(file.content)
        return response

    context = _get_default_context(request)
    context.update({'file': file})

    return render_to_response('documents/file_view', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def file_delete(request, file_id, response_format='html'):
    "File delete"

    file = get_object_or_404(File, pk=file_id)
    if not request.user.get_profile().has_permission(file, mode='w'):
        return user_denied(request, message="You don't have access to this File")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                file.trash = True
                file.save()
            else:
                file.delete()
            return HttpResponseRedirect(reverse('document_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('documents_file_view', args=[file.id]))

    context = _get_default_context(request)
    context.update({'file': file})

    return render_to_response('documents/file_delete', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def file_edit(request, file_id, response_format='html'):
    "File edit page"

    file = get_object_or_404(File, pk=file_id)
    if not request.user.get_profile().has_permission(file, mode='w'):
        return user_denied(request, message="You don't have access to this File")

    if request.POST:
        if not 'cancel' in request.POST:
            form = FileForm(
                request.user.get_profile(), None, request.POST, request.FILES, instance=file)
            if form.is_valid():
                file = form.save()
                return HttpResponseRedirect(reverse('documents_file_view', args=[file.id]))
        else:
            return HttpResponseRedirect(reverse('documents_file_view', args=[file.id]))

    else:
        form = FileForm(request.user.get_profile(), None, instance=file)

    context = _get_default_context(request)
    context.update({'form': form,
                    'file': file})

    return render_to_response('documents/file_edit', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


# Web Links
@handle_response_format
@treeio_login_required
def weblink_add(request, response_format='html'):
    "New web link form"

    if request.POST:
        if not 'cancel' in request.POST:
            link = WebLink()
            form = WebLinkForm(
                request.user.get_profile(), None, request.POST, instance=link)
            if form.is_valid():
                link = form.save()
                link.set_user_from_request(request)
                return HttpResponseRedirect(reverse('documents_weblink_view', args=[link.id]))
        else:
            return HttpResponseRedirect(reverse('document_index'))

    else:
        form = WebLinkForm(request.user.get_profile(), None)

    context = _get_default_context(request)
    context.update({'form': form,
                    'file': file})

    return render_to_response('documents/weblink_add', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def weblink_add_typed(request, folder_id=None, response_format='html'):
    "Web link add to preselected folder"

    folder = None
    if folder_id:
        folder = get_object_or_404(Folder, pk=folder_id)
        if not request.user.get_profile().has_permission(folder, mode='x'):
            folder = None

    if request.POST:
        if not 'cancel' in request.POST:
            link = WebLink()
            form = WebLinkForm(
                request.user.get_profile(), folder_id, request.POST, instance=link)
            if form.is_valid():
                link = form.save()
                link.set_user_from_request(request)
                return HttpResponseRedirect(reverse('documents_weblink_view', args=[link.id]))
        else:
            return HttpResponseRedirect(reverse('document_index'))
    else:
        form = WebLinkForm(request.user.get_profile(), folder_id)

    context = _get_default_context(request)
    context.update({'form': form,
                    'folder': folder})

    return render_to_response('documents/weblink_add_typed', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def weblink_view(request, weblink_id, response_format='html'):
    "Weblink page"

    link = get_object_or_404(WebLink, pk=weblink_id)

    if not request.user.get_profile().has_permission(link):
        return user_denied(request, message="You don't have access to this Web Link")

    context = _get_default_context(request)
    context.update({'link': link})

    return render_to_response('documents/weblink_view', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def weblink_edit(request, weblink_id, response_format='html'):
    "WebLink edit page"

    link = get_object_or_404(WebLink, pk=weblink_id)

    if not request.user.get_profile().has_permission(link, mode='w'):
        return user_denied(request, message="You don't have access to this Web Link")

    if request.POST:
        if not 'cancel' in request.POST:
            form = WebLinkForm(
                request.user.get_profile(), None, request.POST, instance=link)
            if form.is_valid():
                link = form.save()
                return HttpResponseRedirect(reverse('documents_weblink_view', args=[link.id]))
        else:
            return HttpResponseRedirect(reverse('documents_weblink_view', args=[link.id]))

    else:
        form = WebLinkForm(request.user.get_profile(), None, instance=link)

    context = _get_default_context(request)
    context.update({'form': form,
                    'link': link})

    return render_to_response('documents/weblink_edit', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)


@handle_response_format
@treeio_login_required
def weblink_delete(request, weblink_id, response_format='html'):
    "WebLink delete"

    link = get_object_or_404(WebLink, pk=weblink_id)

    if not request.user.get_profile().has_permission(link, mode='w'):
        return user_denied(request, message="You don't have access to this Web Link")

    if request.POST:
        if 'delete' in request.POST:
            if 'trash' in request.POST:
                link.trash = True
                link.save()
            else:
                link.delete()
            return HttpResponseRedirect(reverse('document_index'))
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('documents_weblink_view', args=[link.id]))

    context = _get_default_context(request)
    context.update({'link': link})

    return render_to_response('documents/weblink_delete', context,
                              context_instance=RequestContext(request),
                              response_format=response_format)
