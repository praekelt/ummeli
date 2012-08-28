from django.shortcuts import render
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404


class OpportunityDetailView(DetailView):
    def get_object(self):
        return get_object_or_404(self.model, slug=self.kwargs['slug'])


def internships(request):
    return render(request, 'opportunities/internships.html')


def job_detail(request, slug):
    return render(request, 'opportunities/job_detail.html')


def internship_detail(request, slug):
    return render(request, 'opportunities/internship_detail.html')


def bursary_detail(request, slug):
    return render(request, 'opportunities/bursary_detail.html')


def volunteer_detail(request, slug):
    return render(request, 'opportunities/volunteer_detail.html')


def training_detail(request, slug):
    return render(request, 'opportunities/training_detail.html')


def competition_detail(request, slug):
    return render(request, 'opportunities/competition_detail.html')


def event_detail(request, slug):
    return render(request, 'opportunities/event_detail.html')
