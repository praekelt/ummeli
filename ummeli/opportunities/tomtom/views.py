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
def task_upload(request, slug):
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
            return redirect(reverse('campaigns'))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        if hasattr(task_checkout, 'microtaskresponse'):
            instance = task_checkout.microtaskresponse.tomtommicrotaskresponse
            form = MicroTaskResponseForm(instance=instance)
        else:
            form = MicroTaskResponseForm()

    return render(request, 'opportunities/microtasks/microtask_upload.html',
            {'object': task,
            'city': request.session['location']['city'],
            'form': form,
            })


def get_recognised_device(request):
    if request.session.get('device_override'):
        device = request.session.get('device_override')
    else:
        device = request.META.get('HTTP_X_UA_BRAND_NAME', None)

    return {
        'nokia': {
            'name': device,
            'template': 'opportunities/tomtom/qualify_device_nokia.html'
        },
        'samsung': {
            'name': device,
            'template': 'opportunities/tomtom/qualify_device_samsung.html'
        },
        'rim': {
            'name': 'BlackBerry',
            'template': 'opportunities/tomtom/qualify_device_blackberry.html'
        },
        'apple': {
            'name': device,
            'template': 'opportunities/tomtom/qualify_device_apple.html'
        },
        'motorola': {
            'name': device,
            'template': 'opportunities/tomtom/qualify_device_motorola.html'
        },
        'android': {
            'name': 'Google Nexus / Android',
            'template': 'opportunities/tomtom/qualify_device_google.html'
        },
    }.get(device.lower(),
        {'name': 'Other',
        'template': 'opportunities/tomtom/qualify_device_other.html'})


@login_required
def qualify(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    context = {
        'object': campaign,
        'device': get_recognised_device(request)
    }
    return render(request, 'opportunities/tomtom/qualify_detect.html', context)


@login_required
def qualify_device(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    context = {
        'object': campaign,
        'device': get_recognised_device(request)
    }
    return render(request, 'opportunities/tomtom/qualify_device.html', context)


@login_required
def qualify_device_change(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)

    if request.method == 'POST':
        form = ChangeDeviceForm(request.POST)
        if form.is_valid():
            request.session['device_override'] = form.cleaned_data['device']
            return redirect(reverse('qualify_device', args=[slug, ]))
    else:
        form = ChangeDeviceForm()

    context = {
        'object': campaign,
        'device': get_recognised_device(request),
        'form': form
    }
    return render(request, 'opportunities/tomtom/qualify_device_change.html',
                    context)


@login_required
def qualify_upload(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    context = {
        'object': campaign,
        'device': get_recognised_device(request)
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

    return render(request, 'opportunities/tomtom/qualify.html', context)
