from django.shortcuts import render


def internships(request):
    return render(request, 'opportunity/internships.html')


def job_detail(request, slug):
    return render(request, 'opportunity/job_detail.html')


def internship_detail(request, slug):
    return render(request, 'opportunity/internship_detail.html')


def bursary_detail(request, slug):
    return render(request, 'opportunity/bursary_detail.html')


def volunteer_detail(request, slug):
    return render(request, 'opportunity/volunteer_detail.html')


def training_detail(request, slug):
    return render(request, 'opportunity/training_detail.html')


def competition_detail(request, slug):
    return render(request, 'opportunity/competition_detail.html')


def event_detail(request, slug):
    return render(request, 'opportunity/event_detail.html')
