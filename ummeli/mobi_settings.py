# Django settings for ummeli project.
import os.path
import djcelery

DEBUG = False

try:
    from local_settings import *
except ImportError:
    raise RuntimeError,  "you need a local_settings.py file"


from settings import *

ROOT_URLCONF = 'mobi_urls'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

TEMPLATE_DIRS = (
   "vlive/templates/html",
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
    'vlive.middleware.AddMessageToResponseMiddleware',  # Mobi Only
)
