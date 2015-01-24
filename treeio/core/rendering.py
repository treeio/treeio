"""
Rendering routines for Hardtree
"""

from django.http import HttpResponse
from django.contrib.sites.models import RequestSite
from django.utils.translation import ugettext as _
from django.forms import BaseForm
from django.contrib import messages
from jinja2 import Template
from coffin.template import loader
from treeio.core.conf import settings
from treeio.core.models import UpdateRecord
from treeio.core.ajax.converter import preprocess_context as preprocess_context_ajax, convert_to_ajax
import hashlib
import random
import os
import codecs
import re
import subprocess
import json


def _preprocess_context_html(context):
    "Prepares context to be rendered for HTML"

    # Process popuplink fields
    for key in context:
        if isinstance(context[key], BaseForm):
            form = context[key]
            for fname in form.fields:
                field = form.fields[fname]
                try:
                    # find popuplink fields
                    if field.widget.attrs and 'popuplink' in field.widget.attrs:
                        field.help_text += '<a href="%s" field="id_%s" id="link-%s" class="inline-link add-link popup-link">%s</a>' % \
                            (field.widget.attrs['popuplink'], fname, fname, _("New"))
                except Exception:
                    pass

    return context


def render_to_string(template_name, context={}, context_instance=None, response_format='html'):
    "Picks up the appropriate template to render to string"

    if not response_format or 'pdf' in response_format or not response_format in settings.HARDTREE_RESPONSE_FORMATS:
        response_format = 'html'

    if not ("." + response_format) in template_name:
        template_name += "." + response_format

    template_name = response_format + "/" + template_name

    context['response_format'] = response_format
    if context_instance:
        context['site_domain'] = RequestSite(
            context_instance['request']).domain

    context = _preprocess_context_html(context)

    rendered_string = loader.render_to_string(
        template_name, context, context_instance)
    return rendered_string


def render_to_ajax(template_name, context={}, context_instance=None):
    "Render request into JSON object to be handled by AJAX on the server-side"

    response_format = 'html'
    if not 'response_format_tags' in context:
        context['response_format_tags'] = 'ajax'

    context = preprocess_context_ajax(context)
    content = render_to_string(
        template_name, context, context_instance, response_format)
    content = convert_to_ajax(content, context_instance)
    context['content'] = json.dumps(content)

    notifications = []
    if context_instance and 'request' in context_instance:
        request = context_instance['request']
        maxmsgs = 5
        try:
            for message in list(messages.get_messages(request))[:maxmsgs]:
                msgtext = unicode(message)
                if 'updaterecord:' in msgtext[:13]:
                    try:
                        update_id = int(msgtext.split(':', 1)[1])
                        update = UpdateRecord.objects.get(pk=update_id)
                        message = {'message': update.get_full_message(),
                                   'tags': message.tags}
                        if update.author:
                            if update.record_type == 'manual' or update.record_type == 'share':
                                try:
                                    message[
                                        'image'] = update.author.get_contact().get_picture()
                                except:
                                    pass
                            message['title'] = unicode(update.author)
                        for obj in update.about.all():
                            message[
                                'message'] = "(%s) %s:<br />%s" % (obj.get_human_type(), unicode(obj), message['message'])
                        notifications.append(message)
                    except:
                        pass
                else:
                    notifications.append({'message': unicode(message),
                                          'tags': message.tags})
        except:
            pass
    context['notifications'] = json.dumps(notifications)

    rendered_string = render_to_string(
        'ajax_base', context, context_instance, response_format='json')

    return rendered_string


def render_to_response(template_name, context={}, context_instance=None, response_format='html'):
    "Extended render_to_response to support different formats"

    if not response_format:
        response_format = 'html'

    if not response_format in settings.HARDTREE_RESPONSE_FORMATS:
        response_format = 'html'

    mimetype = settings.HARDTREE_RESPONSE_FORMATS[response_format]

    if 'pdf' in response_format:
        while True:
            hasher = hashlib.md5()
            hasher.update(str(random.random()))
            filepath = u"pdfs/" + hasher.hexdigest()
            output = settings.MEDIA_ROOT + filepath
            if not os.path.exists(output + ".pdf"):
                break

        while True:
            hasher = hashlib.md5()
            hasher.update(str(random.random()))
            filepath = hasher.hexdigest() + ".html"
            source = getattr(settings, 'WKCWD', './') + filepath
            if not os.path.exists(source):
                break

        page_size = "A4"
        orientation = "portrait"

        rendered_string = render_to_string(
            template_name, context, context_instance, response_format)

        f = codecs.open(source, encoding='utf-8', mode='w')
        pdf_string = unicode(rendered_string)

        if context_instance and context_instance['request']:
            pdf_string = pdf_string.replace(
                "a href=\"/", "a href=\"http://" + RequestSite(context_instance['request']).domain + "/")

        pdf_string.replace("href=\"/", "href=\"")

        pattern = """Content-Type: text/html|<td>\n\W*<div class="content-list-tick">\n\W.*\n.*</div></td>|<th scope="col">Select</th>"""
        pdf_string = re.sub(pattern, "", pdf_string).replace(
            '/static/', 'static/')

        f.write(pdf_string)
        f.close()

        wkpath = getattr(settings, 'WKPATH', './bin/wkhtmltopdf-i386')
        x = subprocess.Popen("%s --print-media-type --orientation %s --page-size %s %s %s" %
                             (wkpath,
                              orientation,
                              page_size,
                              source,
                              output),
                             shell=True,
                             cwd=getattr(settings, 'WKCWD', './'))
        x.wait()

        f = open(output)
        response = HttpResponse(f.read(), mimetype='application/pdf')
        f.close()

        os.remove(output)
        os.remove(source)

        #response['Content-Disposition'] = 'attachment; filename=%s'%(pdf_name)

        return response

    if 'ajax' in response_format:
        rendered_string = render_to_ajax(
            template_name, context, context_instance)

    else:

        if response_format == 'html' and context_instance and context_instance['request'].path[:3] == '/m/':
            context['response_format'] = response_format = 'mobile'

        if getattr(settings, 'HARDTREE_FORCE_AJAX_RENDERING', False):
            context = preprocess_context_ajax(context)

        rendered_string = render_to_string(
            template_name, context, context_instance, response_format)

    response = HttpResponse(rendered_string, mimetype=mimetype)

    return response


def render_string_template(template_string, context={}, context_instance=None):
    """
    Performs rendering using template_string instead of a file, and context.
    context_instance is only used to feed user into context (unless already defined)

    Returns string.
    """

    template = Template(template_string)
    if not 'user' in context and context_instance:
        if 'request' in context_instance:
            context.update({'user': context_instance['request']})

    return template.render(context)


def get_template_source(template_name, response_format='html'):
    "Returns source of the template file"

    if not response_format or 'pdf' in response_format or not response_format in settings.HARDTREE_RESPONSE_FORMATS:
        response_format = 'html'

    if not ("." + response_format) in template_name:
        template_name += "." + response_format

    template_name = response_format + "/" + template_name

    t = loader.get_template(template_name)
    f = open(t.filename, 'r')

    return f.read()
