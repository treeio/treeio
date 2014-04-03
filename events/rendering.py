# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Events module wrappers to be used for rendering
"""
from jinja2 import Markup
from datetime import datetime
from django.core.urlresolvers import reverse

# Percentage of calendar cell used by events in week and day views
CELL_WIDTH = 90


def _smart_truncate(content, length=100, suffix='...'):
    "Smart truncate"
    if len(content) <= length:
        return content
    return content[:length].rsplit(' ', 1)[0] + suffix


class EventRenderer:

    "Basic EventRenderer, used for rendering events, independently of the underlying model"

    name = ""
    start = None
    end = None
    url = ""
    markup = '<p class="%s"><a href="%s" style="%s" class="event popup-link">%s</a></p>'
    rendered = []
    margin_step = {}

    def __init__(self, name, start, end, url, markup=None):
        self.name = name
        self.start = start
        self.end = end
        self.url = url

        if markup:
            self.markup = markup

        self.rendered = []
        self.css_class = 'calendar-event'
        self.style = ''

        self.margin_step = {}

    def __unicode__(self):
        return self.name

    def is_full_day(self, date):
        "True if the event takes place throughout the specified date"
        if self.start and self.end and self.start.date() < date and self.end.date() > date:
            return True
        return False

    def covers(self, date, hour):
        "True if the event covers the given date and/or hour"
        if self.start:
            if self.start.date() < date and self.end.date() > date:
                return True
            elif self.start.date() == date and self.start.hour <= hour:
                if self.end.date() > date:
                    return True
                elif self.end.date() == date and self.end.hour >= hour:
                    if self.end.hour > hour:
                        return True
                    elif self.end.hour == hour and self.end.minute > 0:
                        return True
            elif self.start.date() < date and self.end.date() == date:
                if self.end.hour > hour:
                    return True
                elif self.end.hour == hour and self.end.minute > 0:
                    return True
        elif self.end.date() == date and self.end.hour == hour:
            return True
        return False

    def is_renderable(self, date, hour=None):
        "True if the event should be rendered for the given date and hour"
        if hour:
            if date in self.rendered:
                return False
            if self.start and self.start.date() == date and self.start.hour == hour:
                return True
            elif self.start and self.start.date() < date and self.end.date() == date:
                return True
            elif self.start and self.start.date() < date and self.end.date() > date:
                return True
            elif not self.start and self.end.date() == date and self.end.hour == hour:
                return True
        else:
            if self.start and self.start.date() == date:
                return True
            elif self.end and self.end.date() == date:
                return True
            elif self.start and self.end and self.start.date() < date and self.end.date() > date:
                return True
        return False

    def get_duration(self, date=None, start_hour=8, end_hour=23):
        "Returns duration as hours (float)"
        if date:
            if self.start:
                if self.start.date() < date and self.end.date() > date:
                    return start_hour - end_hour + 1
                else:
                    if self.start.date() == date and self.end.date() > date:
                        start = datetime(
                            date.year, date.month, date.day, start_hour, 0, 0)
                        delta = start - self.start
                    elif self.start.date() < date and self.end.date() == date:
                        start = datetime(
                            date.year, date.month, date.day, start_hour, 0, 0)
                        delta = self.end - start
                    else:
                        delta = self.end - self.start
                    return float(delta.seconds // 3600) + (float(delta.seconds % 3600) / 3600)
            else:
                return 1
        else:
            if self.start and self.end:
                return self.end - self.start
            else:
                return 1

    def render(self, css_class='', style=''):
        "Render event into HTML"
        if not css_class:
            css_class = self.css_class
        else:
            css_class = self.css_class + " " + css_class
        if not style:
            style = self.style
        return Markup(self.markup % (css_class, self.url, style, self.name))

    def render_for_date(self, date, css_class='', style=''):
        "Render event for a certain date"
        output = ""
        if self.is_renderable(date):
            output = self.render(css_class, style)
        return output

    def render_for_datehour(self, date, hour, css_class='', style=''):
        "Render event for a certain date and hour"
        output = ""
        if self.is_renderable(date, hour):
            output = self.render(css_class, style)
            self.rendered.append(date)
        return output


class EventCollection:

    "Set of EventWrappers available for rendering"
    events = []

    def __init__(self, raw_events=[], start_hour=8, end_hour=22):
        "Initialize with raw_events as a list or QuerySet of Events"
        self.events = []
        for event in raw_events:
            wrapper = EventRenderer(event.name, event.start, event.end,
                                    reverse("events_event_view", args=[event.id]))
            self.events.append(wrapper)

        self.start_hour = start_hour
        self.end_hour = end_hour

    def collect_events(self, request):
        "Gathers Events from all user modules where .get_events() callable is available"
        modules = request.user.get_profile().get_perspective().get_modules()

        for module in modules:
            if request.user.get_profile().has_permission(module):
                try:
                    import_name = str(module.name) + ".events"
                    imodule = __import__(
                        import_name, fromlist=[str(module.name)])
                    if hasattr(imodule, 'get_events'):
                        collected = imodule.get_events(request)
                        self.events.extend(collected)
                except:
                    pass

    def renderable_events(self, date, hour):
        "Returns the number of renderable events"
        renderable_events = []

        for event in self.events:
            if event.covers(date, hour):
                renderable_events.append(event)

        if hour:
            for current in renderable_events:
                for event in self.events:
                    if event not in renderable_events:
                        for hour in range(self.start_hour, self.end_hour):
                            if current.covers(date, hour) and event.covers(date, hour):
                                renderable_events.append(event)
                                break

        return renderable_events

    def render_for_date(self, date):
        "Render all events for a certain date"
        output = ""

        for event in self.events:
            if event.is_renderable(date):
                output += event.render_for_date(date)

        return output

    def render_for_datehour(self, date, hour):
        "Render all events for a certain date and hour"
        output = ""

        renderable_events = self.renderable_events(date, hour)
        css_class = "calendar-event-hour"

        if renderable_events:
            width = (90.0 / len(renderable_events))
            current_margin = 0
            for event in renderable_events:
                if str(date) in event.margin_step and event.margin_step[str(date)] > current_margin:
                    current_margin = event.margin_step[str(date)]
            for event in renderable_events:
                if event.is_renderable(date, hour):
                    margin = width * current_margin
                    event.margin_step[
                        str(date)] = current_margin = current_margin + 1
                    if event.is_full_day(date):
                        height = (self.end_hour - self.start_hour + 1) * 40 - 5
                    else:
                        duration = event.get_duration(
                            date, self.start_hour, self.end_hour)
                        if hour + duration > self.end_hour + 1:
                            if event.start.date() == date:
                                duration = self.end_hour - hour + 1
                            else:
                                duration = duration - hour
                        height = duration * float(40) - 5
                    style = "width: %.2f%%; height: %dpx; margin-left: %.2f%%" % (
                        width, height, margin)
                    output += event.render_for_datehour(date,
                                                        hour, css_class, style)

        return output
