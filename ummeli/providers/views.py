from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.sites.models import Site
from django.contrib import messages

from ummeli.opportunities.models import (MicroTask, TomTomMicroTask, Campaign,
                                        MicroTaskResponse, Province)
from ummeli.providers.forms import UploadTaskForm, TaskResponseForm

from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import csv

from django.contrib.gis.geos import fromstr
from atlas.models import Location
from atlas.utils import get_city


def health(request):
    return HttpResponse("")


@staff_member_required
def index(request):
    campaign = request.user.campaign_set.all()[0]
    paginator = Paginator(campaign.tasks.all(), 25)

    page = request.GET.get('page', 1)
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    context = {
        'object': campaign,
        'tasks': tasks,
    }
    return render(request, 'opportunities/campaign_detail.html', context)


@staff_member_required
def campaign_view(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug, owner=request.user)

    paginator = Paginator(campaign.tasks.all(), 25)

    page = request.GET.get('page', 1)
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    context = {
        'object': campaign,
        'tasks': tasks,
    }
    return render(request, 'opportunities/campaign_detail.html', context)


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


@staff_member_required
def micro_task_detail(request, campaign, slug):
    campaign = get_object_or_404(Campaign,\
                        owner=request.user,
                        slug=campaign)
    task = get_object_or_404(MicroTask, campaign=campaign, slug=slug)

    if request.method == 'POST':
        form = TaskResponseForm(request.POST, request.FILES)
        if form.is_valid():
            accept = form.cleaned_data['accept']
            username = form.cleaned_data['username']
            response_id = form.cleaned_data['response_id']
            response = get_object_or_404(MicroTaskResponse, pk=response_id)
            if accept:
                msg = '%s`s submission for `%s` has been accepted.' % (
                    username, task.title)
                messages.add_message(request, messages.SUCCESS, msg)
                response.state = 1
                response.save()
            else:
                msg = '%s`s submission has been rejected. `%s` is now live on Ummeli again.' % (
                    username, task.title)
                messages.add_message(request, messages.ERROR, msg)

                response.state = 2
                response.save()
            return redirect(reverse('index'))
        else:
            print form
    else:
        form = TaskResponseForm()

    return render(request, 'opportunities/microtask_detail.html',\
                {'form': form, 'campaign': campaign, 'object': task})


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

            t.website = r['CITY']
            t.website = r['SUBURB']
            t.province = Province.from_str(r['PROVINCE'])
            t.owner = campaign.owner
            t.save()

            t.sites.add(Site.objects.get_current())

            t.publish()

        if t:
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


class MicroTaskListView(OpportunityListView):
    def get_queryset(self):
        campaign = get_object_or_404(MicroTask,\
                        owner=self.request.user,\
                        slug=self.kwargs['slug'])
        return campaign.tasks.order_by('-created')


class TaskResponseListView(ListView):
    paginate_by = 10
    template_name = 'opportunities/responses.html'

    def get_queryset(self):
        campaign = get_object_or_404(Campaign,\
                        owner=self.request.user,
                        slug=self.kwargs['campaign'])
        return MicroTaskResponse.objects.filter(task__campaign=campaign,
                                                state=0)\
                                        .order_by('date')

    def get_context_data(self, **kwargs):
        context = super(TaskResponseListView, self).get_context_data(**kwargs)
        campaign = get_object_or_404(Campaign,\
                        owner=self.request.user,
                        slug=self.kwargs['campaign'])
        context['campaign'] = campaign
        return context
