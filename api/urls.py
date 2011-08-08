from django.conf.urls.defaults import *
from piston.resource import Resource
from ummeli.api.handlers import UserHandler, RegistrationHandler

user_handler = Resource(UserHandler)
registration_handler = Resource(RegistrationHandler)

urlpatterns = patterns('',
    url(r'^getuserdata/', user_handler, { 'emitter_format': 'json' }, name='getuserdata'),
    url(r'^register/', registration_handler, { 'emitter_format': 'json' }, name='register'),
)
