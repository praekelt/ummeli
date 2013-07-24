from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from ummeli.providers import views
from ummeli.providers.views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
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

    url(r'^campaigns/(?P<slug>[\w-]+)/$', views.campaign_view,
        name='providers.campaign_detail'),
    url(r'^campaigns/(?P<campaign>[\w-]+)/task/(?P<slug>[\w-]+)/$',
        views.micro_task_detail,
        name='providers.micro_task_detail'),
    url(r'^payment/(?P<campaign>[\w-]+)/task/(?P<slug>[\w-]+)/id/(?P<response_id>\d+)/$',
        views.submit_payment,
        name='providers.submit_payment'),
    url(r'^campaigns/(?P<campaign>[\w-]+)/submissions/$',
        TaskSubmissionsListView.as_view(),
        name='providers.task_submissions'),
    url(r'^campaigns/(?P<campaign>[\w-]+)/live/$',
        TaskLiveListView.as_view(),
        name='providers.task_live'),
    url(r'^campaigns/(?P<campaign>[\w-]+)/accepted/$',
        TaskAcceptedListView.as_view(),
        name='providers.task_accepted'),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT,}),
    )
