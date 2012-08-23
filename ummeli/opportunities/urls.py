from django.conf.urls.defaults import patterns, url
from ummeli.opportunities.views import *


urlpatterns = patterns('',
    url(r'internship/$', internship_detail, name='internships'),
    url(r'internship/^(?P<slug>[\w-]+)/$',
        internship_detail,
        name='internship_detail'),
)
