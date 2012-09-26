from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from ummeli.opportunities.models import *
from ummeli.opportunities.views import (OpportunityDetailView,\
    OpportunityListView, CampaignDetailView, MicroTaskListView)


urlpatterns = patterns('',
    url(r'^$',
        'ummeli.opportunities.views.opportunities',
        name='opportunities'),
    url(r'^province(?:/(?P<province>\d+))?/$',
        'ummeli.opportunities.views.change_province',
        name='change_province'),

    url(r'^internships/$',
        OpportunityListView.as_view(model=Internship, \
            template_name='opportunities/internships.html'),
        name='internships'),
    #url(r'^jobs/$',
    #    OpportunityListView.as_view(model=Job, \
    #        template_name='opportunities/jobs/jobs.html'),
    #    name='job_opportunities'),
    url(r'^bursaries/$',
        OpportunityListView.as_view(model=Bursary, \
            template_name='opportunities/bursaries.html'),
        name='bursaries'),
    url(r'^volunteering/$',
        OpportunityListView.as_view(model=Volunteer, \
            template_name='opportunities/volunteering.html'),
        name='volunteering'),
    url(r'^training/$',
        OpportunityListView.as_view(model=Training, \
            template_name='opportunities/training.html'),
        name='training'),
    url(r'^competitions/$',
        OpportunityListView.as_view(model=Competition, \
            template_name='opportunities/competitions.html'),
        name='competitions'),
    url(r'^events/$',
        OpportunityListView.as_view(model=Event, \
            template_name='opportunities/events.html'),
        name='events'),
    url(r'^campaigns/$',
        OpportunityListView.as_view(model=Campaign, \
            template_name='opportunities/campaigns.html'),
        name='campaigns'),
    url(r'^campaigns/(?P<campaign>[\w-]+)/tasks/$',\
        login_required(MicroTaskListView.as_view()),
        name='micro_tasks'),

    #url(r'^jobs/(?P<slug>[\w-]+)/$',
    #    OpportunityDetailView.as_view(model=Job,\
    #        template_name='opportunities/job_detail'),
    #    name='job_opportunity'),
    url(r'^internships/(?P<slug>[\w-]+)/$',
        OpportunityDetailView.as_view(model=Internship,\
            template_name='opportunities/internship_detail.html'),
        name='internship_detail'),
    url(r'^bursaries/(?P<slug>[\w-]+)/$',
        OpportunityDetailView.as_view(model=Bursary,\
            template_name='opportunities/bursary_detail.html'),
        name='bursary_detail'),
    url(r'^volunteering/(?P<slug>[\w-]+)/$',
        OpportunityDetailView.as_view(model=Volunteer,\
            template_name='opportunities/volunteer_detail.html'),
        name='volunteer_detail'),
    url(r'^training/(?P<slug>[\w-]+)/$',
        OpportunityDetailView.as_view(model=Training,\
            template_name='opportunities/training_detail.html'),
        name='training_detail'),
    url(r'^competitions/(?P<slug>[\w-]+)/$',
        OpportunityDetailView.as_view(model=Competition,\
            template_name='opportunities/competition_detail.html'),
        name='competition_detail'),
    url(r'^events/(?P<slug>[\w-]+)/$',
        OpportunityDetailView.as_view(model=Event,\
            template_name='opportunities/event_detail.html'),
        name='event_detail'),
    url(r'^campaigns/(?P<slug>[\w-]+)/$',
        login_required(CampaignDetailView.as_view(model=Campaign,\
            template_name='opportunities/campaign_detail.html')),
        name='campaign_detail'),
    url(r'^campagins/(?P<campaign>[\w-]+)/(?P<slug>[\w-]+)/$',
        OpportunityDetailView.as_view(model=MicroTask,\
            template_name='opportunities/microtask_detail.html'),
        name='micro_task_detail'),
    url(r'^campagins/task/tomtom/(?P<slug>[\w-]+)/$',
        OpportunityDetailView.as_view(model=MicroTask,\
            template_name='opportunities/tom_tom_micro_task_detail.html'),
        name='tom_tom_micro_task_detail'),

    url(r'^campagins/(?P<slug>[\w-]+)/qualify/$',\
        'ummeli.opportunities.views.campaign_qualify',\
        name='campaign_qualify'),

    #Jobs from Ummeli 1.0
    url(r'^jobs/$',
        'ummeli.vlive.views.jobs_list',
        name='jobs_list'),
    url(r'^jobs/(?P<id>\d+)/$',
        'ummeli.vlive.views.jobs',
        name='jobs'),
    url(r'^jobs/(?P<cat_id>\d+)/(?P<id>\d+)/$',
        'ummeli.vlive.views.job',
        name='job'),
    url(r'^jobs/(?P<cat_id>\d+)/(?P<id>\d+)/(?P<user_submitted>\d+)/$',
        'ummeli.vlive.views.job',
        name='job'),

    url(r'jobs/connection/apply/(?P<user_id>\d+)/jobs/(?P<pk>\d+)/$',
        'ummeli.vlive.views.connection_job',
        name='connection_job_apply'),

    url(r'^jobs/cron/$', 'ummeli.vlive.views.jobs_cron', name='jobs_cron'),
    url(r'^jobs/create/$', 'ummeli.vlive.views.jobs_create', name='jobs_create'),

)
