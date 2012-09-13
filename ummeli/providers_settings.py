# Django settings for ummeli project.
import os.path
import djcelery

DEBUG = False

try:
    from local_settings import *
except ImportError:
    raise RuntimeError,  "you need a local_settings.py file"


from settings import *

ROOT_URLCONF = 'providers.urls'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

STATIC_ROOT = abspath('providers-static')
STATIC_URL = '/providers-static/'

STATICFILES_DIRS = (
    abspath('providers/static'),
)

TEMPLATE_DIRS = (
   "providers/templates",
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)
