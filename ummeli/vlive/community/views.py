from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,  redirect
from django.core.urlresolvers import reverse

from ummeli.base.models import UserSubmittedJobArticle
from ummeli.vlive.forms import EmailCVForm, FaxCVForm


def community_jobs(request):
    articles = UserSubmittedJobArticle.objects.all().order_by('-date')

    paginator = Paginator(articles, 15)  # Show 15 contacts per page
    page = request.GET.get('page', 'none')

    try:
        paged_jobs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paged_jobs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paged_jobs = paginator.page(paginator.num_pages)
    return render(request, 'opportunities/jobs/community_jobs.html',
                  {'articles': paged_jobs})


def community_job(request, id):
    form = None
    if not UserSubmittedJobArticle.objects.filter(pk=id):
        return redirect(reverse('community_jobs'))  # Sorry, this ad has been removed.
    article = UserSubmittedJobArticle.objects.get(pk=id)

    if request.method == 'POST':
        if(request.POST.get('send_via') == 'email'):
            form = EmailCVForm(data=request.POST)
        else:
            form = FaxCVForm(data=request.POST)

        user_profile = request.user.get_profile()

        if form.is_valid() and not user_profile.missing_fields():
            send_via = form.cleaned_data['send_via']
            send_to = form.cleaned_data['send_to']

            if send_via == 'email':
                user_profile.email_cv(send_to,  article.text)
                return redirect(reverse('community_jobs'))
            else:
                user_profile.fax_cv(send_to, article.text)
                return redirect(reverse('community_jobs'))

    return render(request, 'opportunities/jobs/community_job.html',
                  {'job': article, 'form':  form})
