# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

from __future__ import division
"""
Reports templatetags
"""
from coffin import template
from treeio.core.rendering import render_to_string
from django.utils.translation import ugettext as _
from jinja2 import contextfunction, Markup
from jinja2.utils import internalcode
from django.template import RequestContext
from random import random
from datetime import datetime
import hashlib
from treeio.reports.helpers import loads, aggregate_functions, number_field_regex
from treeio.reports.views import _get_report_content
import json

register = template.Library()


@contextfunction
def display_chart(context, chart, skip_group=False):
    "Return HTML for chart"

    request = context['request']

    response_format = 'html'
    if 'response_format' in context:
        response_format = context['response_format']

    options = loads(chart.options)

    content = _get_report_content(chart.report, request)

    objs = content['set']

    chart_dict = {}

    field_name = options['grouping']

    model = loads(chart.report.model)

    chart_dict['yAxis'] = {'allowDecimals': False,
                           'title': {'text': model.name.split('.')[-1] + " Count vs. " + field_name.replace('_', ' ').title()}}
    chart_dict['xAxis'] = {}
    try:
        xfield = objs[0]._meta.get_field_by_name(field_name)[0]
    except:
        chart.delete()
        return

    def get_date(g, mindate):
        if g and g != datetime.min.date():
            return g
        else:
            return mindate

    if xfield.get_internal_type() == 'ManyToManyField':
        l = []
        for obj in objs:
            for mi in getattr(obj, field_name).all():
                l.append(unicode(mi))
    elif xfield.get_internal_type() == 'DateTimeField' or xfield.get_internal_type() == 'DateField':
        chart_dict['xAxis']['labels'] = {  # 'rotation':90,
            'align': 'left',
            'x': 3,
            'y': 15}
        l, m, datelist = [], [], []
        maxdate = None
        mindate = None
        for obj in objs:
            if getattr(obj, field_name):
                x = getattr(obj, field_name)
                if xfield.get_internal_type() == 'DateTimeField':
                    x = x.date()
                if not maxdate or x > maxdate:
                    maxdate = x
                if not mindate or x < mindate:
                    mindate = x
                datelist.append(x)
                if unicode(x) not in m:
                    m.append(unicode(x))
            else:
                datelist.append(datetime.min.date())
        while datetime.min.date() in datelist:
            datelist.append(mindate)
            datelist.remove(datetime.min.date())
        datelist = sorted(datelist, key=lambda g: get_date(g, mindate))
        l = [unicode(g) for g in datelist]

        # chart_dict['xAxis']['categories']=m

        chart_dict['xAxis']['type'] = 'datetime'
        td = maxdate - mindate
        #print (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6
        chart_dict['zoomType'] = 'x'
        chart_dict['xAxis']['tickInterval'] = (
            td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6) / 10 ** 4
        #chart_dict['xAxis']['tickWidth']= 0,
        chart_dict['maxZoom'] = 14 * 24 * 3600000  # 2wks
        #chart_dict['xAxis']['gridLineWidth']= 1,
        chart_dict['series'] = [{'name': model.name.split('.')[-1], 'data':[]}]
        for x in set(l):
            chart_dict['series'][0]['data'].append(('%s UTC' % x, l.count(x)))

    else:
        l = [unicode(obj.get_field_value(field_name)) for obj in objs]

    if not 'series' in chart_dict:
        chart_dict['series'] = []
        #chart_dict['series'].append({'name':field_name, 'data': [{'name': x, 'y':l.count(x)} for x in set(l)]})
        chart_dict['series'].append({'name': field_name.replace(
            '_', ' ').title(), 'data': [[x, l.count(x)] for x in set(l)]})
    # for x in set(l):
    #    chart_dict['series'].append({'name':x, 'data': l.count(x)})
    #chart_dict['series'].append({'data':[{'name':x, 'y': [l.count(x)]} for x in set(l)]})
        if not 'xAxis' in chart_dict:
            chart_dict['xAxis']['categories'] = [x for x in set(l)]
        # Chart type specific options

        if 'legend' in options and options['legend'] == 'on':
            chart_dict['legend'] = {
                'layout': 'vertical',
                'align': 'right',
                'verticalAlign': 'top',
                'x': -10,
                'y': 100,
                'borderWidth': 0
            }
    if 'title' in options:
        chart_dict['title'] = {'text': options['title']}

    # Create a hash and use it as a unqiue div id and var name for the chart.
    hasher = hashlib.md5()
    hasher.update(str(random()))
    id = 'chartcontainer' + str(hasher.hexdigest())
    # Disable animation for when saving as PDF
    chart_dict['chart'] = {'renderTo': id,
                           'defaultSeriesType': options['type']}
    #chart_dict['plotOptions'] = {'series': {'animation': False}}

    chart_dict['plotOptions'] = {'pie': {
        'allowPointSelect': True,
        'cursor': 'pointer',
        'dataLabels': {
            'enabled': False
        },
        'showInLegend': True
    }}

    chart_dict['credits'] = {'enabled': False}

    rendered_options = json.dumps(chart_dict)

    rendered_options = rendered_options[
        :-1] + ", tooltip: {formatter: function() {return '<b>'+ this.point.name +'</b>: '+ this.y;}}}"

    if 'type' in chart_dict['xAxis'] and chart_dict['xAxis']['type'] == 'datetime':
        rendered_options += """
        datedata = [];
        jQuery.each(options.series[0].data, function(i,item){
        date = Date.parse(item[0]);
        count = item[1];
        datedata.push([date, count]);
        });
      options.series[0].data = datedata;

      function merge_options(obj1,obj2){
        var obj3 = {};
        for (attrname in obj1) { obj3[attrname] = obj1[attrname]; }
        for (attrname in obj2) { obj3[attrname] = obj2[attrname]; }
        return obj3;
      }
      var dateoptions =  {


      tooltip: {
         shared: true,
         crosshairs: true

      },

      };


    options = merge_options(options, dateoptions);

              """

    return Markup(render_to_string('reports/tags/chart',
                                   {'rendered_options': rendered_options,
                                    'id': id,
                                    'chart_id': chart.id,
                                    'chart': chart,
                                    'name': options['title']},
                                   context_instance=RequestContext(request),
                                   response_format=response_format))

register.object(display_chart)


@internalcode
def is_field_number(report, field_name):
    model = loads(report.model)

    classobj = model.get_class_object()
    field = classobj._meta.get_field_by_name(field_name)[0]

    if number_field_regex.match(field.get_internal_type()):
        return True
    return False

register.object(is_field_number)


@contextfunction
def select_for_aggregation(context, field_name, value):
    select_str = '<select type="select" name="aggregation-%(field_name)s"><option></option>%(options)s</select>'
    options = ''.join(['<option value="%s"%s>%s</option>' % (name, ' selected' if value == name else '',
                                                             _(func['description'])) for name, func in aggregate_functions.items()])
    return Markup(select_str % {'field_name': field_name,
                                'options': options})

register.object(select_for_aggregation)
