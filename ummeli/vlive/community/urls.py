from django.conf.urls.defaults import patterns, url
from ummeli.vlive.community import views
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
    url(r'^jobs/$', views.community_jobs, name='community_jobs'),
    url(r'^jobs/(?P<id>\d+)/$', views.community_job, name='community_jobs'),
    url(r'^status/$', login_required(views.StatusUpdateView.as_view()), name='status_update'),
)
