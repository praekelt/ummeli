from django.conf.urls.defaults import patterns, url, include
from ummeli.vlive import views
from ummeli.vlive.utils import pin_required
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings

urlpatterns = patterns('',
    #url(r'^$', views.login, {'template_name': 'pml/login.xml'},  name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.index, name='home'),
    url(r'^my/$', views.my_ummeli, name='my_ummeli'),
    url(r'^my/settings/$', views.my_settings, name='my_settings'),
    url(r'^my/settings/password_change/$', views.password_change_view, name = 'password_change'),
    url(r'^my/settings/contact_privacy/$',
        pin_required(login_required(views.MyContactPrivacyEditView.as_view())),
        name = 'my_contact_privacy'),
    url(r'^my/settings/comment_settings/$',
        pin_required(login_required(views.MyCommentSettingsEditView.as_view())),
        name = 'my_comment_settings'),

    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout_view, name = 'logout'),
    url(r'^forgot/$', views.forgot_password_view, name = 'forgot'),
    url(r'^tips/$', views.tips, name = 'tips'),
    url(r'^contactsupport/$', views.contact_support, name = 'contactsupport'),

    #Ummeli 2.0
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^article/', include('jmboarticles.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^ummeli/comments/', include('jmbocomments.urls')),
    url(r'^yourwords/', include('jmboyourwords.urls')),
    url(r'^poll/', include('jmboarticles.poll.urls')),
    url(r'^my/profile/', include('ummeli.vlive.profile.urls')),
    url(r'^downloads/', include('downloads.urls')),
    url(r'^opportunities/', include('ummeli.opportunities.urls')),

    url(r'^send/$', views.send, name='send'),
    url(r'^send/thanks/$', views.send_thanks, name='send_thanks'),

    url(r'^community/jobs/$', views.community_jobs, name='community_jobs'),
    url(r'^community/jobs/(?P<id>\d+)/$', views.community_job, name='community_jobs'),

    #Jmbo
    url(r'^jmbo/', include('jmbo.urls')),
    url(r'^simple-autocomplete/', include('simple_autocomplete.urls')),
    url(r'^', include('atlas.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
    )
