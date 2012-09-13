from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from ummeli.providers import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sentry/', include('sentry.web.urls')),
    url(r'^health/$', views.health, name="health"),
    url(r'^geckoboard/', include('jmbodashboard.geckoboard.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'admin/login.html'},
        name="login"),
    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name="logout"),
    #url(r'^forgot/$', views.forgot_password_view, name='forgot'),

    url(r'^upload/$', views.upload, name='upload'),
    url(r'^upload/confirm/$', views.upload_confirm, name='upload_confirm'),
    url(r'^upload/process/$', views.process_upload, name='process_upload'),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT,}),
    )
