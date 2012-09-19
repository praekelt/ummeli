from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from ummeli.providers import views
from ummeli.opportunities.models import Campaign, MicroTask
from ummeli.providers.views import *

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

    url(r'^campaigns/(?P<campaign>[\w-]+)/upload/$', views.upload, name='upload'),
    url(r'^campaigns/(?P<campaign>[\w-]+)/upload/process/$', views.process_upload, name='process_upload'),

    url(r'^campaigns/$',
        OpportunityListView.as_view(model=Campaign, \
            template_name='opportunities/campaigns.html'),
        name='providers.campaigns'),

    url(r'^campaigns/(?P<slug>[\w-]+)/$', views.campaign_view,
        name='providers.campaign_detail'),
    url(r'^campagins/(?P<campaign>[\w-]+)/task/(?P<slug>[\w-]+)/$',
        MicroTaskDetailView.as_view(model=MicroTask),\
        name='providers.micro_task_detail'),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT,}),
    )
