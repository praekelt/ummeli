from ummeli.opportunities.tomtom.forms import (MicroTaskResponseForm,
    ChangeDeviceForm)
from ummeli.providers.forms import UploadTaskForm
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ummeli.opportunities.models import (MicroTask, TaskCheckout, Campaign,
    RETURNED, SUBMITTED)
from django.shortcuts import get_object_or_404
from ummeli.vlive.utils import get_lat_lon


@login_required
def task_instructions(request, slug):
    task = get_object_or_404(MicroTask, slug=slug)

    if not task.checked_out_by(request.user):
        messages.error(request, 'That task is not available for you.')
        return redirect(reverse('campaigns'))

    return render(request, 'opportunities/tomtom/microtask_instructions.html',
        {'object': task})


@login_required
def task_upload(request, slug,
        template_name='opportunities/microtasks/microtask_upload.html'):
    task = get_object_or_404(MicroTask, slug=slug)

    if not task.checked_out_by(request.user):
        messages.error(request, 'That task is no longer available.')
        return redirect(reverse('campaigns'))

    task_checkout = get_object_or_404(TaskCheckout, task=task,
                                        state__lte=RETURNED)
    if request.method == 'POST':
        if hasattr(task_checkout, 'microtaskresponse'):
            instance = task_checkout.microtaskresponse.tomtommicrotaskresponse
            form = MicroTaskResponseForm(request.POST, request.FILES,
                    instance=instance)
        else:
            form = MicroTaskResponseForm(request.POST, request.FILES)
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
            return redirect(reverse('micro_tasks', args=[task.campaign.slug]))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        if hasattr(task_checkout, 'microtaskresponse'):
            instance = task_checkout.microtaskresponse.tomtommicrotaskresponse
            form = MicroTaskResponseForm(instance=instance)
        else:
            form = MicroTaskResponseForm()

    return render(request, template_name,
            {'object': task,
            'city': request.session['location']['city'],
            'form': form,
            'task_checkout': task_checkout,
            })


@login_required
def qualify(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    context = {
        'object': campaign,
    }
    return render(request, 'opportunities/tomtom/qualify_detect.html', context)


@login_required
def qualify_device(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    context = {
        'object': campaign,
    }
    return render(request, 'opportunities/tomtom/qualify_device.html', context)


@login_required
def qualify_device_change(request):
    next = request.GET.get('next', reverse('campaigns'))
    if request.method == 'POST':
        form = ChangeDeviceForm(request.POST)
        if form.is_valid():
            request.session['device_override'] = form.cleaned_data['device']
            return redirect(next)
    else:
        form = ChangeDeviceForm()

    context = {
        'form': form,
        'next': next,
    }
    return render(request, 'opportunities/tomtom/qualify_device_change.html',
                    context)


@login_required
def device_instructions(request):
    next = request.GET.get('next', reverse('campaigns'))
    return render(request, 'opportunities/tomtom/device_instructions.html',
        {'next': next,
        })


@login_required
def qualify_upload(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    context = {
        'object': campaign,
    }

    if request.method == 'POST':
        form = UploadTaskForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['file']
            lat, lon = get_lat_lon(f)
            if lat and lon:
                campaign.qualifiers.add(request.user)
                return redirect(reverse('campaign_detail', args=[slug, ]))
            else:
                context['error'] = True
    else:
        form = UploadTaskForm()

    return render(request, 'opportunities/tomtom/qualify.html', context)


from django import forms
class UploadTestForm(forms.Form):
    file = forms.FileField(required=True)
    lat = forms.CharField(required=True, error_messages={'required': 'Image missing x-coordinate'})
    lon = forms.CharField(required=True, error_messages={'required': 'Image missing y-coordinate'})


def upload_test(request):
    lat = lon = exif = None
    if request.method == 'POST':
        form = UploadTestForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['file']
            lat = form.cleaned_data['lat']
            lon = form.cleaned_data['lon']
    else:
        form = UploadTestForm()

    context = {
        'lat': lat,
        'lon': lon,
        'form': form,
    }

    return render(request, 'opportunities/tomtom/upload_test.html', context)
