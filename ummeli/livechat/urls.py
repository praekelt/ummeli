from django.conf.urls.defaults import patterns, url
from ummeli.livechat import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>\d+)/$', views.show, name='show'),
)
