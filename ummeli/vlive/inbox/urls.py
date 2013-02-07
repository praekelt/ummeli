from django.conf.urls.defaults import patterns, url
from ummeli.vlive.inbox import views


urlpatterns = patterns('',
    url(r'^$', views.inbox, name='my_inbox'),
    url(r'^microtasks/$', views.MyTaskCheckoutListView.as_view(),
        name='my_microtasks'),
    )
