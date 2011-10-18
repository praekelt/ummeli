from django.conf.urls.defaults import patterns, url
from ummeli.api.handlers import UserHandler
from ummeli.vlive import views, cv_views
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

urlpatterns = patterns('',
    #url(r'^$', views.login, {'template_name': 'pml/login.xml'},  name='index'),
    #url(r'^$', views.index, name='index'),
    url(r'^home$', views.home, name='home'),
    
    url(r'^login$', views.login, name='login'),    
    url(r'^register$', views.register, name='register'),
    url(r'^logout$', views.logout_view, name = 'logout'),
    url(r'^forgot$', views.forgot_password_view, name = 'forgot'),
    url(r'^password_change$', views.password_change_view, name = 'password_change'),
    
    url(r'^edit$', views.edit, name='edit'),
    
    url(r'^edit/personal$', cv_views.personal_details, name='edit_personal'),
    url(r'^edit/contact$', cv_views.contact_details, name='edit_contact'),
    url(r'^edit/education$', cv_views.education_details, name='edit_education'),
    
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
        
    url(r'^edit/workExperiences/$', 
        login_required(cv_views.WorkExperienceListView.as_view()),  
        name='workExperience_list'),
    url(r'^edit/workExperiences/(?P<pk>\d+)/$', 
        login_required(cv_views.WorkExperienceEditView.as_view()),  
        name='workExperience_edit'),
    url(r'^edit/workExperiences/new/$', 
        login_required(cv_views.WorkExperienceCreateView.as_view()), 
        name='workExperience_new'),
    url(r'^edit/workExperiences/delete/(?P<pk>\d+)/$', 
        login_required(cv_views.WorkExperienceDeleteView.as_view()),  
        name='workExperience_delete'),
        
    url(r'^edit/languages/$', 
        login_required(cv_views.LanguageListView.as_view()),  
        name='language_list'),
    url(r'^edit/languages/(?P<pk>\d+)/$', 
        login_required(cv_views.LanguageEditView.as_view()),  
        name='language_edit'),
    url(r'^edit/languages/new/$', 
        login_required(cv_views.LanguageCreateView.as_view()), 
        name='language_new'),
    url(r'^edit/languages/delete/(?P<pk>\d+)/$', 
        login_required(cv_views.LanguageDeleteView.as_view()),  
        name='language_delete'),
        
    url(r'^edit/references/$', 
        login_required(cv_views.ReferenceListView.as_view()),  
        name='reference_list'),
    url(r'^edit/references/(?P<pk>\d+)/$', 
        login_required(cv_views.ReferenceEditView.as_view()),  
        name='reference_edit'),
    url(r'^edit/references/new/$', 
        login_required(cv_views.ReferenceCreateView.as_view()), 
        name='reference_new'),
    url(r'^edit/references/delete/(?P<pk>\d+)/$', 
        login_required(cv_views.ReferenceDeleteView.as_view()),  
        name='reference_delete'),
        
    url(r'^send$', views.send, name='send'),
    url(r'^send/email$', views.send_via_email, name='send_via_email'),
    url(r'^send/fax$', views.send_via_fax, name='send_via_fax'),
    url(r'^send/thanks$', views.send_thanks, name='send_thanks'),
    
    url(r'^jobs$', views.jobs_province, name='jobs_province'),
    url(r'^jobs/(?P<id>\d+)/$', views.jobs_list, name='jobs_list'),
    url(r'^jobs/(?P<search_id>\d+)/(?P<id>\w+)/$', views.jobs, name='jobs'),
    url(r'^jobs/(?P<search_id>\d+)/(?P<cat_id>\w+)/(?P<id>\w+)/$', views.job, name='job'),
    
    url(r'^jobs/cron$', views.jobs_cron, name='jobs_cron'),
)
