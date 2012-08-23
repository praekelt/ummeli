from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^internship/$',
        'ummeli.opportunities.views.internships',
        name='internships'),
    url(r'^internship/(?P<slug>[\w-]+)/$',
        'ummeli.opportunities.views.internship_detail',
        name='internship_detail')
)
