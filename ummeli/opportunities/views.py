from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from ummeli.base.models import PROVINCE_CHOICES
from ummeli.opportunities.models import *


class OpportunityDetailView(DetailView):
    def get_object(self):
        return get_object_or_404(self.model, slug=self.kwargs['slug'])


class OpportunityListView(ListView):
    paginate_by = 10

    def get_queryset(self):
        province = int(RequestContext(self.request)['province_id'])
        province_qs = self.model.objects.filter(state='published')

        if province > 0:
            province_qs = province_qs.filter(province__province__in=[province, 0])

        return province_qs.order_by('-created')


def opportunities(request):
    context = {
        'bursaries': Bursary.objects.all().exists(),
        'internships': Internship.objects.all().exists(),
        'volunteering': Volunteer.objects.all().exists(),
        'training': Training.objects.all().exists(),
        'competitions': Competition.objects.all().exists(),
        'events': Event.objects.all().exists(),
    }
    return render(request, 'opportunities/opportunities.html', context)


def change_province(request, province=None):
    next = request.GET.get('next', reverse('opportunities'))

    if province and int(province) in range(0, 10):
        request.session['province'] = int(province)
        print request.session['province']
        return redirect(next)

    return render(request, 'opportunities/change_province.html',
                {'provinces': PROVINCE_CHOICES,
                'next': next})
