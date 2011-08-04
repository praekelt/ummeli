from django.conf.urls.defaults import *
from piston.resource import Resource
from ummeli.api.handlers import UserHandler

user_handler = Resource(UserHandler)

urlpatterns = patterns('',
   url(r'^getuserdata/(?P<username>\w+)$', user_handler, { 'emitter_format': 'json' }, name='getuserdata_with_name'),
   url(r'^getuserdata/', user_handler, { 'emitter_format': 'json' }, name='getuserdata'),
)
