from django.conf.urls.defaults import patterns, url, include
from ummeli.vlive.forms import SkillWizardForm, SkillWizardFormPick
from ummeli.vlive.profile import views
from ummeli.vlive.utils import pin_required
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', views.profile, name='profile'),
    url(r'^(?P<user_id>\d+)/$', views.profile_view, name='profile_view'),
    url(r'^connections/(?P<user_id>\d+)/$', views.connections, name='connections'),
    url(r'^connections/add/(?P<user_id>\d+)/$', views.add_connection, name='add_connection'),
    url(r'^connections/requests/$', views.connection_requests, name='connection_requests'),
    url(r'^connections/confirm/(?P<user_id>\d+)/$', views.confirm_request, name='confirm_request'),
    url(r'^connections/reject/(?P<user_id>\d+)/$', views.reject_request, name='reject_request'),

    url(r'^basic/$', views.edit_basic, name='edit_basic'),
    url(r'^basic/personal/$', 
        pin_required(login_required(views.PersonalDetailsEditView.as_view())), 
        name='edit_personal'),
    url(r'^basic/contact/$', views.contact_details, name='edit_contact'),
    url(r'^basic/education/$', views.education_details, name='edit_education'),

    url(r'certificates/$',
        views.CertificateListView.as_view(),
        name='certificate_list'),
    url(r'certificates/(?P<pk>\d+)/$',
        pin_required(login_required(views.CertificateEditView.as_view())),
        name='certificate_edit'),
    url(r'certificates/new/$',
        pin_required(views.CertificateCreateView.as_view()),
        name='certificate_new'),
    url(r'certificates/delete/(?P<pk>\d+)/$',
        pin_required(views.CertificateDeleteView.as_view()),
        name='certificate_delete'),

    url(r'work_experiences/$',
        pin_required(views.WorkExperienceListView.as_view()),
        name='work_experience_list'),
    url(r'work_experiences/(?P<pk>\d+)/$',
        pin_required(views.WorkExperienceEditView.as_view()),
        name='workExperience_edit'),
    url(r'work_experiences/new/$',
        pin_required(views.WorkExperienceCreateView.as_view()),
        name='workExperience_new'),
    url(r'work_experiences/delete/(?P<pk>\d+)/$',
        pin_required(views.WorkExperienceDeleteView.as_view()),
        name='workExperience_delete'),

    url(r'languages/$',
        pin_required(views.LanguageListView.as_view()),
        name='language_list'),
    url(r'languages/(?P<pk>\d+)/$',
        pin_required(views.LanguageEditView.as_view()),
        name='language_edit'),
    url(r'languages/new/$',
        pin_required(views.LanguageCreateView.as_view()),
        name='language_new'),
    url(r'languages/delete/(?P<pk>\d+)/$',
        pin_required(views.LanguageDeleteView.as_view()),
        name='language_delete'),

    url(r'references/$',
        pin_required(views.ReferenceListView.as_view()),
        name='reference_list'),
    url(r'references/(?P<pk>\d+)/$',
        pin_required(views.ReferenceEditView.as_view()),
        name='reference_edit'),
    url(r'references/new/$',
        pin_required(views.ReferenceCreateView.as_view()),
        name='reference_new'),
    url(r'references/delete/(?P<pk>\d+)/$',
        pin_required(views.ReferenceDeleteView.as_view()),
        name='reference_delete'),
    
    url(r'skills/$',
        pin_required(views.SkillListView.as_view()),
        name='skills'),
    url(r'skills/new/$',
        #pin_required(
                     views.SkillsWizard([SkillWizardForm, SkillWizardFormPick], 
        #condition_dict={'1': views.get_skill_from_first_step})
        ),
        name='skills_new'),
    url(r'skills/delete/(?P<pk>\d+)/$',
        pin_required(views.SkillDeleteView.as_view()),
        name='skills_delete'),
)
