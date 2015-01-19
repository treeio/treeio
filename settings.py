# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

# coding=utf-8

"""
Django settings for treeio project.
"""

from os import path
# assuming settings are in the same dir as source
PROJECT_ROOT = path.abspath(path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

QUERY_DEBUG = False
QUERY_DEBUG_FULL = False

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

from core.db import DatabaseDict
DATABASES = DatabaseDict()

import sys
# Covers regular testing and django-coverage
TESTING = 'test' in sys.argv or 'test_coverage' in sys.argv
if TESTING:
    DATABASES = {'default': {}}
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-GB'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
FORMAT_MODULE_PATH = 'treeio.formats'

HARDTREE_API_CONSUMER_DB = 'default'
# OAUTH_DATA_STORE is needed for correct database setting up
OAUTH_DATA_STORE = 'treeio.core.api.auth.store.store'


# Static files location for Tree.io
STATIC_ROOT = path.join(PROJECT_ROOT, 'static')
STATIC_URL = path.join(PROJECT_ROOT, 'static/')
STATIC_DOC_ROOT = path.join(PROJECT_ROOT, 'static')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = path.join(STATIC_DOC_ROOT, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/media/'

# Captcha Settings
CAPTCHA_FONT_SIZE = 30
CAPTCHA_LENGTH = 6
CAPTCHA_DISABLE = True
CAPTCHA_FOREGROUND_COLOR = '#333333'
CAPTCHA_NOISE_FUNCTIONS = []

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static-admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'z_#oc^n&z0c2lix=s$4+z#lsb9qd32qtb!#78nk7=5$_k3lq16'

# List of callables that know how to import templates from various sources.
# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.load_template_source',
#     'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
# )
if DEBUG or TESTING:
    TEMPLATE_LOADERS = [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
    ]
else:
    TEMPLATE_LOADERS = [
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
            'django.template.loaders.eggs.Loader',
        )),
    ]

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.i18n",
    "django.core.context_processors.debug",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    'django.contrib.messages.context_processors.messages',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'treeio.core.middleware.user.AuthMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    "treeio.core.middleware.user.LanguageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.common.CommonMiddleware',
    'johnny.middleware.LocalStoreClearMiddleware',
    'johnny.middleware.QueryCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    #    'treeio.core.middleware.domain.DomainMiddleware',
    'treeio.core.middleware.user.SSLMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'treeio.core.middleware.chat.ChatAjaxMiddleware',
    "django.contrib.messages.middleware.MessageMiddleware",
    "treeio.core.middleware.modules.ModuleDetect",
    "minidetector.Middleware",
    "treeio.core.middleware.user.CommonMiddleware",
    "treeio.core.middleware.user.PopupMiddleware",
)


ROOT_URLCONF = 'treeio.urls'

TEMPLATE_DIRS = (
    path.join(PROJECT_ROOT, 'templates'),
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.markup',
    'django_websocket',
    'django.contrib.messages',
    'treeio.account',
    'treeio.core',
    'treeio.core.api',
    'treeio.core.search',
    'treeio.documents',
    'treeio.events',
    'treeio.finance',
    'treeio.identities',
    'treeio.infrastructure',
    'treeio.knowledge',
    'treeio.messaging',
    'treeio.news',
    'treeio.projects',
    'treeio.reports',
    'treeio.sales',
    'treeio.services',
    'dajaxice',
    'dajax',
    'coffin',
    'captcha',
    'south',
)


TEST_RUNNER = 'treeio.core.test_runner.CustomTestRunner'

AUTH_PROFILE_MODULE = 'core.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'treeio.core.auth.HashBackend',
    'treeio.core.auth.EmailBackend',
)

# LDAP Configuration
#AUTH_LDAP_SERVER_URI = 'ldap://'
#AUTH_LDAP_BIND_DN = ""
#AUTH_LDAP_BIND_PASSWORD = ""
# AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=users,dc=example,dc=com",
#        ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
#AUTH_LDAP_START_TLS = True

#
# Hardtree configuration
#
HARDTREE_MODULE_IDENTIFIER = 'hmodule'

HARDTREE_DEFAULT_USER_ID = 1

HARDTREE_DEFAULT_PERMISSIONS = 'everyone'

HARDTREE_SEND_EMAIL_TO_CALLER = True

HARDTREE_ALLOW_EMAIL_NOTIFICATIONS = True
HARDTREE_ALLOW_GRITTER_NOTIFICATIONS = True

HARDTREE_PASSWORD_LENGTH_MIN = 4

HARDTREE_RESPONSE_FORMATS = {
    'html': 'text/html',
    'mobile': 'text/html',
    'json': 'text/plain',
    #'json': 'application/json',
    'ajax': 'text/plain',
    #'ajax': 'application/json',
    'csv': 'text/csv',
    'xls': 'text/xls',
    'pdf': 'application/pdf',
    'rss': 'application/rss+xml',
}

HARDTREE_IMAGE_MAX_SIZE = (300, 400)
HARDTREE_IMAGE_RESIZE_FILTER = 'ANTIALIAS'

HARDTREE_MINIFY_JSON = False

HARDTREE_PAGINATOR_LENGTH = 20
HARDTREE_PAGINATOR_PAGES = 15

#
# CRON Fine-tuning
#

# How often should we loop through jobs, add/remove from pool, recycle jobs:
HARDTREE_CRON_PERIOD = 10  # seconds, default 60

# Number of cycles to keep HIGH priority jobs before forcefully terminating
# HARDTREE_CRON_HIGH_PRIORITY = 10 # defualt 10 cycles

# Number of cycles to keep LOW priority jobs before forcefully terminating
# HARDTREE_CRON_LOW_PRIORITY = 3 # default 3 cycles

# Number of seconds since last access to domain to give the job HIGH priority
# HARDTREE_CRON_QUALIFY_HIGH = 10 # default 10 cycles

# Number of seconds since last access to domain to run cron jobs for the domain
# HARDTREE_CRON_QUALIFY_RUN = 86400 # seconds, default 86400, i.e. 1 day

# Number of jobs to keep in the pool at the same time
# HARDTREE_CRON_POOL_SIZE = 10 # default 10

# Priority value at which we should try to gracefully end a job
# HARDTREE_CRON_SOFT_KILL = 0 # defualt 0

# Priority value at which we must kill a job using any possible means (kill -9 job)
# HARDTREE_CRON_HARD_KILL = -1 # defualt -1

# Seconds to wait between SIGKILL signals to a dead job
# HARDTREE_CRON_GRACE_WAIT = 5 # default 5

# CHAT CRON!
HARDTREE_CRON_DISABLED = True  # Run chat?

# CRON config ends here

HARDTREE_MULTIPLE_LOGINS_DISABLED = False

HARDTREE_SERVER_DEFAULT_TIMEZONE = 49  # (GMT+00:00) UTC
HARDTREE_SERVER_TIMEZONE = (('0', u'(GMT-11:00) International Date Line West'),
                            ('1', u'(GMT-11:00) Midway Island'), ('2',
                                                                  u'(GMT-11:00) Samoa'),
                            ('3', u'(GMT-10:00) Hawaii'), ('4',
                                                           u'(GMT-09:00) Alaska'),
                            ('5', u'(GMT-08:00) Tijuana'), ('6',
                                                            u'(GMT-08:00) Pacific Time (US & Canada)'),
                            ('7', u'(GMT-07:00) Arizona'), ('8',
                                                            u'(GMT-07:00) Arizona'),
                            ('9', u'(GMT-08:00) Pacific Time (US & Canada)'), ('10',
                                                                               u'(GMT-07:00) Arizona'),
                            ('11', u'(GMT-07:00) Mountain Time (US & Canada)'), ('12',
                                                                                 u'(GMT-07:00) Chihuahua'),
                            ('13', u'(GMT-07:00) Mazatlan'), ('14',
                                                              u'(GMT-06:00) Central Time (US & Canada)'),
                            ('15', u'(GMT-06:00) Guadalajara'), ('16',
                                                                 u'(GMT-06:00) Mexico City'),
                            ('17', u'(GMT-06:00) Monterrey'), ('18',
                                                               u'(GMT-06:00) Saskatchewan'),
                            ('19', u'(GMT-05:00) Eastern Time (US & Canada)'), ('20',
                                                                                u'(GMT-05:00) Indiana (East)'),
                            ('21', u'(GMT-05:00) Bogota'), ('22',
                                                            u'(GMT-05:00) Lima'),
                            ('23', u'(GMT-05:00) Quito'), ('24',
                                                           u'(GMT-04:30) Caracas'),
                            ('25', u'(GMT-04:00) Atlantic Time (Canada)'), ('26',
                                                                            u'(GMT-04:00) La Paz'),
                            ('27', u'(GMT-04:00) Santiago'), ('28',
                                                              u'(GMT-03:30) Newfoundland'),
                            ('29', u'(GMT-08:00) Pacific Time (US & Canada)'), ('30',
                                                                                u'(GMT-03:00) Brasilia'),
                            ('31', u'(GMT-03:00) Buenos Aires'), ('32',
                                                                  u'(GMT-03:00) Georgetown'),
                            ('33', u'(GMT-03:00) Greenland'), ('34',
                                                               u'(GMT-02:00) Mid-Atlantic'),
                            ('35', u'(GMT-01:00) Azores'), ('36',
                                                            u'(GMT-01:00) Cape Verde Is.'),
                            ('37', u'(GMT+00:00) Casablanca'), ('38',
                                                                u'(GMT+00:00) Dublin'),
                            ('39', u'(GMT+00:00) Edinburgh'), ('40',
                                                               u'(GMT+00:00) Lisbon'),
                            ('41', u'(GMT+00:00) London'), ('42',
                                                            u'(GMT+00:00) Monrovia'),
                            ('43', u'(GMT+00:00) UTC'), ('44',
                                                         u'(GMT+01:00) Amsterdam'),
                            ('45', u'(GMT+01:00) Belgrade'), ('46',
                                                              u'(GMT+01:00) Berlin'),
                            ('47', u'(GMT+01:00) Bern'), ('48',
                                                          u'(GMT+01:00) Bratislava'),
                            ('49', u'(GMT+01:00) Brussels'), ('50',
                                                              u'(GMT+01:00) Budapest'),
                            ('51', u'(GMT+01:00) Copenhagen'), ('52',
                                                                u'(GMT+01:00) Ljubljana'),
                            ('53', u'(GMT+01:00) Madrid'), ('54',
                                                            u'(GMT+01:00) Paris'),
                            ('55', u'(GMT+01:00) Prague'), ('56',
                                                            u'(GMT+01:00) Rome'),
                            ('57', u'(GMT+01:00) Sarajevo'), ('58',
                                                              u'(GMT+01:00) Skopje'),
                            ('59', u'(GMT+01:00) Stockholm'), ('60',
                                                               u'(GMT+01:00) Vienna'),
                            ('61', u'(GMT+01:00) Warsaw'), ('62',
                                                            u'(GMT+01:00) West Central Africa'),
                            ('63', u'(GMT+01:00) Zagreb'), ('64',
                                                            u'(GMT+02:00) Athens'),
                            ('65', u'(GMT+02:00) Bucharest'), ('66',
                                                               u'(GMT+02:00) Cairo'),
                            ('67', u'(GMT+02:00) Harare'), ('68',
                                                            u'(GMT+02:00) Helsinki'),
                            ('69', u'(GMT+02:00) Istanbul'), ('70',
                                                              u'(GMT+02:00) Jerusalem'),
                            ('71', u'(GMT+02:00) Kyev'), ('72',
                                                          u'(GMT+02:00) Minsk'),
                            ('73', u'(GMT+02:00) Pretoria'), ('74',
                                                              u'(GMT+02:00) Riga'),
                            ('75', u'(GMT+02:00) Sofia'), ('76',
                                                           u'(GMT+02:00) Tallinn'),
                            ('77', u'(GMT+02:00) Vilnius'), ('78',
                                                             u'(GMT+03:00) Baghdad'),
                            ('79', u'(GMT+03:00) Kuwait'), ('80',
                                                            u'(GMT+03:00) Moscow'),
                            ('81', u'(GMT+03:00) Nairobi'), ('82',
                                                             u'(GMT+03:00) Riyadh'),
                            ('83', u'(GMT+03:00) St. Petersburg'), ('84',
                                                                    u'(GMT+03:00) Volgograd'),
                            ('85', u'(GMT+03:30) Tehran'), ('86',
                                                            u'(GMT+04:00) Abu Dhabi'),
                            ('87', u'(GMT+04:00) Baku'), ('88',
                                                          u'(GMT+04:00) Muscat'),
                            ('89', u'(GMT+04:00) Tbilisi'), ('90',
                                                             u'(GMT+04:00) Yerevan'),
                            ('91', u'(GMT+04:30) Kabul'), ('92',
                                                           u'(GMT+05:00) Ekaterinburg'),
                            ('93', u'(GMT+05:00) Islamabad'), ('94',
                                                               u'(GMT+05:00) Karachi'),
                            ('95', u'(GMT+05:00) Tashkent'), ('96',
                                                              u'(GMT+05:30) Chennai'),
                            ('97', u'(GMT+05:30) Kolkata'), ('98',
                                                             u'(GMT+05:30) Mumbai'),
                            ('99', u'(GMT+05:30) New Delhi'), ('100',
                                                               u'(GMT+05:30) Sri Jayawardenepura'),
                            ('101', u'(GMT+05:45) Kathmandu'), ('102',
                                                                u'(GMT+06:00) Almaty'),
                            ('103', u'(GMT+06:00) Astana'), ('104',
                                                             u'(GMT+06:00) Dhaka'),
                            ('105', u'(GMT+06:00) Novosibirsk'), ('106',
                                                                  u'(GMT+06:30) Rangoon'),
                            ('107', u'(GMT+07:00) Bangkok'), ('108',
                                                              u'(GMT+07:00) Hanoi'),
                            ('109', u'(GMT+07:00) Jakarta'), ('110',
                                                              u'(GMT+07:00) Krasnoyarsk'),
                            ('111', u'(GMT+08:00) Beijing'), ('112',
                                                              u'(GMT+08:00) Chongqing'),
                            ('113', u'(GMT+08:00) Hong Kong'), ('114',
                                                                u'(GMT+08:00) Irkutsk'),
                            ('115', u'(GMT+08:00) Kuala Lumpur'), ('116',
                                                                   u'(GMT+08:00) Perth'),
                            ('117', u'(GMT+08:00) Singapore'), ('118',
                                                                u'(GMT+08:00) Taipei'),
                            ('119', u'(GMT+08:00) Ulaan Bataar'), ('120',
                                                                   u'(GMT+08:00) Urumqi'),
                            ('121', u'(GMT+09:00) Osaka'), ('122',
                                                            u'(GMT+09:00) Sapporo'),
                            ('123', u'(GMT+09:00) Seoul'), ('124',
                                                            u'(GMT+09:00) Tokyo'),
                            ('125', u'(GMT+09:00) Yakutsk'), ('126',
                                                              u'(GMT+09:30) Adelaide'),
                            ('127', u'(GMT+09:30) Darwin'), ('128',
                                                             u'(GMT+10:00) Brisbane'),
                            ('129', u'(GMT+10:00) Canberra'), ('130',
                                                               u'(GMT+10:00) Guam'),
                            ('131', u'(GMT+10:00) Hobart'), ('132',
                                                             u'(GMT+10:00) Melbourne'),
                            ('133', u'(GMT+10:00) Port Moresby'), ('134',
                                                                   u'(GMT+10:00) Sydney'),
                            ('135', u'(GMT+10:00) Vladivostok'), ('136',
                                                                  u'(GMT+11:00) Magadan'),
                            ('137', u'(GMT+11:00) New Caledonia'), ('138',
                                                                    u'(GMT+11:00) Solomon Is.'),
                            ('139', u'(GMT+12:00) Auckland'), ('140',
                                                               u'(GMT+12:00) Fiji'),
                            ('141', u'(GMT+12:00) Kamchatka'), ('142',
                                                                u'(GMT+12:00) Marshall Is.'),
                            ('143', u'(GMT+12:00) Wellington'), ('144',
                                                                 u'(GMT+13:00) Nukualofa'),
                            )

#
# Messaging
#
HARDTREE_MESSAGING_POP3_LIMIT = 100  # number of emails
HARDTREE_MESSAGING_IMAP_LIMIT = 200  # number of emails

HARDTREE_MESSAGING_UNSAFE_BLOCKS = ('head', 'object', 'embed', 'applet', 'noframes',
                                    'noscript', 'noembed', 'iframe', 'frame', 'frameset')

HARDTREE_MESSAGING_IMAP_DEFAULT_FOLDER_NAME = 'UNSEEN'

HARDTREE_SIGNALS_AUTOCREATE_USER = False

HARDTREE_HELP_LINK_PREFIX = '/help/'
HARDTREE_HELP_SOURCE = 'http://www.tree.io/help'

HARDTREE_LANGUAGES = (('en', u'English'), ('ru', u'Русский'), ('es', u'Español'), ('de', u'Deutsche'), (
    'zh_CN', u'简体中文'), ('fr', u'Français'), ('el', u'ελληνικά'), ('pt_BR', u'português'))
HARDTREE_LANGUAGES_DEFAULT = 'en'

LOCALE_PATHS = (PROJECT_ROOT + "/locale",)

HARDTREE_AJAX_RELOAD_ON_REDIRECT = ('home',
                                    'user_login',
                                    'account_settings_view',
                                    'core_admin_index_perspectives',
                                    'core_admin_perspective_view',
                                    'core_settings_view')

HARDTREE_FORCE_AJAX_RENDERING = True

#
# htsafe settings
#

# Replace unsafe tags
HARDTREE_SAFE_TAGS = ('div', 'ul', 'li', 'label', 'span', 'strong', 'em', 'p', 'input',
                      'select', 'textarea', 'br')
HARDTREE_UNSAFE_TAGS = ('script', 'object', 'embed',
                        'applet', 'noframes', 'noscript', 'noembed', 'iframe',
                        'frame', 'frameset')


#
# Hardtree Subcription settings
#

EVERGREEN_FREE_USERS = 3

USER_PRICE = 15

HARDTREE_SUBSCRIPTION_CUSTOMIZATION = True

HARDTREE_SUBSCRIPTION_USER_LIMIT = 0

HARDTREE_SUBSCRIPTION_BLOCKED = False

HARDTREE_SUBSCRIPTION_SSL_ENABLED = False
HARDTREE_SUBSCRIPTION_SSL_ENFORCE = False

HARDTREE_DEMO_MODE = False


#
# Nuvius settings (for integration)
#
NUVIUS_URL = "http://nuvius.com"
NUVIUS_KEY = '28563.ff6ed93307fc398a52d312966c122660'
NUVIUS_SOURCE_ID = "28563"
NUVIUS_NEXT = "iframe"
NUVIUS_CHECK_USER_KEYS = True

NUVIUS_DATA_CACHE_LIFE = 600
CACHE_KEY_PREFIX = 'treeio_'

#
# Email settings
#

EMAIL_SERVER = 'localhost'
IMAP_SERVER = ''
EMAIL_USERNAME = None
EMAIL_PASSWORD = None
EMAIL_FROM = 'noreply@tree.io'
DEFAULT_SIGNATURE = """
Thanks!
The Tree.io Team
http://www.tree.io
            """


#
# Search index (Whoosh)
#
SEARCH_DISABLED = False
SEARCH_ENGINE = 'db'

from whoosh import fields
WHOOSH_SCHEMA = fields.Schema(id=fields.ID(stored=True, unique=True),
                              name=fields.TEXT(stored=True),
                              type=fields.TEXT(stored=True),
                              content=fields.TEXT,
                              url=fields.ID(stored=True))

WHOOSH_INDEX = path.join(PROJECT_ROOT, 'storage/search')

#
# CACHING
#
#CACHE_BACKEND = 'dummy://'
CACHE_BACKEND = 'locmem://?timeout=30'
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/?timeout=30'

# CACHE_BACKEND="johnny.backends.locmem://"

JOHNNY_MIDDLEWARE_KEY_PREFIX = 'jc_treeio'

DISABLE_QUERYSET_CACHE = False

HARDTREE_OBJECT_BLACKLIST = ['id', 'creator', 'object_name', 'object_type',
                             'trash', 'full_access', 'read_access', 'nuvius_resource',
                             'object_ptr', 'comments', 'likes', 'dislikes', 'tags',
                             'links', 'subscribers', 'read_by']

HARDTREE_UPDATE_BLACKLIST = ['likes', 'dislikes', 'tags', 'reference', 'total',
                             'links', 'subscribers', 'read_by', 'date_created', 'last_updated']

HARDTREE_TIMEZONE_BLACKLIST = [
    'date_created', 'last_updated', 'time_from', 'time_to']

WKPATH = path.join(PROJECT_ROOT, 'bin/wkhtmltopdf')
WKCWD = PROJECT_ROOT

CHAT_LONG_POLLING = False
CHAT_TIMEOUT = 25  # response time if not new data
CHAT_TIME_SLEEP_THREAD = 25  # interval for "Delete inactive users"
CHAT_TIME_SLEEP_NEWDATA = 1  # time sleep in expectation of new data

MESSAGE_STORAGE = 'treeio.core.contrib.messages.storage.cache.CacheStorage'

# Dajaxice settings
DAJAXICE_MEDIA_PREFIX = "dajaxice"
