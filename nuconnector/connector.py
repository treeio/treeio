# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Everpick connector for Nuvius

Processes data requests to Nuvius and provides
convenience method to simplify data manipulations via
Nuvius data points.

See NUVIUS_URL in settings to configure where Nuvius instance is located
"""

from treeio.core.conf import settings
from django.core.cache import cache
import simplejson as json
import urllib

class DataBlock():
    """
    DataBlock class to provide easier manipulation on the data returned from Nuvius
    
    Allows both, attribute manipulation and key-value manipulation.
    When initialized, recursively build data model from Nuvius JSON-sourced data.
    """
    
    multiblock = ""
    raw = ""
    
    def __init__(self, data):
        self.raw = data
        if isinstance(data, list):
            self.multiblock = list()
            for piece in data:
                block = DataBlock(piece)
                self.multiblock.append(block)
        elif isinstance(data, dict):
            self.multiblock = dict()
            if 'data' in data:
                data = data['data']
            for key in data:
                block = DataBlock(data[key])
                self.multiblock.update({key: block})
        else:
            self.multiblock = data
        self.__setattr__ = self.__setattrnew__
    
    def __len__(self):
        return self.multiblock.__len__()
    
    def __nonzero__(self):
        return self.multiblock.__len__() > 0
    
    def __getitem__(self, key):
        return self.multiblock.__getitem__(key)
    
    def __setitem__(self, key, value):
        self.multiblock.__setitem__(key, value)
    
    def __delitem__(self, key):
        self.multiblock.__delitem__(key)
    
    def __iter__(self):
        return self.multiblock.__iter__()
    
    def __contains__(self, key):
        return self.multiblock.__contains__(key)
    
    def __getattr__(self, item):
        try:
            return self.multiblock.__getitem__(item)
        except KeyError:
            raise AttributeError(unicode(item) + " does not exist. Choices are: " + unicode(self.multiblock.keys()))
        except TypeError:
            raise AttributeError(unicode(item) + " does not exist. This DataBlock is a list, and index must be an integer.")
            
    
    def __setattrnew__(self, item, value):
        self.multiblock.__setitem__(item, value)
    
    def __str__(self):
        return self.multiblock.__str__()
    
    def __repr__(self):
        return self.multiblock.__repr__()
    
    def __unicode__(self):
        if isinstance(self.multiblock, dict) or isinstance(self.multiblock, list):
            return self.multiblock.__str__()
        else:
            return self.multiblock
    
    def __eq__(self, item):
        return self.multiblock.__eq__(item)

    def __ne__(self, item):
        return self.multiblock.__ne__(item)
    
    def append(self, item):
        return self.multiblock.append(item)
    
    def extend(self, iterable):
        return self.multiblock.extend(iterable)
    
    def update(self, item):
        return self.multiblock.update(item)
    
    def get_type(self):
        return type(self.multiblock)

class DataPile():
        
    def __init__(self):
        self.raw = []
        self.raw_collected = []
        self.user_required = []
        self.sources = []
        self.service = None
        self.data = DataBlock({})
        self.data_collected = DataBlock([])
    

class Connector():
    """
    Nuvius Connector simplifies data manipulation for
    data requests between Everpick and Nuvius
    """
    
    nuvius_key = None
    profile_id = None
    profile_key = ''
    base_url = "http://nuvius.com"
    
    def __init__(self, request=None, nuvius_key=None, profile_id=None, profile_key=None):
        """
        Initialize Connector with nuvius_key to use on data requests. or 
        
        nuvius_key is a Nuvius public access key to specify which Nuvius profile
        the Connector should use and fetch data for.
        """
        
        if nuvius_key:
            self.nuvius_key = nuvius_key
        else:
            self.nuvius_key = getattr(settings, 'NUVIUS_KEY', '')
        
        if profile_id:
            self.profile_id = profile_id
        elif request and 'nuvius_id' in request.session:
            self.profile_id = request.session['nuvius_id']
        
        if profile_key:
            self.profile_key = profile_key
        elif request and 'nuvius_profile_key' in request.session:
            self.profile_key = request.session['nuvius_profile_key']
        
        self.base_url = getattr(settings, 'NUVIUS_URL', 'http://nuvius.com')
    
    
    def _make_url(self, url, parameters={}, dataType='json', set_profile_id=True):
        "Creates a Nuvius-friendly URL"
        if not self.base_url in url:
            url = self.base_url + url
        
        if not unicode("." + dataType) in url:
            url += "." + dataType
        
        if self.profile_id and set_profile_id and not "/id" + unicode(self.profile_id) in url:
            url += "/id" + unicode(self.profile_id)
        
        if self.nuvius_key and not 'nuvius_key=' in url:
            parameters.update({'nuvius_key': self.nuvius_key})
        
        if parameters:
            if '?' in url:
                url += '&'
            else:
                url += '?'
            url += urllib.urlencode(parameters)
        
        return url
    
    
    def _get_cache_key(self, url):
        "Produces a cache key for the given URL and nuvius_key"
        
        cache_key = getattr(settings, 'CACHE_KEY_PREFIX', 'treeio_') + "_nuvius_id_" + self.profile_id + "_url_" + url
        return cache_key
    
    
    def toggle_usage(self, app_id, service_id=None, service_url=''):
        "Toggle usage for the given app"
        
        url = "/profile/appmap/" + str(app_id) + "/"
        if service_id:
            url += str(service_id) + "/"
        
        response = self.get(url, 'xml', no_cache=True)
        
        if service_url:
            cache_key = self._get_cache_key(service_url + "view.json")
            if cache.has_key(cache_key):
                return cache.delete(cache_key)
        
        return response
    
    
    def get_profile(self, profile_id=None):
        "Requests Nuvius profile (current or by id if specified)"
        
        if not profile_id:
            profile_id = self.profile_id
        
        url = self._make_url("/profile/view/" + profile_id + ".json", {'profile_key': self.profile_key}, set_profile_id=False)
        
        response = urllib.urlopen(url).read()
        profile = json.loads(response)
        
        return profile
    
    
    def get(self, url, dataType='json', no_cache=False, parameters={}):
        "Make a data GET request to Nuvius"
        
        if not no_cache:
            cache_key = self._get_cache_key(url)
            if self.nuvius_key and cache.has_key(cache_key):
                return cache.get(cache_key)
        
        url = self._make_url(url, dataType=dataType, parameters=parameters)
        
        response = urllib.urlopen(url).read()
        
        if dataType == 'json':
            try:
                data = json.loads(response)
            except Exception:
                data = response
        else:
            data = response
        
        if not no_cache:
            cache.set(cache_key, data, getattr(settings, 'NUVIUS_DATA_CACHE_LIFE', 10))
        
        return data

    def get_app(self, app_id, dataType='json', no_cache=False):
        "Make a data GET request to Nuvius"
        url = '/app/view/' + unicode(app_id)
        
        if not no_cache:
            cache_key = self._get_cache_key(url)
            if self.nuvius_key and cache.has_key(cache_key):
                return cache.get(cache_key)
        
        url = self._make_url(url, dataType=dataType, set_profile_id=False)
        
        response = urllib.urlopen(url).read()
        
        if dataType == 'json':
            try:
                data = json.loads(response)
            except Exception:
                data = response
        else:
            data = response
            
        if not no_cache:
            cache.set(cache_key, data, getattr(settings, 'NUVIUS_DATA_CACHE_LIFE', 10))
        
        return data

    def collect(self, url, no_cache=False, next=None):
        "Collect from all available sources on the URL"
        
        pile = DataPile()
        if not 'collect' in url:
            url += 'collect'
        if not '/service' in url[:8]:
            url = '/service' + url
        
        data = self.get(url, no_cache=no_cache)
        if 'data' in data:
            data = data['data']
            pile.raw = data
            pile.data = DataBlock(data)
            applications = []
            if 'applications' in data['info']:
                applications = data['info']['applications']
            
            if 'service' in data['info']:
                pile.service = data['info']['service']
            
            if applications:
                pile.sources = applications
                
                for response in data['aggregated']:
                    result = response['data']['result']
                    result_name = response['data']['result_name']
                    
                    if result_name == 'success' and result:
                        if isinstance(result, list):
                            pile.raw_collected.extend(result)
                            pile.data_collected.extend(DataBlock(result))
                        else:
                            pile.raw_collected.append(result)
                            pile.data_collected.append(DataBlock(result))
                            
                    elif result_name == 'input-error':
                        pile.user_required.append(response)
                        
                    elif result_name == 'redirect':
                        if next:
                            data_uri = response['data']['data_uri']
                            new_url = self._make_url(data_uri, {'next': next})
                            new_response = self.get(new_url)
                            if new_response['data']['result_name'] == 'redirect':
                                response = new_response
                        pile.user_required.append(response)
        
        return pile
