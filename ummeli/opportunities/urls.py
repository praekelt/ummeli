from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^internship/$',
        'ummeli.opportunities.views.internships',
        name='internships'),

    url(r'^job/(?P<slug>[\w-]+)/$',
        'ummeli.opportunities.views.job_detail',
        name='job_detail'),

    url(r'^internship/(?P<slug>[\w-]+)/$',
        'ummeli.opportunities.views.internship_detail',
        name='internship_detail'),

    url(r'^bursary/(?P<slug>[\w-]+)/$',
        'ummeli.opportunities.views.bursary_detail',
        name='bursary_detail'),

    url(r'^volunteer/(?P<slug>[\w-]+)/$',
        'ummeli.opportunities.views.volunteer_detail',
        name='volunteer_detail'),

    url(r'^training/(?P<slug>[\w-]+)/$',
        'ummeli.opportunities.views.training_detail',
        name='training_detail'),

    url(r'^competition/(?P<slug>[\w-]+)/$',
        'ummeli.opportunities.views.competition_detail',
        name='competition_detail'),

    url(r'^event/(?P<slug>[\w-]+)/$',
        'ummeli.opportunities.views.event_detail',
        name='event_detail'),
)
