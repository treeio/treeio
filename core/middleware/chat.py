# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

# -*- coding:utf-8 -*-

import json
from time import sleep
from django.http import HttpResponse, HttpRequest
from treeio.core.conf import settings
import threading
from datetime import datetime
from time import strftime
from hashlib import md5
import sys
from django.core.cache import cache
import cPickle
from django.contrib.messages.storage import default_storage


def get_key(postfix=""):
    """
    Return key for memcached
    :param postfix: postfix key
    :type postfix: basestring
    """
    domain = getattr(settings, 'CURRENT_DOMAIN', 'default')
    key = "treeio_%s_chat_%s" % (domain, postfix)
    return key


def create_lock(key):
    try:
        while True:
            if cache.add(key + '_lock', '1', 10):  # lifetime lock 10 seconds
                break
        return True
    except:
        print "Error: ", sys.exc_info()
        return False


def delete_lock(key):
    cache.delete(key + '_lock')


def set_memcached(key, obj, lock=True):
    """
    Serialization object and add his in memcached
    """
    if lock:
        if create_lock(key):
            # 60 sec * 60 min * 24 hour * 30 day = 2 592 000 sec
            cache.set(key, cPickle.dumps(obj), 2592000)
            delete_lock(key)
    else:
        cache.set(key, cPickle.dumps(obj), 2592000)


def get_memcached(key):
    """
    Return deserialize object from memcached
    """
    data = cache.get(key)
    if not data:
        set_memcached(key, {})
    obj = cPickle.loads(cache.get(key))
    return obj


def get_notifications(user):
    """
    Return list notifications
    :param user: object user
    """
    notifications = []
    try:
        user.id
    except:
        return []
    try:
        if not getattr(settings, 'HARDTREE_ALLOW_GRITTER_NOTIFICATIONS', False):
            return notifications
        request = HttpRequest()
        request.user = user
        storage = default_storage(request)
        for msg in storage._get()[0]:
            notifications.append({'message': msg.message,
                                  'tags': msg._get_tags()})
        storage._store(None)
    except:
        pass
    return notifications


def get_user_profile(user):
    """
    return user profile
    """
    try:
        listeners = get_memcached(get_key("listeners"))
        return listeners[user]["profile"]
    except:
        return user


def update_user(user, location):
    """
    update location and the last time request Users
    :param user: object user
    :param location: location user on site
    :type location: basestring
    """
    try:
        listeners = get_memcached(get_key("listeners"))
        _user_profile = str(user.get_profile())
        _user = str(user)
        listeners[_user] = {
            "datetime": datetime.now(), "locations": location, "profile": _user_profile}
        set_memcached(get_key("listeners"), listeners)
    except:
        print "Error: ", sys.exc_info()


def remove_user(id, user):
    """
    Remove user from conference
    :param id: ID conference
    :type id: basestring
    :type user: basestring
    """
    conferences = get_memcached(get_key("conferences"))
    if verification_user(id, user):
        del conferences[id]["users"][user]
        set_memcached(get_key("conferences"), conferences)
    return get_new_message_for_user(user)


def verification_user(id, user):
    """
    Verification user in conference
    return True if the user is present in conference, else return False
    :param id: ID conference
    :type id: basestring
    :type user: basestring
    """
    conferences = get_memcached(get_key("conferences"))
    if not user in conferences[id]["users"].keys():
        return False
    return True


def checking_conference(id_conference):
    """
    Checking for the existence of the conference
    :param id_conference: ID conference
    :type id_conference: basestring
    """
    conferences = get_memcached(get_key("conferences"))
    if id_conference in conferences.keys():
        return True
    return False


def is_owner_user(id, user):
    """
    Checks whether user is owner of conferences
    :param id: ID conference
    :type id: basestring
    :type user: basestring
    """
    conferences = get_memcached(get_key("conferences"))
    if conferences[id]["info"]["creator"] == user:
        return True
    return False


def exit_from_conference(id, user):
    """
    Remove user from conference if user exited from conference
    :param id: ID conference
    :type id: basestring
    :type user: basestring
    """
    if checking_conference(id):
        if verification_user(id, user):
            conferences = get_memcached(get_key("conferences"))
            if is_owner_user(id, user):
                delete_conference(id, user)
            del conferences[id]["users"][user]
            set_memcached(get_key("conferences"), conferences)
    return get_new_message_for_user(user)


def delete_conference(id, user):
    """
    Delete conference (if user is owner conference)
    :param id: ID conference
    :type id: basestring
    :type user: basestring
    """
    if is_owner_user(id, user):
        conferences = get_memcached(get_key("conferences"))
        del conferences[id]
        set_memcached(get_key("conferences"), conferences)
    return get_new_message_for_user(user)


def remove_users_in_conference(id, user, users):
    """
    Remove users from conference (if user is owner conference)
    :param id: ID conference
    :type id: basestring
    :type user: basestring
    :type users: baselist
    :param users: List of users to remove from conferences
    """
    if checking_conference(id) and is_owner_user(id, user):
        conferences = get_memcached(get_key("conferences"))
        for val in users:
            del conferences[id]["users"][val]
        set_memcached(get_key("conferences"), conferences)
    return get_new_message_for_user(user)


def add_users_in_conference(id, user, users):
    """
    Add users in conference (if user is owner conference)
    :param id: ID conference
    :type id: basestring
    :type user: basestring
    :type users: baselist
    :param users: List of users to add in conference
    """
    if checking_conference(id):
        conferences = get_memcached(get_key("conferences"))
        for val in users:
            conferences[id]["users"][val] = {"messages": [], "locations": []}
        set_memcached(get_key("conferences"), conferences)
    return get_new_message_for_user(user)


def create_conference(user, users, title):
    """
    Create conference
    :type user: basestring
    :type users: baselist
    :param users: List of users to add in conference
    :type title: basestring
    """
    id = md5()
    id.update(str(datetime.now()))
    id = user + "_" + id.hexdigest()
    users.append(user)
    conferences = get_memcached(get_key("conferences"))
    if id in conferences.keys():
        return get_new_message_for_user(user)
    conferences[id] = {}
    conferences[id]["users"] = {}
    conferences[id]["info"] = {
        "creator": user,
        "title": title,
        "creation_date": datetime.now()
    }
    set_memcached(get_key("conferences"), conferences)
    add_users_in_conference(id, user, users)
    return get_new_message_for_user(user)


def get_active_conferences(user):
    """
    get_active_conferences(user) -> list active conferences
    Return active conferences
    :type user: basestring
    :return: list
    """
    conferences = get_memcached(get_key("conferences"))
    list_conferences = []
    for key in conferences.keys():
        if user in conferences[key]["users"].keys():
            list_conferences.append(
                dict(id=key,
                     title=conferences[key]["info"]["title"],
                     creator=conferences[key]["info"]["creator"],
                     creation_date=str(
                         conferences[key]["info"]["creation_date"]),
                     users=[dict(username=username, profile=get_user_profile(username)) for username in conferences[key]["users"].keys() if not username == user])
            )
    return list_conferences


def get_new_message_for_user(user, **kwargs):
    """
    get_new_message_for_user(user, **kwargs) -> HTTPResponse(json(new_data))
    Return HTTP response to new data
    :type user: basestring
    """
    def __update_data(_data):
        conferences = get_memcached(get_key("conferences"))
        for key in conferences.keys():
            if user in conferences[key]["users"].keys():
                try:
                    msg = conferences[key]["users"][user]["messages"]
                except:
                    msg = []
                if msg:
                    _data["new_data"].append({key: {"messages": msg}})
                    conferences[key]["users"][user]["messages"] = []
                    set_memcached(get_key("conferences"), conferences)
        notifications = get_notifications(kwargs["user_obj"])
        if notifications:
            _data["notifications"] = _data["notifications"] + notifications
        return _data

    def __get_new_data():
        listeners = get_memcached(get_key("listeners"))
        _new_data = {
            "users": [dict(name=key,
                           location=listeners[key]["locations"],
                           profile=listeners[key]["profile"]) for key in listeners.keys() if not key == str(user)],
            "new_data": [],
            "conferences": get_active_conferences(user),
            "notifications": get_notifications(kwargs["user_obj"])
        }
        return _new_data.copy()

    if not "flag" in kwargs.keys():
        kwargs["flag"] = None
    if not "long_polling" in kwargs.keys():
        kwargs["long_polling"] = False
    if "user_obj" in kwargs.keys() and "location" in kwargs.keys():
        _location = kwargs['location']
    else:
        kwargs["user_obj"] = None

    data = __get_new_data()

    if settings.CHAT_LONG_POLLING and kwargs["long_polling"]:

        out_time = 0
        while not data["new_data"] and out_time < settings.CHAT_TIMEOUT:

            if kwargs["user_obj"]:
                if _location:
                    update_user(kwargs["user_obj"], _location)

            out_time += 1

            _temp_data = __get_new_data()
            _temp_data = __update_data(_temp_data)

            if not _temp_data == data:
                data = _temp_data.copy()
                break

            if kwargs["flag"] == "connect":
                break

            if not _temp_data["new_data"]:
                sleep(settings.CHAT_TIME_SLEEP_NEWDATA)
            else:
                data = _temp_data.copy()

    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json', status=200)


def add_new_message(id, user, user_profile, text):
    """
    Add new message
    :param id: ID conference
    :type id: basestring
    :type user: basestring
    :type user_profile: basestring
    :type text: basestring
    """
    try:
        if not verification_user(id, user):
            return get_new_message_for_user(user)
        if checking_conference(id):
            conferences = get_memcached(get_key("conferences"))
            for key in conferences[id]["users"].keys():
                conferences[id]["users"][key]["messages"].append(
                    dict(user=user,
                         text=text,
                         time=strftime("%H:%M:%S"),
                         date=strftime("%Y-%m-%d"),
                         profile=user_profile)
                )
            set_memcached(get_key("conferences"), conferences)
    except:
        data = json.dumps(
            {"cmd": "Error", "data": {"msg": str(sys.exc_info())}})
        return HttpResponse(data, mimetype='application/json', status=200)

    return get_new_message_for_user(user)


def connect(user, location):
    update_user(user, location)
    # if first response, then long_polling = False
    return get_new_message_for_user(str(user).lower(), location=location, long_polling=False, user_obj=user)


def disconnect(user):
    listeners = get_memcached(get_key("listeners"))
    del listeners[user]
    set_memcached(get_key("listeners"), listeners)
    return HttpResponse(json.dumps({"cmd": "Disconnect"}), mimetype='application/json', status=200)


def cmd(message, user):
    """
    Handler AJAX query
    :param user: object user
    :param message: content POST
    :type message: basedict
    """
    try:
        user_obj = user
        user_profile = str(user.get_profile())
        user = str(user).lower()
        data = json.loads(message["json"])
    except:
        print "error: ", sys.exc_info()
        data = json.dumps(
            {"cmd": "Error", "data": {"msg": str(sys.exc_info())}})
        return HttpResponse(data, mimetype='application/json', status=200)

    try:

        update_user(user_obj, data['location'])

        if data['cmd'] == 'Connect':
            return connect(user_obj, data['location'])

        if data['cmd'] == 'Disconnect':
            return disconnect(user)

        if data['cmd'] == 'Get':
            return get_new_message_for_user(user, user_obj=user_obj, location=data['location'], long_polling=True)

        if data['cmd'] == 'Message':
            return add_new_message(data["data"]["id"], user, user_profile, data["data"]["text"])

        if data['cmd'] == 'Exit':
            return exit_from_conference(data["data"]["id"], user)

        if data['cmd'] == 'Delete':
            return delete_conference(data['data']['id'], user)

        if data['cmd'] == 'Remove':
            return remove_users_in_conference(data['data']['id'], user, data['data']['users'])

        if data['cmd'] == 'Add':
            return add_users_in_conference(data['data']['id'], user, data['data']['users'])

        if data['cmd'] == 'Create':
            return create_conference(user, data['data']['users'], data['data']['title'])

    except:
        print "Error: ", sys.exc_info()
        data = json.dumps(
            {"cmd": "Error", "data": {"msg": str(sys.exc_info())}})
        return HttpResponse(data, mimetype='application/json', status=200)

    return HttpResponse(json.dumps({"cmd": "Error", "data": {"msg": "unknown command"}}), mimetype='application/json', status=200)


class Search_Inactive_Users(threading.Thread):

    """
    Delete inactive users
    """

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                sleep(settings.CHAT_TIME_SLEEP_THREAD)
                listeners = get_memcached(get_key("listeners"))
                for user in listeners.keys():
                    time = datetime.now() - listeners[user]['datetime']
                    if time.seconds > settings.CHAT_TIMEOUT:
                        del listeners[user]
                set_memcached(get_key("listeners"), listeners)
            except:
                print "error: ", sys.exc_info()


class ChatAjaxMiddleware(object):

    def __init__(self, *args, **kwargs):
        if not settings.HARDTREE_CRON_DISABLED:
            Search_Inactive_Users().start()
            pass
        # noinspection PyArgumentList
        super(ChatAjaxMiddleware, self).__init__(*args, **kwargs)

    def process_request(self, request):

        if not request.META['PATH_INFO'] == '/chat':
            return

        if not request.user.is_authenticated():
            data = json.dumps(
                {"cmd": "Error", "data": "User is not authenticated"})
            response = HttpResponse(mimetype='application/json')
            response.write(data)
            return response

        if request.method == "POST":
            return cmd(request.POST, request.user)

        return
