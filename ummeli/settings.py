# Django settings for ummeli project.
import os.path
import djcelery

DEBUG = False

try:
    from local_settings import *
except ImportError:
    raise RuntimeError,  "you need a local_settings.py file"

TEMPLATE_DEBUG = True

djcelery.setup_loader()

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# --- Environment Specific Settings --- 
ROOT_URLCONF = 'pml_urls'
#ROOT_URLCONF = 'mobi_urls'

TEMPLATE_DIRS = (
   #"vlive/templates/html",
   "vlive/templates/pml",
)

def abspath(*args):
    """convert relative paths to absolute paths relative to PROJECT_ROOT"""
    return os.path.join(PROJECT_ROOT, *args)

ADMINS = ()
SENTRY_ADMINS = ('dev@praekeltfoundation.org',)
MANAGERS = SENTRY_ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ummeli',    # Or path to database file if using sqlite3.
        'USER': 'ummeli',
        'PASSWORD': 'ummeli',
        'HOST': 'localhost',
        'PORT': '',
    }
}

AUTHENTICATION_BACKENDS = (
    # FOR PML ONLY
    'ummeli.vlive.auth.backends.VodafoneLiveUserBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = abspath('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = abspath('ummeli-static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/ummeli-static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/ummeli-static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # '/ummeli/vlive/static',
    abspath('vlive/static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
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
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'vlive.auth.middleware.UserAuthorizationMiddleware',
    'jmbovlive.middleware.VodafoneLiveUserMiddleware',
    'jmbovlive.middleware.VodafoneLiveInfoMiddleware',
    'jmbovlive.middleware.PMLFormActionMiddleware',
    #'vlive.middleware.AddMessageToResponseMiddleware', #Mobi Only
    'jmbovlive.middleware.ModifyPMLResponseMiddleware', # FOR PML ONLY
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
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ummeli.base',
    'ummeli.vlive',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'south',
    'django_nose',
    'djcelery',
    'djcelery_email',
    'gunicorn',
    'sentry',
    'raven.contrib.django',
    
    #ummeli 2.0
    'django.contrib.flatpages',
    'django.contrib.comments',
    
    #jmbo
    'jmboarticles',
    'jmbocomments',
    'jmboarticles.video',
    'jmboarticles.poll',
    'category',
    
    # 3rd party
    'ckeditor',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
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

# If we're running in DEBUG mode then skip RabbitMQ and execute tasks
# immediate instead of deferring them to the queue / workers.
CELERY_ALWAYS_EAGER = DEBUG
CELERY_IMPORTS = ("ummeli.vlive.jobs.tasks", "ummeli.vlive.tasks")
CELERY_RESULT_BACKEND = "amqp"
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
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            [      'Undo', 'Redo',
              '-', 'Bold', 'Italic', 'Underline',
              '-', 'Link', 'Unlink', 'Anchor',
              #'-', 'Format',
              #'-', 'SpellChecker', 'Scayt',
              #'-', 'Maximize',
            ],
            [      'HorizontalRule',
              #'-', 'Table',
              '-', 'BulletedList', 'NumberedList',
              '-', 'Cut','Copy','Paste','PasteText','PasteFromWord',
              #'-', 'SpecialChar',
              '-', 'Source',
              #'-', 'About',
            ]
        ],
        'width': 620,
        'height': 300,
        'toolbarCanCollapse': False,
    }
}

COMMENTS_APP = 'jmbocomments'