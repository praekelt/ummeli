from django.shortcuts import render


def detail(request, slug):
    return render(request, 'opportunity/detail.html')
