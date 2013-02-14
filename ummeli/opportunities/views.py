from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ummeli.base.models import PROVINCE_CHOICES
from ummeli.opportunities.models import *
from ummeli.providers.forms import UploadTaskForm
from ummeli.opportunities.forms import TomTomMicroTaskResponseForm
from ummeli.vlive.utils import get_lat_lon
from django.contrib.gis.geos import Point


class OpportunityDetailView(DetailView):
    def get_object(self):
        return get_object_or_404(self.model, slug=self.kwargs['slug'])


class MicroTaskDetailView(OpportunityDetailView):
    def get_context_data(self, **kwargs):
        context = super(MicroTaskDetailView, self).get_context_data(**kwargs)
        context['city'] = self.request.session['location']['city']
        return context


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

        if self.request.session.get('override_location'):
            tasks = MicroTask.permitted.filter(campaign__pk=campaign.pk)\
                                        .order_by('province', 'location__city')
            province = self.request.session['province']
            if province > 0:
                tasks = tasks.filter(province=province)
            return [task for task in tasks if task.available()]

        if not isinstance(position, Point):
            position = self.request.session['location']['city'].coordinates
        tasks = MicroTask.permitted.filter(campaign__pk=campaign.pk)\
                                .distance(position).order_by('distance')
        return [task for task in tasks if task.available()]

    def get_context_data(self, **kwargs):
        context = super(MicroTaskListView, self).get_context_data(**kwargs)
        campaign = get_object_or_404(Campaign, slug=self.kwargs['campaign'])
        context['campaign'] = campaign
        context['city'] = self.request.session['location']['city']
        return context


class MyMicroTaskListView(MicroTaskListView):
    def get_queryset(self):
        campaign = get_object_or_404(Campaign, slug=self.kwargs['campaign'])

        if not campaign.has_qualified(self.request.user):
            return MicroTask.objects.none()

        return campaign.tasks.filter(taskcheckout__user=self.request.user,
                                taskcheckout__state=OPEN)\
                            .order_by('-taskcheckout__date')


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
        request.session['override_location'] = True
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


@login_required
def checkout(request, slug):
    task = get_object_or_404(MicroTask, slug=slug)
    if task.checkout(request.user):
        msg = 'You have booked this task. You have %shrs to finish the task.'
        messages.success(request, msg % task.hours_per_task)
        return redirect(reverse('micro_task_instructions', args=[slug, ]))
    messages.error(request, 'That task is no longer available for you.')
    return redirect(reverse('campaigns', args=[slug, ]))


@login_required
def task_upload(request, slug):
    task = get_object_or_404(MicroTask, slug=slug)

    if not task.checked_out_by(request.user):
        messages.error(request, 'That task is no longer available.')
        return redirect(reverse('campaigns'))

    task_checkout = get_object_or_404(TaskCheckout, task=task,
                                        state__lte=RETURNED)
    if request.method == 'POST':
        if task_checkout.microtaskresponse:
            form = TomTomMicroTaskResponseForm(request.POST, request.FILES,
                    instance=task_checkout.microtaskresponse.tomtommicrotaskresponse)
        else:
            form = TomTomMicroTaskResponseForm(request.POST, request.FILES)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.task = task
            response.task_checkout = task_checkout
            response.state = SUBMITTED
            response.save()

            task_checkout.state = RETURNED
            task_checkout.save()

            messages.success(request, 'Thank you! Your task has been sent.')
            return redirect(reverse('campaigns'))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        if hasattr(task_checkout, 'microtaskresponse'):
            form = TomTomMicroTaskResponseForm(instance=task_checkout.microtaskresponse.tomtommicrotaskresponse)
        else:
            form = TomTomMicroTaskResponseForm()

    return render(request, 'opportunities/microtasks/microtask_upload.html',
            {'object': task,
            'city': request.session['location']['city'],
            'form': form,
            })


@login_required
def task_instructions(request, slug):
    task = get_object_or_404(MicroTask, slug=slug)

    if not task.checked_out_by(request.user):
        messages.error(request, 'That task is not available for you.')
        return redirect(reverse('campaigns'))

    return render(request, 'opportunities/microtasks/microtask_instructions.html',
        {'object': task})
