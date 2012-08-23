from django.conf.urls.defaults import patterns, url

from ummeli.opportunities.views import detail


urlpatterns = patterns('',
    url(r'^(?P<slug>[\w-]+)/$', detail, name='detail')
)
