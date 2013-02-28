from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from ummeli.vlive.inbox import views


urlpatterns = patterns('',
    url(r'^$', views.inbox, name='my_inbox'),
    url(r'^microtasks/$',
        login_required(views.MyTaskCheckoutListView.as_view()),
        name='my_microtasks'),
    )
