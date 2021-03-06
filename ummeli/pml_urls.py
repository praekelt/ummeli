from django.conf.urls.defaults import *
from django.contrib import admin
from ummeli.vlive import views
from django.views.generic.simple import redirect_to
from django.views.generic import TemplateView

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

    url(r'^vlive$', views.index, name='index'),
    url(r'^vlive/register/$', views.register, name='register'),
    url(r'^vlive/', include('ummeli.vlive.urls')),
    url(
        r'^vlivebanner/banner/$',
        TemplateView.as_view(template_name="banner_banner.html")),
    url(
        r'^vlivebanner/thumbnail/$',
        TemplateView.as_view(template_name="banner_thumbnail.html")),
)
