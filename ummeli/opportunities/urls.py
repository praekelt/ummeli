from django.conf.urls.defaults import patterns, url
from ummeli.opportunities.models import *
from ummeli.opportunities.views import OpportunityDetailView, OpportunityListView


urlpatterns = patterns('',
    url(r'^internships/$',
        OpportunityListView.as_view(model=Internship, \
            template_name='opportunities/internships.html'),
        name='internships'),
    url(r'^jobs/$',
        OpportunityListView.as_view(model=Job, \
            template_name='opportunities/jobs.html'),
        name='job_opportunities'),
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

    url(r'^jobs/(?P<slug>[\w-]+)/$',
        OpportunityDetailView.as_view(model=Job,\
            template_name='opportunities/job_detail'),
        name='job_opportunity'),
    url(r'^internships/(?P<slug>[\w-]+)/$',
        OpportunityDetailView.as_view(model=Internship,\
            template_name='opportunities/internship_detail.html'),
        name='internship_detail'),
    url(r'^bursaries/(?P<slug>[\w-]+)/$',
        OpportunityDetailView.as_view(model=Bursary,\
            template_name='opportunities/bursary_detail'),
        name='bursary_detail'),
    url(r'^volunteering/(?P<slug>[\w-]+)/$',
        OpportunityDetailView.as_view(model=Volunteer,\
            template_name='opportunities/volunteer_detail'),
        name='volunteer_detail'),
    url(r'^training/(?P<slug>[\w-]+)/$',
        OpportunityDetailView.as_view(model=Training,\
            template_name='opportunities/training_detail'),
        name='training_detail'),
    url(r'^competitions/(?P<slug>[\w-]+)/$',
        OpportunityDetailView.as_view(model=Competition,\
            template_name='opportunities/competition_detail'),
        name='competition_detail'),
    url(r'^events/(?P<slug>[\w-]+)/$',
        OpportunityDetailView.as_view(model=Event,\
            template_name='opportunities/event_detail'),
        name='event_detail'),
)
