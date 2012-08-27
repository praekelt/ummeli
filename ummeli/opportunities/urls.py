from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^internship/$',
        'ummeli.opportunities.views.internships',
        name='internships'),
    url(r'^(?P<slug>[\w-]+)/$',
        'ummeli.opportunities.views.opportunity_detail',
        name='internship_detail')
)
