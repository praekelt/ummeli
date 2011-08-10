from django.conf.urls.defaults import *
from piston.resource import Resource
from ummeli.api.handlers import UserHandler

user_handler = Resource(UserHandler)

urlpatterns = patterns('',
    url(r'^userdata/', user_handler, { 'emitter_format': 'json' }, name='userdata'),
)