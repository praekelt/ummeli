from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ummeli.opportunities.models import TaskCheckout


@login_required
def inbox(request):
    context = {
        'tasks_out': TaskCheckout.objects.filter(user=request.user,
                                                state=0),
        'tasks_expired': TaskCheckout.objects.filter(user=request.user,
                                                state=2),
        }
    return render(request, 'inbox/index.html', context)


@login_required
def my_microtasks(request):
    context = {
        'tasks_out': TaskCheckout.objects.filter(user=request.user,
                                                state=0),
        'tasks_expired': TaskCheckout.objects.filter(user=request.user,
                                                state=2),
        }
    return render(request, 'inbox/my_microtasks.html', context)
