from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from ummeli.base.models import PROVINCE_CHOICES


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
    return render(request, 'opportunities/opportunities.html')


def change_province(request, province=None):
    next = request.GET.get('next', reverse('opportunities'))

    if province and int(province) in range(0, 10):
        request.session['province'] = int(province)
        print request.session['province']
        return redirect(next)

    return render(request, 'opportunities/change_province.html',
                {'provinces': PROVINCE_CHOICES,
                'next': next})
