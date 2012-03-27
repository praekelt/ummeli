from django.conf.urls.defaults import *
from django.contrib import admin
from ummeli.vlive import views

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^ummeli/', include('ummeli.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sentry/', include('sentry.web.urls')),
    url(r'^health/$', views.health, name="health"),
    url(r'^stats/$', views.stats, name="stats"),
    url(r'^geckoboard/', include('jmbodashboard.geckoboard.urls')),

    url(r'^vlive$', views.index, name='index'),
    url(r'^vlive/register/$', views.register, name='register'),
    url(r'^vlive/', include('ummeli.vlive.urls')),
)
