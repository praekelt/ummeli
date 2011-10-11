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
    url(r'^api/', include('ummeli.api.urls', namespace='api')),

    url(r'^vlive$', views.login, {'template_name': 'pml/login.xml'},
        name = 'index'),
    url(r'^vlive/', include('ummeli.vlive.urls')),
)
