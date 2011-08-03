from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^webservice/$', 'ummeli.webservice.views.home'),
	url(r'^webservice/getuserdata/(?P<_username>\w+)/$', 'ummeli.webservice.views.getuserdata'),
    # url(r'^ummeli/', include('ummeli.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
