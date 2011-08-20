from django.conf.urls.defaults import patterns, url
from ummeli.api.handlers import UserHandler
from ummeli.vlive import views, cv_views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, {'template_name': 'vlive/login.html'}, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', {'login_url': '../login'}, name='logout'),
    url(r'^edit$', views.edit, name='edit'),
    url(r'^edit/personal$', cv_views.personal_details),
    url(r'^edit/contact$', cv_views.contact_details),
    url(r'^send$', views.send, name='send'),
    url(r'^jobs$', views.jobs, name='jobs'),
)
