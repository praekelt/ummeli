from django.conf.urls.defaults import patterns, url
from ummeli.api.handlers import UserHandler
from ummeli.vlive import views, cv_views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, {'template_name': 'vlive/login.html'}, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', {'login_url': '../login'}, name='logout'),
    url(r'^edit$', views.edit, name='edit'),
    url(r'^edit/personal$', cv_views.personal_details),
    url(r'^edit/contact$', cv_views.contact_details),
    url(r'^edit/education$', cv_views.education_details),
    
    url(r'^edit/certificates/$', 
        login_required(cv_views.CertificateListView.as_view()),  
        name='certificate_list'),
    url(r'^edit/certificates/(?P<pk>\d+)/$', 
        login_required(cv_views.CertificateEditView.as_view()),  
        name='certificate_edit'),
    url(r'^edit/certificates/new/$', 
        login_required(cv_views.CertificateCreateView.as_view()), 
        name='certificate_new'),
    url(r'^edit/certificates/delete/(?P<pk>\d+)/$', 
        login_required(cv_views.CertificateDeleteView.as_view()),  
        name='certificate_delete'),
    
    url(r'^edit/workExperiences$', cv_views.workExperiences_details),
    url(r'^edit/workExperiences/(?P<pk_id>\d+)$', cv_views.workExperience_details),
    url(r'^edit/workExperiences/add$', cv_views.workExperience_details),
    url(r'^edit/languages$', cv_views.languages_details),
    url(r'^edit/languages/(?P<pk_id>\d+)$', cv_views.language_details),
    url(r'^edit/languages/add$', cv_views.language_details),
    url(r'^edit/references$', cv_views.references_details),
    url(r'^edit/references/(?P<pk_id>\d+)$', cv_views.reference_details),
    url(r'^edit/references/add$', cv_views.reference_details),
    url(r'^send$', views.send, name='send'),
    url(r'^send/email$', views.send_via_email),
    url(r'^send/fax$', views.send_via_fax),
    url(r'^send/thanks$', views.send_thanks),
    url(r'^jobs$', views.jobs, name='jobs'),
)
