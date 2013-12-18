from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('reporting.views',
    url(r'^report/(?P<slug>[\w-]+)/(?P<report_key_field>[\w-]+)/$',
        'report',
        name='report_object'),
    )
