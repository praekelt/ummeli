from django.shortcuts import render


def detail(request, slug):
    return render(request, 'opportunity/detail.html')


def internship_detail(request, slug):
    return render(request, 'opportunity/internship_detail.html')
