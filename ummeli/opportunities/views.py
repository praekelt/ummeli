from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.shortcuts import render


class OpportunityDetailView(DetailView):
    def get_object(self):
        return get_object_or_404(self.model, slug=self.kwargs['slug'])


class OpportunityListView(ListView):
    def get_queryset(self):
        return self.model.objects.filter(state='published')\
                                    .order_by('-created')


def opportunities(request):
    return render(request, 'opportunities/opportunities.html')
