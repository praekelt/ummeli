# Django settings for ummeli project.
import os.path
import djcelery

DEBUG = False

try:
    from local_settings import *
except ImportError:
    raise RuntimeError,  "you need a local_settings.py file"


from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'ummeli.db',    # Or path to database file if using sqlite3.
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

NEO4J_DATABASES = {
    'default' : {
        'HOST':'localhost',
        'PORT':7475,
        'ENDPOINT':'/db/data'
    }
}