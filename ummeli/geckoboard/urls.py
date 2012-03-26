from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('geckoboard.views',
    url(r'^total-users-joined/$', 'total_users_joined', name='total_users_joined'),
    url(r'^total-comments/$', 'total_comments', name='total_comments'),
)