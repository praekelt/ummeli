from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ummeli.base.models import PROVINCE_CHOICES, ALL
from ummeli.opportunities.models import *
from ummeli.opportunities.tomtom.forms import SelectLocationForm
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

        if province != ALL:
            province_qs = province_qs.filter(province__province__in=[province,
                                                                    ALL])

        return province_qs.order_by('-publish_on')


class JobListView(OpportunityListView):
    template_name='opportunities/jobs/jobs.html'
    def get_queryset(self):
        qs = super(JobListView, self).get_queryset()

        if self.kwargs['category_id'] != 0:
            qs = qs.filter(category=self.kwargs['category_id'])

        return qs

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        context['category'] = dict(CATEGORY_CHOICES)[int(self.kwargs['category_id'])]
        return context


class MicroTaskListView(ListView):
    paginate_by = 10

    def get_queryset(self):
        campaign = get_object_or_404(Campaign, slug=self.kwargs['campaign'])

        if not campaign.has_qualified(self.request.user):
            return MicroTask.objects.none()

        location = self.request.session.get('location')

        if location and not self.request.session.get('override_location'):
            position = location.get('position')
            if not isinstance(position, Point):
                position = location('city').coordinates
            tasks = MicroTask.available.filter(campaign__pk=campaign.pk)\
                                    .distance(position).order_by('distance')
            return tasks

        tasks = MicroTask.available.filter(campaign__pk=campaign.pk)\
                                    .order_by('province', 'location__city')
        province = self.request.session.get('province', ALL)
        if province != ALL:
            tasks = tasks.filter(province=province)
        return tasks

    def get_context_data(self, **kwargs):
        context = super(MicroTaskListView, self).get_context_data(**kwargs)
        campaign = get_object_or_404(Campaign, slug=self.kwargs['campaign'])
        context['campaign'] = campaign
        return context


class VliveMicroTaskListView(ListView):
    paginate_by = 10

    def get_queryset(self):
        campaign = get_object_or_404(Campaign, slug=self.kwargs['campaign'])

        tasks = MicroTask.objects.filter(campaign__pk=campaign.pk)

        province = self.request.session.get('province', ALL)
        if province != ALL:
            tasks = tasks.filter(province=province)

        tasks = tasks.values('province', 'location__city__name')\
                    .annotate(num_tasks=Count('id'))\
                    .order_by('location__city__name')
        return tasks


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
        'campaign': Campaign.permitted.latest('created'),
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


def microtask_change_province(request, province=None):
    next = request.GET.get('next', reverse('opportunities'))

    if province and int(province) in range(0, 10):
        request.session['province'] = int(province)
        request.session['override_location'] = True
        return redirect(next)

    return render(request, 'opportunities/microtasks/change_province.html',
                {'provinces': PROVINCE_CHOICES,
                'next': next})


@login_required
def checkout(request, slug):
    task = get_object_or_404(MicroTask, slug=slug)
    if task.checkout(request.user):
        msg = 'You have booked this task. You have %shrs to finish the task.'
        messages.success(request, msg % task.hours_per_task)
        return redirect(reverse('micro_task_instructions', args=[slug, ]))
    messages.error(request, 'That task is no longer available for you.')
    return redirect(reverse('campaigns'))


@login_required
def select_location(request):
    c = Campaign.permitted.latest('created')
    next = request.GET.get('next', reverse('micro_tasks', args=[c.slug]))

    if request.method == 'POST':
        form = SelectLocationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['error'] is False:
                request.session['override_location'] = False
                return redirect(next)
            else:
                msg = 'We were unable to detect your location. %s'
                help = '<a href="%s?next=%s">Need Help? Click here</a>' % (
                        reverse('device_privacy'),
                        next)
                messages.error(request, msg % help)
                return redirect('%s?next=%s' %
                        (reverse('microtask_change_province'), next))
    else:
        form = SelectLocationForm()

    return render(request, 'atlas/select_location.html',
        {'next': next, 'form': form})


def jobs_list(request):
    return render(request, 'opportunities/jobs/jobs_list.html',
                              {'categories': CATEGORY_CHOICES})
