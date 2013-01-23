from settings import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': 'ummeli.db',    # Or path to database file if using sqlite3.
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

NEO4J_DATABASES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 7475,
        'ENDPOINT': '/db/data'
    }
}

CELERY_ALWAYS_EAGER = True
