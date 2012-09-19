from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.files.temp import NamedTemporaryFile
from django.http import HttpResponse, HttpResponseBadRequest

from ummeli.opportunities.models import MicroTask, TomTomMicroTask, Campaign
from ummeli.providers.forms import UploadTaskForm

from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from ummeli.base.models import PROVINCE_CHOICES

import os.path
import json
import csv
from datetime import date

from django.contrib.gis.geos import fromstr
from atlas.models import Location
from atlas.utils import get_city


def health(request):
    return HttpResponse("")


@staff_member_required
def index(request):
    context = {}
    return render(request, 'index.html', context)


@staff_member_required
def upload(request, campaign):
    if request.method == 'POST':
        form = UploadTaskForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            process_upload(file, campaign)
            return redirect(reverse('providers.campaign_detail',\
                                args=[campaign, ]))
    else:
        campaign_obj = get_object_or_404(Campaign,\
                        owner=request.user,
                        slug=campaign)
        form = UploadTaskForm()

    return render(request, 'upload.html',\
                {'form': form, 'campaign': campaign_obj})


def process_upload(csv_file, campaign_slug):
    #csv_file = open(file, 'rU')
    rows = read_data_from_csv_file(csv_file)
    campaign = Campaign.objects.get(slug=campaign_slug)

    for r in rows:
        try:
            t = TomTomMicroTask.objects.get(poi_id=r['POI_ID'])
        except TomTomMicroTask.DoesNotExist:
            t = TomTomMicroTask(poi_id=r['POI_ID'])
            loc = Location()
            # srid is the ID for the coordinate system, 4326 specifies longitude/latitude coordinates
            loc.coordinates = fromstr("POINT (%s %s)" % (r['X'], r['Y']), srid=4326)
            loc.city = get_city(position=loc.coordinates)
            loc.country = loc.city.country
            loc.save()

            t.title = r['NAME']
            t.description = '%s %s' % (r['NAME_ALT'], r['ADDRESS'])
            t.category = r['CAT_NAME']
            t.location = loc
            t.tel_1 = r['TEL_NR']
            t.tel_2 = r['TEL_NR2']
            t.fax = r['FAX_NR']
            t.email = r['E_MAIL']
            t.website = r['WEBSITE']
            t.owner = campaign.owner
            t.save()

            t.publish()

            campaign.tasks.add(t)


def read_data_from_csv_file(csvfile):
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Only process rows that actually have data
        if any([column for column in row]):
            yield row


class OpportunityDetailView(DetailView):
    def get_object(self):
        return get_object_or_404(self.model,\
                    owner=self.request.user,\
                    slug=self.kwargs['slug'])


class OpportunityListView(ListView):
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)\
                                    .order_by('-created')


class CampaignDetailView(OpportunityDetailView):
    def get_context_data(self, **kwargs):
        context = super(CampaignDetailView, self).get_context_data(**kwargs)
        context['published_count'] = self.get_object().tasks.filter(state='published').count()
        context['new_count'] = self.get_object()\
                                    .tasks\
                                    .filter(created__gte=date.today())\
                                    .count()
        return context


class MicroTaskDetailView(DetailView):
    def get_object(self):
        campaign = get_object_or_404(Campaign,\
                        owner=self.request.user,
                        slug=self.kwargs['campaign'])
        return get_object_or_404(self.model, campaign=campaign,\
                                    slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(MicroTaskDetailView, self).get_context_data(**kwargs)
        campaign = get_object_or_404(Campaign,\
                        owner=self.request.user,
                        slug=self.kwargs['campaign'])
        context['campaign'] = campaign
        return context


class MicroTaskListView(OpportunityListView):
    def get_queryset(self):
        campaign = get_object_or_404(MicroTask,\
                        owner=self.request.user,\
                        slug=self.kwargs['slug'])
        return campaign.tasks.order_by('-created')
