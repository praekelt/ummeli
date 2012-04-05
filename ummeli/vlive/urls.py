from django.conf.urls.defaults import patterns, url, include
from ummeli.vlive import views
from ummeli.vlive.utils import pin_required
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings

urlpatterns = patterns('',
    #url(r'^$', views.login, {'template_name': 'pml/login.xml'},  name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.index, name='home'),
    url(r'^my/$', views.my_ummeli, name='my_ummeli'),

    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout_view, name = 'logout'),
    url(r'^forgot/$', views.forgot_password_view, name = 'forgot'),
    url(r'^password_change/$', views.password_change_view, name = 'password_change'),
    url(r'^about/$', views.about, name = 'about'),
    url(r'^terms/$', views.terms, name = 'terms'),
    url(r'^contactsupport/$', views.contact_support, name = 'contactsupport'),
    
    #Ummeli 2.0
    url(r'^article/', include('jmboarticles.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^ummeli/comments/', include('jmbocomments.urls')),
    url(r'^poll/', include('jmboarticles.poll.urls')),
    url(r'^profile/', include('ummeli.vlive.profile.urls')),

    url(r'^send/$', views.send, name='send'),
    url(r'^send/thanks/$', views.send_thanks, name='send_thanks'),

    url(r'^jobs/$', views.jobs_province, name='jobs_province'),
    url(r'^jobs/(?P<id>-\d+|\d+)/$', views.jobs_list, name='jobs_list'),
    url(r'^jobs/(?P<search_id>-\d+|\d+)/(?P<id>\d+)/$', views.jobs, name='jobs'),
    url(r'^jobs/(?P<search_id>-\d+|\d+)/(?P<cat_id>\d+)/(?P<id>\d+)/$', views.job, name='job'),
    url(r'^jobs/(?P<search_id>-\d+|\d+)/(?P<cat_id>\d+)/(?P<id>\d+)/(?P<user_submitted>\d+)/$', views.job, name='job'),

    url(r'^jobs/cron/$', views.jobs_cron, name='jobs_cron'),
    url(r'^jobs/create/$', views.jobs_create, name='jobs_create'),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
    )