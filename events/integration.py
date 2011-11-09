# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Events Integration library
"""
from treeio.core.models import Object, ModuleSetting
from treeio.events.models import Event
from nuconnector import Connector, DataBlock
from datetime import datetime

def _clean_missing(resource_id, items, user):
    "Clean items missing from data of their original resource"
    key = '#' + unicode(resource_id) + '.'
    events = Object.filter_permitted(user, Event.objects).filter(nuvius_resource__contains=key)
    if not len(events) == len(items):
        candidates = list(events)
        for event in events:
            for item in items:
                itemkey = key + unicode(item.id.raw)
                if itemkey in event.nuvius_resource:
                    candidates.remove(event)
        for victim in candidates:
            victim.auto_notify = False
            victim.delete()
    

def _find_duplicates(resource_id, item, user):
    "Finds matching items"
    
    dups = []
    item_id = None
    if 'id' in item.raw:
        item_id = item.id.raw
    
    # Finding previously syncd items
    if item_id:
        key = '#' + unicode(resource_id) + '.' + unicode(item_id) + '#' 
        dups = Object.filter_permitted(user, Event.objects).filter(nuvius_resource__contains=key)
        if dups:
            return dups
    
    # Finding equivalent items
    if item.date:
        title = item.title.raw
        start = datetime(*item.date[0].start.raw[:6])
        end = datetime(*item.date[0].end.raw[:6])
        dups = Object.filter_permitted(user, Event.objects).filter(name=title, start=start, end=end)
    
    return dups
    

def _do_sync(data, user):
    "Run updates"
    
    resource_id = data.info.application.id.raw
    
    for item in data.result:
        item_id = None
        if 'id' in item.raw:
            item_id = item.id.raw
        dups = _find_duplicates(resource_id, item, user)
        if dups:
            for event in dups:
                try:
                    event.add_nuvius_resource(resource_id, item_id)
                    event.name = item.title.raw
                    if item.date:
                        idate = item.date[0]
                        event.start = datetime(*idate.start.raw[:6])
                        event.end = datetime(*idate.end.raw[:6])
                    event.auto_notify = False
                    event.save()
                except:
                    pass
        else:
            try:
                event = Event()
                event.add_nuvius_resource(resource_id, item_id)
                event.name = item.title.raw
                if item.date:
                    idate = item.date[0]
                    event.start = datetime(*idate.start.raw[:6])
                    event.end = datetime(*idate.end.raw[:6])
                event.auto_notify = False
                event.set_user(user)
                event.save()
            except:
                pass
            
    _clean_missing(resource_id, data.result, user)
    

def sync(user=None):
    
    if user:
        conf = ModuleSetting.get('nuvius_profile', user=user, strict=True)
    else:
        conf = ModuleSetting.get('nuvius_profile')
    
    for item in conf:
        profile = item.loads()
        user = item.user
        if user:
            connector = Connector(profile_id=profile['id'])
            active_resources = ModuleSetting.get_for_module('treeio.events', 'integration_resource', user=user, strict=True)
            for resource in active_resources:
                res = resource.loads()
                response = connector.get('/service/calendar/event/data.json/id' + profile['id'] + '/app' + str(res.resource_id))
                data = DataBlock(response['data'])
                if data.result_name == 'success':
                    _do_sync(data, user)
