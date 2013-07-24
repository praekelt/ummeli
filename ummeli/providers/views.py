from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib import messages

from ummeli.opportunities.models import (Campaign, MicroTask, ACCEPTED,
    MicroTaskResponse, REJECTED, SUBMITTED, PAID)
from ummeli.providers.forms import UploadTaskForm, TaskResponseForm
from ummeli.providers.tasks import process_upload

from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from praekeltpayment.flickswitch.models import FlickSwitchPayment


def health(request):
    return HttpResponse("")


@staff_member_required
def index(request):
    campaign = Campaign.objects.filter(owner=request.user).latest('created')

    all_tasks = MicroTask.permitted.filter(campaign=campaign)
    live_tasks = MicroTask.available.filter(campaign=campaign)
    closed_tasks = MicroTask.permitted.filter(campaign=campaign,
                                              microtaskresponse__state=ACCEPTED,
                                              )

    context = {
        'object': campaign,
        'all_tasks': all_tasks,
        'live_tasks': live_tasks,
        'closed_tasks': closed_tasks,
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
    campaign_obj = get_object_or_404(Campaign,
                        owner=request.user,
                        slug=campaign)

    if request.method == 'POST':
        form = UploadTaskForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            temp_file = handle_uploaded_file(file)
            print '-------: %s' % temp_file
            process_upload.delay(temp_file, campaign)
            return redirect(reverse('index'))
    else:
        form = UploadTaskForm()

    return render(request, 'upload.html',
                {'form': form, 'campaign': campaign_obj})

from tempfile import NamedTemporaryFile
from ummeli.settings import abspath
def handle_uploaded_file(f):
    temp = NamedTemporaryFile(dir=abspath('providers/uploaded'),
                            delete=False)
    with open(temp.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return temp.name


@staff_member_required
def micro_task_detail(request, campaign, slug):
    campaign = get_object_or_404(Campaign,
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
                response.state = ACCEPTED
                response.save()
            else:
                msg = '%s`s submission has been rejected. `%s` is now live on Ummeli again.' % (
                    username, task.title)
                messages.add_message(request, messages.ERROR, msg)

                response.reject_reason = form.cleaned_data['reject_reason']
                response.reject_comment = form.cleaned_data['reject_comment']

                response.state = REJECTED
                response.save()
                return redirect(reverse('index'))
        else:
            print form
    else:
        form = TaskResponseForm()

    return render(request, 'opportunities/microtask_detail.html',
                  {'form': form, 'campaign': campaign, 'object': task})


def submit_payment(request, campaign, slug, response_id):
    if request.method == 'POST':
        get_object_or_404(Campaign, owner=request.user, slug=campaign)
        get_object_or_404(MicroTask, campaign__slug=campaign, slug=slug)
        response = get_object_or_404(MicroTaskResponse, pk=response_id)

        payment = FlickSwitchPayment.objects.create(msisdn=response.user.username,
                                                    amount=1000)
        payment.send_airtime()
        response.state = PAID
        response.save()

        msg = 'Payment has been made to `%s`' % response.user.username
        messages.success(request, msg)
    return redirect(reverse('providers.micro_task_detail',
                            args=[campaign, slug]))


class OpportunityDetailView(DetailView):
    def get_object(self):
        return get_object_or_404(self.model,
                    owner=self.request.user,
                    slug=self.kwargs['slug'])


class OpportunityListView(ListView):
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)\
                                    .order_by('-created')


class MicroTaskListView(OpportunityListView):
    def get_queryset(self):
        campaign = get_object_or_404(MicroTask,
                        owner=self.request.user,
                        slug=self.kwargs['slug'])
        return campaign.tasks.order_by('-created')


class TaskSubmissionsListView(ListView):
    paginate_by = 10
    template_name = 'opportunities/task_submissions.html'

    def get_queryset(self):
        campaign = get_object_or_404(Campaign,
                        owner=self.request.user,
                        slug=self.kwargs['campaign'])
        return MicroTaskResponse.objects.filter(task__campaign=campaign,
                                                state=SUBMITTED)\
                                        .order_by('date')


class TaskLiveListView(ListView):
    paginate_by = 10
    template_name = 'opportunities/task_live.html'

    def get_queryset(self):
        campaign = get_object_or_404(Campaign,
                        owner=self.request.user,
                        slug=self.kwargs['campaign'])
        return MicroTask.available.filter(campaign=campaign)\
                                    .order_by('created')


class TaskAcceptedListView(ListView):
    paginate_by = 10
    template_name = 'opportunities/task_accepted.html'

    def get_queryset(self):
        campaign = get_object_or_404(Campaign,
                                     owner=self.request.user,
                                     slug=self.kwargs['campaign'])
        return MicroTaskResponse.objects.filter(task__campaign=campaign,
                                                state=ACCEPTED)\
                                        .order_by('date')
