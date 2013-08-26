from django.conf.urls.defaults import patterns, url
from ummeli.vlive.community import views
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView


urlpatterns = patterns('',
    url(r'^jobs/$', views.community_jobs, name='community_jobs'),
    url(r'^jobs/(?P<slug>[\w-]+)/$', views.community_job, name='community_jobs'),
    url(r'^status/$', login_required(views.StatusUpdateView.as_view()), name='status_update'),
    url(r'^skills/$', login_required(TemplateView.as_view(template_name='profile/community/advertise_skills.html')), name='advertise_skills'),
    url(r'^skills/post/$', views.advertise_skills_post, name='advertise_skills_post'),
)
