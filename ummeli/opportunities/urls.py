from django.conf.urls.defaults import patterns, url, include
from django.contrib.auth.decorators import login_required
from ummeli.opportunities.models import *
from ummeli.opportunities.views import (OpportunityDetailView,\
    OpportunityListView, CampaignDetailView, MicroTaskListView,
    MyMicroTaskListView, MicroTaskDetailView, VliveMicroTaskListView)
from atlas.views import location_required


urlpatterns = patterns('',
    url(r'^$',
        'ummeli.opportunities.views.opportunities',
        name='opportunities'),
    url(r'^province/(?P<province>\d+)?/?$',
        'ummeli.opportunities.views.change_province',
        name='change_province'),
    url(r'^microtasks/province/(?P<province>\d+)?/?$',
        'ummeli.opportunities.views.microtask_change_province',
        name='microtask_change_province'),

    url(r'^internships/$',
        OpportunityListView.as_view(model=Internship, \
            template_name='opportunities/internships.html'),
        name='internships'),
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

    #vlive campaigns
    url(r'^vlive/campaigns/$',
        OpportunityListView.as_view(model=Campaign, \
            template_name='opportunities/vlive_campaigns.html'),
        name='vlive_campaigns'),
    url(r'^vlive/campaigns/(?P<campaign>[\w-]+)/$',
        VliveMicroTaskListView.as_view(
            template_name='opportunities/vlive_campaigns_tasks.html'),
        name='vlive_campaigns_tasks'),

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
    url(r'^campaigns/$',
        OpportunityListView.as_view(model=Campaign, \
            template_name='opportunities/campaigns.html'),
        name='campaigns'),
    url(r'^campaigns/(?P<slug>[\w-]+)/$',
        location_required(login_required(CampaignDetailView.as_view(model=Campaign,\
            template_name='opportunities/campaign_detail.html'))),
        name='campaign_detail'),
    url(r'^campaigns/(?P<campaign>[\w-]+)/tasks/$',\
        location_required(login_required(MicroTaskListView.as_view(
            template_name='opportunities/microtask_list.html'))),
        name='micro_tasks'),
    url(r'^campaigns/(?P<campaign>[\w-]+)/mytasks/$',\
        location_required(login_required(MyMicroTaskListView.as_view(
            template_name='opportunities/microtasks/my_microtask_list.html'))),
        name='my_micro_tasks'),
    url(r'^microtasks/(?P<slug>[\w-]+)/$',
        location_required(login_required(MicroTaskDetailView.as_view(model=MicroTask,\
            template_name='opportunities/microtasks/microtask_detail.html'))),
        name='micro_task_detail'),
    url(r'^microtasks/(?P<slug>[\w-]+)/checkout/$',
        'ummeli.opportunities.views.checkout',
        name='micro_task_checkout'),
    url(r'^tomtom/', include('ummeli.opportunities.tomtom.urls')),

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

    #Jobs from Ummeli 2.0
    url(r'^jobs/new/(?P<slug>[\w-]+)/$',
        OpportunityDetailView.as_view(model=Job,\
            template_name='opportunities/job_detail.html'),
        name='job_detail'),

    url(r'jobs/connection/apply/(?P<user_id>\d+)/jobs/(?P<pk>\d+)/$',
        'ummeli.vlive.views.connection_job',
        name='connection_job_apply'),

    url(r'^jobs/cron/$', 'ummeli.vlive.views.jobs_cron', name='jobs_cron'),
    url(r'^jobs/create/$', 'ummeli.vlive.views.jobs_create', name='jobs_create'),

)
