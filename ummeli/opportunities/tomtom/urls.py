from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from ummeli.opportunities.models import MicroTask
from ummeli.opportunities.views import OpportunityDetailView


urlpatterns = patterns('',
    url(r'^device/instructions/$',
        'ummeli.opportunities.tomtom.views.device_instructions',
        name='device_instructions'),
    url(r'^device/change/$',
        'ummeli.opportunities.tomtom.views.qualify_device_change',
        name='qualify_device_change'),
    url(r'^microtasks/(?P<slug>[\w-]+)/instructions/$',
        'ummeli.opportunities.tomtom.views.task_instructions',
        name='micro_task_instructions'),
    url(r'^microtasks/(?P<slug>[\w-]+)/conditions/$',
        login_required(OpportunityDetailView.as_view(
            template_name='opportunities/tomtom/microtask_conditions.html',
            model=MicroTask)),
        name='micro_task_conditions'),
    url(r'^(?P<slug>[\w-]+)/qualify/$',
        'ummeli.opportunities.tomtom.views.qualify',
        name='campaign_qualify'),
    url(r'^(?P<slug>[\w-]+)/qualify/upload/$',
        'ummeli.opportunities.tomtom.views.qualify_upload',
        name='qualify_upload'),
    url(r'^(?P<slug>[\w-]+)/qualify/device/$',
        'ummeli.opportunities.tomtom.views.qualify_device',
        name='qualify_device'),
    url(r'^microtasks/(?P<slug>[\w-]+)/upload/$',
        'ummeli.opportunities.tomtom.views.task_upload',
        name='micro_task_upload'),
    url(r'^microtasks/(?P<slug>[\w-]+)/moved/$',
        'ummeli.opportunities.tomtom.views.task_upload',
        {'template_name': 'opportunities/tomtom/microtask_moved.html'},
        name='micro_task_moved'),
    url(r'^upload/test/$',
        'ummeli.opportunities.tomtom.views.upload_test',
        name='upload_test'),
    )
