# Django settings for ummeli project.
import os.path
import djcelery
djcelery.setup_loader()

from datetime import timedelta
CELERYBEAT_SCHEDULE = {
    'exipire-microtasks-every-minute': {
        'task': 'ummeli.opportunities.tasks.microtask_expire_tasks',
        'schedule': timedelta(seconds=60)
    },
    'update-recharge-status-every-minute': {
         'task': 'praekeltpayment.flickswitch.tasks.update_payment_status',
         'schedule': timedelta(seconds=60)
     },
}

DEBUG = False

# vumi credentials for password reset
VUMI_USERNAME = ''
VUMI_PASSWORD = ''

JMBO_ANALYTICS = {
    'google_analytics_id': 'xxx',
}

DJANGO_ATLAS = {
    'google_maps_api_key': 'xxx',
}

PRAEKELT_PAYMENT = {
    'flickswitch_username': 'xxx',
    'flickswitch_password': 'xxx',
    # trailing slash included,
    'flickswitch_url': 'http://api.hotsocket.co.za:8080/test/'
}


TEMPLATE_DEBUG = DEBUG


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# --- Environment Specific Settings ---
ROOT_URLCONF = 'pml_urls'
ROOT_URL = 'http://ummeli.praekeltfoundation.org'
#ROOT_URLCONF = 'mobi_urls'

TEMPLATE_DIRS = (
   #"vlive/templates/html",
   "vlive/templates/pml",
)


def abspath(*args):
    """convert relative paths to absolute paths relative to PROJECT_ROOT"""
    return os.path.join(PROJECT_ROOT, *args)

ADMINS = ()

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ummeli',    # Or path to database file if using sqlite3.
        'USER': 'ummeli',
        'PASSWORD': 'ummeli',
        'HOST': 'localhost',
        'PORT': '',
    }
}

NEO4J_DATABASES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 7474,
        'ENDPOINT': '/db/data'
    }
}

_data_path = os.path.join(PROJECT_ROOT, 'graphing_data')
if not os.path.exists(_data_path):
    os.mkdir(_data_path)

NEO4J_RESOURCE_URI = abspath(_data_path)
NEO4J_OPTIONS = {}
NEO4J_DELETE_KEY = 'ummeli-secret-key'


AUTHENTICATION_BACKENDS = (
    # FOR PML ONLY
    'ummeli.vlive.auth.backends.VodafoneLiveUserBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TIME_ZONE = 'Africa/Johannesburg'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = abspath('ummeli-static/media')
MEDIA_URL = '/ummeli-static/media/'

STATIC_ROOT = abspath('ummeli-static')
STATIC_URL = '/ummeli-static/'

ADMIN_MEDIA_PREFIX = '/ummeli-static/admin/'
STATICFILES_DIRS = (
    abspath('vlive/static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '_l*l+!!^-t6%kzw*ona8y6zgjdq=cn!*8q*b@&k^zn7spa)#)i'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'vlive.auth.middleware.UserAuthorizationMiddleware',
    'jmbovlive.middleware.VodafoneLiveUserMiddleware',
    'jmbovlive.middleware.VodafoneLiveInfoMiddleware',
    'jmbovlive.middleware.PMLFormActionMiddleware',
    'jmbovlive.middleware.ModifyPMLResponseMiddleware',
    'jmbo_analytics.middleware.GoogleAnalyticsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "vlive.custom_context_processors.unique_id_processor",
    "vlive.custom_context_processors.user_profile_processor",
    "vlive.custom_context_processors.province_session_processor",
    "vlive.custom_context_processors.next_url_processor",
    "opportunities.tomtom.context_processors.recognised_device_processor",
)

INSTALLED_APPS = (
    'object_tools',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ummeli.base',
    'ummeli.vlive',
    'ummeli.opportunities',
    'pml',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'south',
    'django_nose',
    'djcelery',
    'djcelery_email',
    'gunicorn',

    #ummeli 2.0
    'django.contrib.flatpages',
    'django.contrib.comments',

    #jmbo
    'jmbo',
    'jmboarticles',
    'jmbocomments',
    'jmboarticles.video',
    'jmboarticles.poll',
    'jmboarticles.featured',
    'category',
    'jmbodashboard.geckoboard',
    'jmbowordsuggest',
    'jmboyourwords',
    'jmbo_analytics',
    'praekeltpayment.flickswitch',

    'downloads',
    'sites_groups',
    'publisher',
    'photologue',
    'secretballot',

    #Ummeli Apps
    'livechat',
    'reporting',

    # 3rd party
    'ckeditor',
    'atlas',
    'django.contrib.gis',
    'tastypie',
    'simple_autocomplete',
    'export',
    'pml',
)

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False
PISTON_DISPLAY_ERRORS = False
AUTH_PROFILE_MODULE = "base.Curriculumvitae"
LOGIN_URL = '/vlive/login/'
LOGIN_REDIRECT_URL = '/vlive/'

CELERY_ALWAYS_EAGER = False
CELERY_IMPORTS = ('ummeli.vlive.jobs.tasks',
                'ummeli.vlive.tasks',
                'jmbo_analytics.tasks',
                'praekeltpayment.flickswitch.api',
                'ummeli.providers.tasks',
                )
CELERY_RESULT_BACKEND = "amqp"
CELERY_TASK_RESULT_EXPIRES = 60

EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'

MAX_LAUNCH_FAXES_COUNT = 2
SEND_FROM_FAX_EMAIL_ADDRESS = 'ummeli@praekeltfoundation.org'
SEND_FROM_EMAIL_ADDRESS = 'ummeli@praekeltfoundation.org'
UMMELI_SUPPORT = 'ummeli.support@praekeltfoundation.org'

# Session Key for PIN auth
UMMELI_PIN_SESSION_KEY = 'ummeli_provided_pin'

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "ummeli"
BROKER_PASSWORD = "ummeli"
BROKER_VHOST = "/ummeli/production"

# CKEDITOR
CKEDITOR_UPLOAD_PATH = MEDIA_ROOT
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            ['Undo', 'Redo',
              '-', 'Bold', 'Italic', 'Underline',
            ],
            ['-', 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord',
              '-', 'Source',
            ]
        ],
        'width': 620,
        'height': 300,
        'toolbarCanCollapse': False,
        'basicEntities': False,
        'forcePasteAsPlainText': True,
        'enterMode': 2,
        'coreStyles_bold': {'element': 'b', 'overrides': 'strong'}
    }
}

COMMENTS_APP = 'jmbocomments'
COMMENTS_PER_PAGE = 15

PML_IGNORE_PATH = ['/vlive/downloads/', '/vlive/jmbo-analytics/', ]
GOOGLE_ANALYTICS_IGNORE_PATH = ['/health/', ]

GEOIP_PATH = abspath('../ve/src/django-atlas/atlas/datasets/MaxMind/')
GEOIP_CITY = 'GeoLiteCity.dat'
GEOIP_COUNTRY = 'GeoIPv6.dat'
SERIALIZATION_MODULES = {
    'csv': 'snippetscream.csv_serializer',
}

REDIS_SETTINGS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0
}
