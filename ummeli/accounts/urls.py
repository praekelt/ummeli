from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('accounts.views',
    url(r'^profile/$', 'profile_detail', name='accounts_profile'),
    url(r'^profile/(?P<pk>\d+)/$', 'profile_detail', name='accounts_profile'),
)