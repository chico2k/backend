
import time
from sys import stdout
import logging
from elasticsearch_dsl import connections
from .base import *
import os
import socket
from elasticsearch import Elasticsearch

print("###################################################################################")
print("########           Started with Development Settings          #####################")
print("###################################################################################")

INSTALLED_APPS += [
    'mixer',
    'django_elasticsearch_dsl'
]

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',
    'backend',
    'ultigu-test.6qfyr2bjnx.eu-central-1.elasticbeanstalk.com',
]

EMAIL_HOST = 'smtp-server'
EMAIL_PORT = '1025'

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://frontent:3000',
    'http://localhost:8000',
    'http://localhost:8080',
)


# django-debug-toolbar
MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'debug_toolbar_force.middleware.ForceDebugToolbarMiddleware',
    'request_logging.middleware.LoggingMiddleware',
)

INSTALLED_APPS += (
    'debug_toolbar',
    'elastic_panel',
)

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + '1' for ip in ips] + ['127.0.0.1', '10.0.2.2']


DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

DEBUG_TOOLBAR_PANELS = (
    # Defaults
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    # Additional
    'elastic_panel.panel.ElasticDebugPanel',
)

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'elasticsearch:9200'
    },
}


# Name of the Elasticsearch index
ELASTICSEARCH_INDEX_NAMES = {
    'search_indexes.documents.profile': 'profiles',
    'search_indexes.documents.review': 'reviews',
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',  # change debug level as appropiate
            'propagate': False,
        },
    },
}

MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


db_conn = None
while db_conn is not True:
    es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
    db_conn = es.ping()
    print(f'{bcolors.WARNING}Elasticsearch unavailable, waiting 2 seconds...{bcolors.ENDC}')
    if logging.getLogger("elasticsearch").setLevel(logging.CRITICAL) is not None:
        print(logging.getLogger("elasticsearch").setLevel(logging.CRITICAL))
    time.sleep(2)
print(f'{bcolors.OKGREEN}Elasticsearch available!{bcolors.ENDC}')
