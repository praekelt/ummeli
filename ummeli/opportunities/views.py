from django.shortcuts import render


def internships(request):
    return render(request, 'opportunity/internships.html')


def opportunity_detail(request, slug):
    return render(request, 'opportunity/internship_detail.html')
