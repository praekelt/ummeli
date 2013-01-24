from django.conf.urls.defaults import patterns, url
from ummeli.vlive.inbox import views


urlpatterns = patterns('',
    url(r'^$', views.inbox, name='my_inbox'),
    )
