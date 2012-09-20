from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from ummeli.base.models import PROVINCE_CHOICES
from ummeli.opportunities.models import Campaign
from ummeli.providers.forms import UploadTaskForm


class OpportunityDetailView(DetailView):
    def get_object(self):
        return get_object_or_404(self.model, slug=self.kwargs['slug'])


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


def campaign_qualify(request, slug):
    context = {
        'object': get_object_or_404(Campaign, slug=slug),
    }

    if request.method == 'POST':
        form = UploadTaskForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            result = check_file_for_gps(file)
            context['result'] = result
            #return redirect(reverse('providers.campaign_detail',\
            #                    args=[campaign, ]))
    else:
        form = UploadTaskForm()

    return render(request, 'opportunities/campaign_qualify.html', context)


def check_file_for_gps(file):
    return True
