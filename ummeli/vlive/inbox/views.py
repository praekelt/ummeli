from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
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


class MyTaskCheckoutListView(ListView):
    paginate_by = 10
    template_name = 'inbox/my_microtasks.html'

    def get_queryset(self):
        return TaskCheckout.objects.filter(user=self.request.user)\
                                    .order_by('state')
