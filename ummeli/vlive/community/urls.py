from django.conf.urls.defaults import patterns, url
from ummeli.vlive.community import views


urlpatterns = patterns('',
    url(r'^jobs/$', views.community_jobs, name='community_jobs'),
    url(r'^jobs/(?P<id>\d+)/$', views.community_job, name='community_jobs'),
)
