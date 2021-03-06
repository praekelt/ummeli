from django.conf.urls.defaults import *
from django.contrib import admin
from ummeli.vlive import views
from django.views.generic.simple import redirect_to

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^ummeli/', include('ummeli.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/None/$', redirect_to, {'url': '/admin/'}),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^health/$', views.health, name="health"),
    url(r'^stats/$', views.stats, name="stats"),
    url(r'^geckoboard/', include('jmbodashboard.geckoboard.urls')),

    url(r'^register/$', views.mobi_register, name='register'),
    url(r'', include('ummeli.vlive.urls')),
)
