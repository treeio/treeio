# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Core templatetags
"""
from coffin import template
from jinja2 import contextfunction, contextfilter, Markup
from treeio.core.conf import settings
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode
from django.utils import translation
from django.template.defaultfilters import date as djangodate, time as djangotime
from django.db import models
from treeio.core.rendering import render_to_string
from treeio.core.models import Module, ModuleSetting
from treeio.core.rss import get_secret_key
from treeio.core import sanitizer
from treeio.finance.models import Currency
from datetime import datetime, timedelta
from dajaxice.templatetags.dajaxice_templatetags import dajaxice_js_import as dajaxice_orig_tag
import re
import base64
import urllib


register = template.Library()


def _get_modules(request):
    "Returns set of current modules and active module"
    user = None
    if request.user.username:
        try:
            user = request.user.get_profile()
        except Exception:
            pass

    perspective = user.get_perspective()

    modules = perspective.modules.filter(display=True).order_by('title')
    if not modules:
        modules = Module.objects.filter(display=True).order_by('title')
    active = None

    for module in modules:
        module.type = 'minor'
        try:
            import_name = module.name + "." + \
                settings.HARDTREE_MODULE_IDENTIFIER
            hmodule = __import__(import_name, fromlist=[str(module.name)])
            urls = hmodule.URL_PATTERNS
            for regexp in urls:
                if re.match(regexp, request.path):
                    active = module
            module.type = hmodule.PROPERTIES['type']
        except ImportError:
            pass
        except AttributeError:
            pass
        except KeyError:
            pass

    return modules, active


@contextfunction
def modules_header_block(context):
    "Modules header block"
    request = context['request']
    modules, active = _get_modules(request)

    for module in modules:
        module.title = _(module.title)

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    return Markup(render_to_string('core/tags/modules_header_block',
                                   {'modules': modules,
                                    'active': active,
                                    'request': request},
                                   response_format=response_format))

register.object(modules_header_block)


@contextfunction
def dajaxice_js_import(context):
    "Thin wrapper for dajaxice"

    return Markup(dajaxice_orig_tag(context))

register.object(dajaxice_js_import)


@contextfunction
def modules_active(context):
    "Active modules"
    request = context['request']
    modules, active = _get_modules(request)

    if active:
        return active.name.replace(".", "-")

    return "treeio-home"

register.object(modules_active)


@contextfunction
def paginate(context, items, plength=None):
    "Pagination"
    request = context['request']

    skip = 0
    if 'page_skip' in request.GET:
        try:
            skip = long(request.GET['page_skip'])
        except Exception:
            pass

    if not plength:
        plength = getattr(settings, 'HARDTREE_PAGINATOR_LENGTH', 10)
    length = skip + plength

    return items[skip:length]

register.object(paginate)


@contextfunction
def pager(context, items, plength=None):
    "Pager"
    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    skip = 0
    if 'page_skip' in request.GET:
        try:
            skip = long(request.GET['page_skip'])
        except Exception:
            pass

    if not plength:
        plength = getattr(settings, 'HARDTREE_PAGINATOR_LENGTH', 10)
    if hasattr(items, 'count'):
        try:
            items_length = items.count()
        except:
            items_length = len(items)
    else:
        items_length = len(items)
    pagenum = items_length // plength

    if items_length % plength:
        pagenum += 1

    maxpages = getattr(settings, 'HARDTREE_PAGINATOR_PAGES', 20)

    current = skip // plength
    start = current - (maxpages // 2)
    if pagenum - start < maxpages:
        start = pagenum - maxpages
    if start <= 0:
        start = 1

    pages = []
    if pagenum > 1:
        if current >= 1:
            pages.append(
                {'page': '&larr;', 'skip': (current - 1) * plength, 'mover': True})
        else:
            pages.append({'page': '&larr;', 'skip': 0, 'mover': True})
        if start > 1:
            pages.append(
                {'page': '...', 'skip': (start - 1) * plength, 'mover': False})
            maxpages -= 1
        for i in range(start, pagenum + 1):
            if i > (maxpages + start + 1):
                pages.append(
                    {'page': '...', 'skip': (i) * plength, 'mover': False})
                break
            else:
                pages.append({'page': i, 'skip': (i - 1) * plength})
        if current + 1 == pagenum:
            pages.append(
                {'page': '&rarr;', 'skip': current * plength, 'mover': True})
        else:
            pages.append(
                {'page': '&rarr;', 'skip': (current + 1) * plength, 'mover': True})

    url = request.path + "?"
    if request.GET:
        for arg in request.GET:
            if arg != 'page_skip':
                values = request.GET.getlist(arg)
                for value in values:
                    url += unicode(arg) + "=" + value + "&"

    return Markup(render_to_string('core/tags/pager',
                                   {'url': url, 'pages': pages, 'skip': skip},
                                   response_format=response_format))

register.object(pager)


@contextfunction
def htsort(context, objects):
    "Sort objects based on request"
    if not objects or not 'request' in context:
        # Don't bother trying sorting if we can't do it
        return objects

    request = context['request']

    if not 'sorting' in request.GET or not hasattr(objects, 'order_by') or not hasattr(objects, 'model'):
        # Dont bother if there's nothing to sort on
        return objects

    args = request.GET.getlist('sorting')
    fields = objects.model._meta.get_all_field_names()
    for arg in args:
        field_name = arg.lstrip('-')
        if field_name in fields:
            field = objects.model._meta.get_field(field_name)
            if isinstance(field, models.ManyToManyField):
                agg_field = agg_arg = str('sorting_%s' % field_name)
                if arg[0] == '-':
                    agg_arg = '-' + agg_arg
                kwargs = {agg_field: models.Count(field_name)}
                objects = objects.annotate(**kwargs).order_by(agg_arg)
            else:
                objects = objects.order_by(arg)

    return objects.distinct()

register.object(htsort)


@contextfunction
def htsortlink(context, field_name):
    "Return URL of the sorting field"

    if not 'request' in context:
        return ''
    request = context['request']

    sort_value = field_name
    url = u"%s?" % (request.path)
    if request.GET:
        for arg in request.GET:
            values = request.GET.getlist(arg)
            for value in values:
                svalue = value.lstrip('-')
                if arg == 'sorting' and svalue == field_name:
                    if value[0] != '-':
                        sort_value = u'-%s' % sort_value
                else:
                    url += unicode(arg) + "=" + value + "&"
    url += "sorting=%s" % sort_value

    return url

register.object(htsortlink)


@contextfunction
def object_tree_path(context, object, skipself=False):
    "Object tree path"
    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    path = object.get_tree_path(skipself)

    return Markup(render_to_string('core/tags/object_tree_path',
                                   {'path': path, 'skipself': skipself},
                                   response_format=response_format))

register.object(object_tree_path)


def htsafe(text):
    """
      Strip all unsafe tags

      1. Replace unsafe tags
      2. Return text with 'safe' filter applied --- Alex: Thanks, Cap!
    """
    text = smart_unicode(text)

    safe_string = smart_unicode(sanitizer.clean_html(text))

    return Markup(safe_string)

register.filter('htsafe', htsafe)


def httranslate(text):
    "Translates given string into chosen language"
    return Markup(_(text))

register.object(httranslate)


@contextfunction
def htform(context, form):
    "Set time zone"

    request = context['request']

    user = None
    if request.user.username:
        try:
            user = request.user.get_profile()
        except Exception:
            pass

    # timezone
    default_timezone = settings.HARDTREE_SERVER_DEFAULT_TIMEZONE
    try:
        conf = ModuleSetting.get('default_timezone')[0]
        default_timezone = conf.value
    except:
        pass

    try:
        conf = ModuleSetting.get('default_timezone', user=user)[0]
        default_timezone = conf.value
    except Exception:
        default_timezone = getattr(
            settings, 'HARDTREE_SERVER_TIMEZONE')[default_timezone][0]

    all_timezones = getattr(settings, 'HARDTREE_SERVER_TIMEZONE', [
                            (1, '(GMT-11:00) International Date Line West')])
    title = all_timezones[int(default_timezone)][1]
    GMT = title[4:10]  # with sign e.g. +06:00
    sign = GMT[0:1]  # + or -
    hours = int(GMT[1:3])  # e.g. 06
    mins = int(GMT[4:6])

    if not form.errors:
        for field in form:
            try:
                date = datetime.strptime(
                    str(field.form.initial[field.name]), "%Y-%m-%d %H:%M:%S")
                if date:
                    if sign == "-":
                        field.form.initial[
                            field.name] = date - timedelta(hours=hours, minutes=mins)
                    else:
                        field.form.initial[
                            field.name] = date + timedelta(hours=hours, minutes=mins)
            except:
                pass

    return form

register.object(htform)


@contextfilter
def htdate(context, date, dateformat='DATE_FORMAT'):
    """ Render date in the current locale

    To render date in a custom format use Django format, details:
    http://docs.djangoproject.com/en/dev/ref/templates/builtins/#date

    """

    if not date:
        return ''

    lang = translation.get_language()

    localeformat = dateformat
    formatspath = getattr(settings, 'FORMAT_MODULE_PATH', 'treeio.formats')
    try:
        modulepath = formatspath + "." + lang + ".formats"
        module = __import__(modulepath, fromlist=[str(modulepath)])
        localeformat = getattr(module, dateformat, dateformat)
    except ImportError:
        pass

    request = context['request']

    user = None
    if request.user.username:
        try:
            user = request.user.get_profile()
        except Exception:
            pass

    # timezone
    default_timezone = settings.HARDTREE_SERVER_DEFAULT_TIMEZONE
    try:
        conf = ModuleSetting.get('default_timezone')[0]
        default_timezone = conf.value
    except:
        pass

    try:
        conf = ModuleSetting.get('default_timezone', user=user)[0]
        default_timezone = conf.value
    except Exception:
        default_timezone = getattr(
            settings, 'HARDTREE_SERVER_TIMEZONE')[default_timezone][0]

    all_timezones = getattr(settings, 'HARDTREE_SERVER_TIMEZONE', [
                            (1, '(GMT-11:00) International Date Line West')])
    title = all_timezones[int(default_timezone)][1]
    GMT = title[4:10]  # with sign e.g. +06:00
    sign = GMT[0:1]  # + or -
    hours = int(GMT[1:3])  # e.g. 06
    mins = int(GMT[4:6])

    if sign == "-":
        date = date - timedelta(hours=hours, minutes=mins)
    else:
        date = date + timedelta(hours=hours, minutes=mins)

    result = djangodate(date, localeformat)
    return Markup(result)

register.filter('htdate', htdate)


@contextfilter
def htdatetime(context, date, dateformat='DATETIME_FORMAT'):
    """ Shortcut: render datetime in the current locale """

    if not date:
        return ''

    lang = translation.get_language()

    localeformat = dateformat
    formatspath = getattr(settings, 'FORMAT_MODULE_PATH', 'treeio.formats')
    try:
        modulepath = formatspath + "." + lang + ".formats"
        module = __import__(modulepath, fromlist=[str(modulepath)])
        localeformat = getattr(module, dateformat, dateformat)
    except ImportError:
        pass

    request = context['request']

    user = None
    if request.user.username:
        try:
            user = request.user.get_profile()
        except Exception:
            pass

    # timezone
    default_timezone = settings.HARDTREE_SERVER_DEFAULT_TIMEZONE
    try:
        conf = ModuleSetting.get('default_timezone')[0]
        default_timezone = conf.value
    except:
        pass

    try:
        conf = ModuleSetting.get('default_timezone', user=user)[0]
        default_timezone = conf.value
    except Exception:
        default_timezone = getattr(
            settings, 'HARDTREE_SERVER_TIMEZONE')[default_timezone][0]

    all_timezones = getattr(settings, 'HARDTREE_SERVER_TIMEZONE', [
                            (1, '(GMT-11:00) International Date Line West')])
    title = all_timezones[int(default_timezone)][1]
    GMT = title[4:10]  # with sign e.g. +06:00
    sign = GMT[0:1]  # + or -
    hours = int(GMT[1:3])  # e.g. 06
    mins = int(GMT[4:6])

    if sign == "-":
        date = date - timedelta(hours=hours, minutes=mins)
    else:
        date = date + timedelta(hours=hours, minutes=mins)

    result = djangodate(date, localeformat)

    return Markup(result)

register.filter('htdatetime', htdatetime)


@contextfilter
def httime(context, time, timeformat='TIME_FORMAT'):
    """ Render time in the current locale """

    if not time:
        return ''

    lang = translation.get_language()

    localeformat = timeformat
    formatspath = getattr(settings, 'FORMAT_MODULE_PATH', 'treeio.formats')
    try:
        modulepath = formatspath + "." + lang + ".formats"
        module = __import__(modulepath, fromlist=[str(modulepath)])
        localeformat = getattr(module, timeformat, timeformat)
    except ImportError:
        pass

    request = context['request']

    user = None
    if request.user.username:
        try:
            user = request.user.get_profile()
        except Exception:
            pass

    # timezone
    default_timezone = settings.HARDTREE_SERVER_DEFAULT_TIMEZONE
    try:
        conf = ModuleSetting.get('default_timezone')[0]
        default_timezone = conf.value
    except:
        pass

    try:
        conf = ModuleSetting.get('default_timezone', user=user)[0]
        default_timezone = conf.value
    except Exception:
        default_timezone = getattr(
            settings, 'HARDTREE_SERVER_TIMEZONE')[default_timezone][0]

    all_timezones = getattr(settings, 'HARDTREE_SERVER_TIMEZONE', [
                            (1, '(GMT-11:00) International Date Line West')])
    title = all_timezones[int(default_timezone)][1]
    GMT = title[4:10]  # with sign e.g. +06:00
    sign = GMT[0:1]  # + or -
    hours = int(GMT[1:3])  # e.g. 06
    mins = int(GMT[4:6])

    if sign == "-":
        time = time - timedelta(hours=hours, minutes=mins)
    else:
        time = time + timedelta(hours=hours, minutes=mins)

    result = djangotime(time, localeformat)

    return Markup(result)

register.filter('httime', httime)


@contextfunction
def core_logo_content(context, gif=False):
    "Return current logo encoded as base64"

    staticpath = getattr(settings, 'STATIC_DOC_ROOT', './static')
    logopath = staticpath + '/logo'
    if gif:
        logopath += '.gif'
        mimetype = 'image/gif'
    else:
        logopath += '.png'
        mimetype = 'image/png'

    customlogo = ''
    try:
        conf = ModuleSetting.get_for_module('treeio.core', 'logopath')[0]
        customlogo = getattr(
            settings, 'MEDIA_ROOT', './static/media') + conf.value
    except:
        pass

    logofile = ''
    if customlogo:
        try:
            logofile = open(customlogo, 'r')
        except:
            pass

    if not logofile:
        try:
            logofile = open(logopath, 'r')
        except:
            pass

    result = "data:" + mimetype + ";base64," + \
        base64.b64encode(logofile.read())

    return Markup(result)

register.object(core_logo_content)


MOMENT = 120    # duration in seconds within which the time difference
                # will be rendered as 'a moment ago'


@contextfilter
def humanize_datetime(context, value):
    """
    Finds the difference between the datetime value given and now()
    and returns appropriate humanize form
    """

    request = context['request']

    user = None
    if request.user.username:
        try:
            user = request.user.get_profile()
        except:
            pass

    # timezone
    default_timezone = settings.HARDTREE_SERVER_DEFAULT_TIMEZONE
    try:
        conf = ModuleSetting.get('default_timezone')[0]
        default_timezone = conf.value
    except:
        pass

    try:
        conf = ModuleSetting.get('default_timezone', user=user)[0]
        default_timezone = conf.value
    except Exception:
        default_timezone = getattr(
            settings, 'HARDTREE_SERVER_TIMEZONE')[default_timezone][0]

    all_timezones = getattr(settings, 'HARDTREE_SERVER_TIMEZONE', [
                            (1, '(GMT-11:00) International Date Line West')])
    title = all_timezones[int(default_timezone)][1]
    GMT = title[4:10]  # with sign e.g. +06:00
    sign = GMT[0:1]  # + or -
    hours = int(GMT[1:3])  # e.g. 06
    mins = int(GMT[4:6])

    now = datetime.now()

    if value:
        if sign == "-":
            value = value - timedelta(hours=hours, minutes=mins)
            now = now - timedelta(hours=hours, minutes=mins)
        else:
            value = value + timedelta(hours=hours, minutes=mins)
            now = now + timedelta(hours=hours, minutes=mins)

    if isinstance(value, timedelta):
        delta = value
    elif isinstance(value, datetime):
        delta = now - value
    else:
        delta = None

    if delta:
        if delta.days > 6:                                      # May 15, 17:55
            month = None
            if value.strftime("%b") == 'Jan':
                month = _("Jan")
            elif value.strftime("%b") == 'Feb':
                month = _("Feb")
            elif value.strftime("%b") == 'Mar':
                month = _("Mar")
            elif value.strftime("%b") == 'Apr':
                month = _("Apr")
            elif value.strftime("%b") == 'May':
                month = _("May")
            elif value.strftime("%b") == 'Jun':
                month = _("Jun")
            elif value.strftime("%b") == 'Jul':
                month = _("Jul")
            elif value.strftime("%b") == 'Aug':
                month = _("Aug")
            elif value.strftime("%b") == 'Sep':
                month = _("Sep")
            elif value.strftime("%b") == 'Oct':
                month = _("Oct")
            elif value.strftime("%b") == 'Nov':
                month = _("Nov")
            elif value.strftime("%b") == 'Dec':
                month = _("Dec")
            return month + value.strftime(" %d, %H:%M")

        if delta.days > 1:                                      # Wednesday
            if value.strftime("%A") == 'Monday':
                return _("Monday")
            elif value.strftime("%A") == 'Tuesday':
                return _("Tuesday")
            elif value.strftime("%A") == 'Wednesday':
                return _("Wednesday")
            elif value.strftime("%A") == 'Thursday':
                return _("Thursday")
            elif value.strftime("%A") == 'Friday':
                return _("Friday")
            elif value.strftime("%A") == 'Saturday':
                return _("Saturday")
            elif value.strftime("%A") == 'Sunday':
                return _("Sunday")

        elif delta.days == 1:
            return _("yesterday")                               # yesterday
        elif delta.seconds >= 7200:
            return str(delta.seconds / 3600) + _(" hours ago")  # 3 hours ago
        elif delta.seconds >= 3600:
            return _("1 hour ago")                              # 1 hour ago
        elif delta.seconds > MOMENT:
            # 29 minutes ago
            return str(delta.seconds / 60) + _(" minutes ago")
        else:
            return _("a moment ago")                            # a moment ago
        return djangodate(value)
    else:
        return str(value)

register.filter('humanize_datetime', humanize_datetime)


@contextfilter
def currency_format(context, value, currency=None):
    """
    Adds the currency symbol as set in Sales module settings to a given string
    If the currency has no symbol it adds a three letter code to the end e.g. USD
    """

    # get default currency
    if not currency:
        currency = Currency.objects.get(is_default=True)
    if not currency.symbol:
        return unicode(value) + " " + currency.code
    else:
        return currency.symbol + unicode(value)

register.filter('currency_format', currency_format)


@contextfunction
def currency_print(context, currency=None):
    """
    Just returns the currency symbol as set in Sales module settings to a given string.
    """
    if not currency:
        currency = Currency.objects.get(is_default=True)
    # if currency.symbol:
    #    return unicode(currency.symbol)
    # else:
    return unicode(currency.code)

register.object(currency_print)


@contextfilter
def number_format(context, value):
    """
    Enforces 2 decimal places after a number if only one is given (adds a zero)
    also formats comma separators every 3rd digit before decimal place.
    """
    value = str(value)

    negative = False
    addzero = None

    if value[0] == '-':
        value = value[1:]
        negative = True

    if '.' in value:
        point = value.rindex('.')
        if point == len(value) - 2:
            addzero = True
    else:
        point = len(value)

    # Ensure we don't get lots of zero's after '.'
    # Cut trailing zeros and only leave two
    while point < len(value) - 3:
        if value[len(value) - 1] == '0':
            value = value[:len(value) - 1]
        else:
            break

    while point > 3:
        value = value[:point - 3] + "," + value[point - 3:]
        point = value.index(',')

    if addzero:
        value += "0"

    if negative:
        value = "-" + value

    return value

register.filter('number_format', number_format)


@contextfunction
def show_hint(context, hint=None, object=None):
    "Generic hint framework"

    request = context['request']
    response_format = 'html'

    user = None
    if request.user.username:
        try:
            user = request.user.get_profile()
        except Exception:
            pass

    return Markup(render_to_string('core/hints/' + hint, {'user': user, 'object': object},
                                   response_format=response_format))

register.object(show_hint)


@contextfilter
def group_by_letter(context, object_list):
    "Group contacts by letter"
    res = {}

    for x in object_list:
        # case 1
        r = re.search('^[a-zA-Z]', x.name)
        if r:
            key = r.group().lower()
            if not res.has_key(key):
    #            print "reg", key
                res[key] = [x]
            else:
                res[key].append(x)

        # case 2
        n = re.search('^[0-9_]', x.name)
        if n:
            if not res.has_key('#'):
                res['#'] = [x]
            else:
                res['#'].append(x)

        # case 3
        if not n and not r:
            if not res.has_key('#'):
                res['#'] = [x]
            else:
                res['#'].append(x)

    # converting dictionary to list of tuples, since template support only
    # List.
    l = []
    for k, v in res.items():
        l.append((k, v))
        l.sort(cmp=lambda x, y: cmp(x, y))
    return l

register.filter('group_by_letter', group_by_letter)


@contextfunction
def rss_link(context, url=None):
    "Generic rss link for this URL"

    request = context['request']

    params = request.GET.copy()
    params.update({'secret': get_secret_key(request)})

    if not url:
        url = request.path
    for ext in getattr(settings, 'HARDTREE_RESPONSE_FORMATS', {'html': 'text/html'}):
        url = url.replace('.' + ext, '')
    url += '.rss'
    try:
        url += '?' + urllib.urlencode(params)
    except:
        pass

    return Markup(url)

register.object(rss_link)


@contextfunction
def logo_block_container(context):
    "Returns logo_block_container"

    #request = context['request']
    response_format = 'html'

    return Markup(render_to_string('core/tags/logo_block_container',
                                   response_format=response_format))

register.object(logo_block_container)
