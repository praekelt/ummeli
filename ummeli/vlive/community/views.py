from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,  redirect
from django.core.urlresolvers import reverse
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib.sites.models import Site
from django.contrib import messages

from ummeli.opportunities.models import Job, UmmeliOpportunity, StatusUpdate, SkillsUpdate
from ummeli.vlive.forms import EmailCVForm, FaxCVForm
from ummeli.vlive.community.forms import StatusUpdateForm


current_site = Site.objects.get_current()


def community_jobs(request):
    posts = UmmeliOpportunity.objects.filter(is_community=True).order_by('-created')

    paginator = Paginator(posts, 15)  # Show 15 contacts per page
    page = request.GET.get('page', 'none')

    try:
        paged_posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paged_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paged_posts = paginator.page(paginator.num_pages)
    return render(request, 'opportunities/jobs/community_jobs.html',
                  {'articles': paged_posts})


def community_job(request, slug):
    form = None
    if not Job.objects.filter(slug=slug):
        return redirect(reverse('community_jobs'))  # Sorry, this ad has been removed.
    article = Job.objects.get(slug=slug)

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


class StatusUpdateView(FormView):
    """
    Renders and handles user status update view/form.
    """
    form_class = StatusUpdateForm
    template_name = "profile/community/status_edit.html"

    def get_context_data(self, *args, **kwargs):
        context = super(StatusUpdateView, self).get_context_data(*args, **kwargs)
        context.update({
            'statuses': StatusUpdate.objects.order_by('-created')[:5],
        })
        return context

    def form_valid(self, form):
        title = form.cleaned_data['title']
        s = StatusUpdate.objects.create(title=title,
                                        owner=self.request.user,
                                        state='published',
                                        is_community=True)
        s.sites.add(current_site)
        s.save()
        return redirect(reverse('status_update'))


class AdvertiseSkillsView(TemplateView):
    template_name = "profile/community/advertise_skills.html"

    def get_context_data(self, *args, **kwargs):
        context = super(AdvertiseSkillsView, self).get_context_data(*args, **kwargs)
        return context

def advertise_skills_post(request):
    if request.method == 'POST':
        s = SkillsUpdate.objects.create(title=request.user.username,
                                        owner=request.user,
                                        is_community=True,
                                        state='published')
        s.sites.add(current_site)
        s.save()
        msg = 'You skills have been posted.'
        messages.success(request, msg)
    return redirect(reverse('index'))
