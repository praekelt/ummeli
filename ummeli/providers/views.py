from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.files.temp import NamedTemporaryFile
from django.http import HttpResponse, HttpResponseBadRequest

from ummeli.opportunities.models import MicroTask, Campaign
from ummeli.providers.forms import UploadTaskForm

from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from ummeli.base.models import PROVINCE_CHOICES

import os.path
import json
import csv


def health(request):
    return HttpResponse("")


@staff_member_required
def index(request):
    context = {}
    return render(request, 'index.html', context)


@staff_member_required
def upload(request):
    if request.method == 'POST':
        form = UploadTaskForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            handle_uploaded_file(request, file)
            return redirect(reverse('upload_confirm'))
    else:
        form = UploadTaskForm()

    return render(request, 'upload.html', {'form': form})


@staff_member_required
def upload_confirm(request):
    if request.method == 'POST':
        new_tasks = request.POST.getlist('new_task')
        if new_tasks:
            # publish selected tasks
            TomTomMicroTask.objects.filter(id__in=new_tasks).update(published=True)
            return redirect(reverse('index'))
    else:
        # check if file exists
        if request.session.get('uploaded_csv_path', None):
            if not os.path.exists(request.session['uploaded_csv_path']):
                del request.session['uploaded_csv_path']
                return redirect(reverse('upload'))
        else:
            return redirect(reverse('upload'))

    return render(request, 'upload_confirm.html')


@staff_member_required
def process_upload(request):
    uploaded_csv_path = request.session.get('uploaded_csv_path')

    if not uploaded_csv_path:
        return HttpResponseBadRequest()

    csv_file = open(uploaded_csv_path, 'rU')
    rows = prepare_csv_data(request, read_data_from_csv_file(csv_file))

    data = json.dumps(rows)
    return HttpResponse(data, mimetype='application/json')


def prepare_csv_data(request, rows):
    new_tasks = []
    duplicate_tasks = []

    for r in rows:
        t, created = TomTomMicroTask.objects.get_or_create(poi_id=r['POI_ID'],
                                                    x_coordinate=r['X'],
                                                    y_coordinate=r['Y'],
                                                    title=r['NAME'])
        if created:
            t.description = '%s %s' % (r['NAME_ALT'], r['ADDRESS'])
            t.category = r['CAT_NAME']
            #t.province = r['PROVINCE']
            #t.city = r['CITY']
            #t.suburb = r['SUBURB']
            t.tel_1 = r['TEL_NR']
            t.tel_2 = r['TEL_NR2']
            t.fax = r['FAX_NR']
            t.email = r['E_MAIL']
            t.website = r['WEBSITE']
            t.save()

            new_tasks.append(t.to_dto())
        else:
            duplicate_tasks.append(t.to_dto())

    # clean session and temp file
    os.remove(request.session['uploaded_csv_path'])
    del request.session['uploaded_csv_path']

    return {'new_tasks': new_tasks, 'duplicate_tasks': duplicate_tasks}


def read_data_from_csv_file(csvfile):
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Only process rows that actually have data
        if any([column for column in row]):
            yield row


def handle_uploaded_file(request, f):
    newfile = NamedTemporaryFile(suffix='.csv', delete=False)
    newfile.write(f.read())
    newfile.flush()

    request.session['uploaded_csv_path'] = newfile.name


class OpportunityDetailView(DetailView):
    def get_object(self):
        return get_object_or_404(self.model, slug=self.kwargs['slug'])


class OpportunityListView(ListView):
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(state='published').order_by('-created')


class MicroTaskDetailView(DetailView):
    def get_object(self):
        campaign = get_object_or_404(Campaign, slug=self.kwargs['campaign'])
        return get_object_or_404(self.model, campaign=campaign,\
                                    slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(MicroTaskDetailView, self).get_context_data(**kwargs)
        campaign = get_object_or_404(Campaign, slug=self.kwargs['campaign'])
        context['campaign'] = campaign
        return context


class MicroTaskListView(ListView):
    paginate_by = 10

    def get_queryset(self):
        campaign = get_object_or_404(MicroTask, slug=self.kwargs['slug'])
        return campaign.tasks.filter(state='published').order_by('-created')
