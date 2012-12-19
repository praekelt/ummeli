from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from ummeli.base.models import PROVINCE_CHOICES
from ummeli.opportunities.models import *
from ummeli.providers.forms import UploadTaskForm
from ummeli.vlive.utils import get_lat_lon

from django.contrib.gis.geos import Point


class OpportunityDetailView(DetailView):
    def get_object(self):
        return get_object_or_404(self.model, slug=self.kwargs['slug'])


class CampaignDetailView(OpportunityDetailView):
    def get_context_data(self, **kwargs):
        context = super(CampaignDetailView, self).get_context_data(**kwargs)
        context['has_qualified'] = self.get_object()\
                                        .has_qualified(self.request.user)
        return context


class OpportunityListView(ListView):
    paginate_by = 10

    def get_queryset(self):
        province = int(RequestContext(self.request)['province_id'])
        province_qs = self.model.objects.filter(state='published')

        if province > 0:
            province_qs = province_qs.filter(province__province__in=[province, 0])

        return province_qs.order_by('-created')


class MicroTaskListView(ListView):
    paginate_by = 10

    def get_queryset(self):
        campaign = get_object_or_404(Campaign, slug=self.kwargs['campaign'])

        if not campaign.has_qualified(self.request.user):
            return MicroTask.objects.none()

        position = self.request.session['location']['position']

        if not isinstance(position, Point):
            position = self.request.session['location']['city'].coordinates
        tasks = MicroTask.permitted.filter(campaign__pk=campaign.pk)
        return tasks.distance(position).order_by('distance')

    def get_context_data(self, **kwargs):
        context = super(MicroTaskListView, self).get_context_data(**kwargs)
        campaign = get_object_or_404(Campaign, slug=self.kwargs['campaign'])
        context['campaign'] = campaign
        return context


def opportunities(request):
    context = {
        'campaigns': Campaign.permitted.exists(),
        'bursaries': Bursary.permitted.exists(),
        'internships': Internship.permitted.exists(),
        'volunteering': Volunteer.permitted.exists(),
        'training': Training.permitted.exists(),
        'competitions': Competition.permitted.exists(),
        'events': Event.permitted.exists(),
    }
    return render(request, 'opportunities/opportunities.html', context)


def change_province(request, province=None):
    next = request.GET.get('next', reverse('opportunities'))

    if province and int(province) in range(0, 10):
        request.session['province'] = int(province)
        print request.session['province']
        return redirect(next)

    return render(request, 'opportunities/change_province.html',
                {'provinces': PROVINCE_CHOICES,
                'next': next})


@login_required
def campaign_qualify(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    context = {
        'object': campaign,
    }

    if request.method == 'POST':
        form = UploadTaskForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            lat, lon = get_lat_lon(file)
            if lat and lon:
                campaign.qualifiers.add(request.user)
                return redirect(reverse('campaign_detail', args=[slug, ]))
            else:
                context['error'] = True
    else:
        form = UploadTaskForm()

    return render(request, 'opportunities/campaign_qualify.html', context)
