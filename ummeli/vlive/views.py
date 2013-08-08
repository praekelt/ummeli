import urlparse
import string
import random

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.sites.models import Site
site = Site.objects.get_current()

from ummeli.opportunities.models import Job, Province as OpportunityProvince,\
    UmmeliOpportunity
from ummeli.base.models import CurriculumVitae, Article,  Province,\
    Category, ALL
from ummeli.vlive.jobs import tasks
from ummeli.vlive.community.forms import JobEditForm
from ummeli.vlive.tasks import send_password_reset, send_email
from ummeli.vlive.utils import pin_required, process_post_data_username
from ummeli.vlive.forms import (EmailCVForm, FaxCVForm, MobiUserCreationForm,
                                ForgotPasswordForm,
                                ConcactSupportForm, MyContactPrivacyForm,
                                MyCommentSettingsForm)

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,  redirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django.template import RequestContext

#imports for login
from django.http import HttpResponse
from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login,
                                 logout as auth_logout,  authenticate)
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm,\
    PasswordChangeForm, SetPasswordForm

from jmboarticles.models import Article as EditorialArticle


def login(request, template_name='login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):

    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=process_post_data_username(request.POST))
        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL

            # setting the PIN for this session
            request.session[settings.UMMELI_PIN_SESSION_KEY] = True

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return redirect(redirect_to)
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    return render(request, template_name,
              {'form': form, redirect_field_name: redirect_to})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        # we need to call this so user.backend is set properly,
        # Django's session / login mechanics require it.
        user = authenticate(remote_user=username)
        form = SetPasswordForm(user, data=request.POST)
        if form.is_valid():
            form.save()
            # setting the PIN for this session
            request.session[settings.UMMELI_PIN_SESSION_KEY] = True
            # redirect through Django's auth mechanisms
            auth_login(request, user)
            return redirect(reverse('home'))
    else:
        form = UserCreationForm()

    return render(request, 'register.html',{'form': form})

def mobi_register(request):
    if request.method == 'POST':
        post_data = process_post_data_username(request.POST)
        username = post_data['username']
        form = MobiUserCreationForm(post_data)
        if form.is_valid():
            form.save()
            #auto-login user
            password = request.POST.get('password1')
            user = authenticate(username=username,  password=password)
            auth_login(request, user)
            request.session[settings.UMMELI_PIN_SESSION_KEY] = True
            return redirect(reverse('home'))
    else:
        form = MobiUserCreationForm()

    return render(request, 'register.html',{'form': form})

def logout_view(request):
    # remove the pin from the session
    request.session.pop(settings.UMMELI_PIN_SESSION_KEY, None)
    auth_logout(request)
    return redirect(reverse('home'))

def generate_password(length=6, chars=string.letters + string.digits):
    return ''.join([random.choice(chars) for i in range(length)])

def forgot_password_view(request):
    if request.method == 'POST':
        post_data = process_post_data_username(request.POST)
        form = ForgotPasswordForm(post_data)

        if(form.is_valid()):
            username = form.cleaned_data['username']
            new_password = generate_password(chars = string.digits)

            send_password_reset.delay(username,  new_password)

            user = User.objects.get(username = username)
            user.set_password(new_password)
            user.save()

            return redirect(reverse('login'))
    else:
        form = ForgotPasswordForm()

    return render(request,'forgot_password.html', {'form': form})

@login_required
@pin_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,  data = request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect(reverse('home'))
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'password_change.html', {'form': form})

def index(request):
    community_list = UmmeliOpportunity.objects.filter(is_community=True).order_by('-created')[:3]
    return render(request, 'index.html', {'community_list': community_list})

@login_required
@pin_required
def my_ummeli(request):
    return render(request, 'my_ummeli.html')

@login_required
@pin_required
def my_settings(request):
    return render(request, 'my_settings.html')

class MyContactPrivacyEditView(UpdateView):
    model = CurriculumVitae
    form_class = MyContactPrivacyForm
    template_name = 'my_contact_privacy.html'

    def get_success_url(self):
        return reverse("my_settings")

    def get_object(self, queryset=None):
        return self.request.user.get_profile()

class MyCommentSettingsEditView(UpdateView):
    model = CurriculumVitae
    form_class = MyCommentSettingsForm
    template_name = 'my_comment_settings.html'

    def get_success_url(self):
        return reverse("my_settings")

    def get_object(self, queryset=None):
        return self.request.user.get_profile()

@login_required
@pin_required
def send(request):
    form = None

    if request.method == 'POST':
        if(request.POST.get('send_via') == 'email'):
            form = EmailCVForm(data = request.POST)
        else:
            form = FaxCVForm(data = request.POST)

        user_profile = request.user.get_profile()

        if form.is_valid() and not user_profile.missing_fields():
            send_via = form.cleaned_data['send_via']
            send_to = form.cleaned_data['send_to']
            send_message = form.cleaned_data['send_message']

            if send_via == 'email':
                user_profile.email_cv(send_to, email_message=send_message)
                return send_thanks(request)
            else:
                user_profile.fax_cv(send_to, email_message=send_message)
                return send_thanks(request)

    return render(request, 'send_cv.html', {'form': form})

@login_required
@pin_required
def send_thanks(request):
    return redirect(reverse('my_ummeli'))

def get_search_id(request):
    search_ids = ((0,1),
                    (1,-5),
                    (2,-3),
                    (3,2),
                    (4,6),
                    (5,-1),
                    (6,-2),
                    (7,-6),
                    (8,-4),
                    (9,5))
    province = int(RequestContext(request)['province_id'])
    return dict(search_ids)[province]

def jobs_list(request):
    id = get_search_id(request)
    categories = [category for category in Province.objects.get(search_id=id).category_set.all().order_by('title') if category.must_show()]
    return render(request, 'opportunities/jobs/jobs_list.html',
                              {'categories': categories})

def jobs(request, id):
    search_id = get_search_id(request)

    province = Province.objects.get(search_id=search_id)

    if not province.category_set.filter(pk=id).exists():
        return redirect(reverse('jobs_list'))

    category = province.category_set.get(pk=id)

    all_jobs = []
    [all_jobs.append(a) for a in category.articles.all()]

    #TODO: filter jobs in a category (Job.objects.filter(category=category))
    #[all_jobs.append(a.to_view_model()) for a in category.user_submitted_job_articles.all()]

    ummeli_jobs = Job.from_str(category.title)

    if province.name == 'All':
        [all_jobs.append(a.to_view_model()) for a in ummeli_jobs]
    else:
        a_province = OpportunityProvince.from_str(province.name)
        [all_jobs.append(a.to_view_model())
            for a in ummeli_jobs.filter(province__in=[a_province, ALL])]

    all_jobs = sorted(all_jobs, key=lambda job: job.date, reverse=True)

    paginator = Paginator(all_jobs, 15) # Show 25 contacts per page
    page = request.GET.get('page', 'none')

    try:
        paged_jobs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paged_jobs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paged_jobs = paginator.page(paginator.num_pages)

    return render(request, 'opportunities/jobs/jobs.html',
                              {'articles': paged_jobs,
                              'cat_id': id,
                              'province_name': province.name,
                              'category_title': category.title})

def job(request,  cat_id,  id, user_submitted=0):
    search_id = get_search_id(request)

    form = None
    if int(user_submitted) == 1:
        if not Job.objects.filter(pk=id).exists():
            return redirect(reverse('jobs', args=[cat_id]))  # Sorry, this ad has been removed.
        article = Job.objects.get(pk=id).to_view_model()
    else:
        if not Article.objects.filter(pk=id).exists():
            return redirect(reverse('jobs', args=[cat_id]))
        article = Article.objects.get(pk=id)

    if request.method == 'POST':
        if(request.POST.get('send_via') == 'email'):
            form = EmailCVForm(data = request.POST)
        else:
            form = FaxCVForm(data = request.POST)

        user_profile = request.user.get_profile()

        if form.is_valid() and not user_profile.missing_fields():
            send_via = form.cleaned_data['send_via']
            send_to = form.cleaned_data['send_to']

            if send_via == 'email':
                user_profile.email_cv(send_to,  article.text)
                return send_thanks_job_apply(request,  cat_id)
            else:
                user_profile.fax_cv(send_to, article.text)
                return send_thanks_job_apply(request,  cat_id)

    province = Province.objects.get(search_id=search_id)
    category = Category.objects.get(pk = cat_id)

    return render(request, 'opportunities/jobs/job.html',
                              {'job': article,
                              'cat_id': cat_id,
                              'province_name':  province.name,
                              'category_title':  category.title,
                              'form':  form,})

def connection_job(request, user_id, pk):
    article = get_object_or_404(UmmeliOpportunity, pk = pk).to_view_model()

    if request.method == 'POST':
        if(request.POST.get('send_via') == 'email'):
            form = EmailCVForm(data = request.POST)
        else:
            form = FaxCVForm(data = request.POST)

        user_profile = request.user.get_profile()

        if form.is_valid() and not user_profile.missing_fields():
            send_via = form.cleaned_data['send_via']
            send_to = form.cleaned_data['send_to']

            if send_via == 'email':
                user_profile.email_cv(send_to,  article.text)
            else:
                user_profile.fax_cv(send_to, article.text)
            return redirect(reverse('connection_jobs', args=[user_id]))

    return redirect(reverse('my_connections'))


def send_thanks_job_apply(request,  cat_id):
    return redirect(reverse('jobs',  args=[cat_id]))

def jobs_cron(request):
    tasks.run_jobs_update.delay()
    return render(request, 'cron.html')

def about(request):
    return render(request, 'about.html')

def terms(request):
    return render(request, 'terms.html')

def tips(request):
    articles = EditorialArticle.objects.filter(published=True)\
                                       .filter(categories__slug="tips")\
                                       .order_by('-published_on')

    return render(request, 'tips.html', {'articles': articles})

def contact_support(request):
    if request.method == 'POST':
        form = ConcactSupportForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            message = form.cleaned_data['message']
            send_email(username, message)
            return redirect(reverse('home'))
    else:
        form = ConcactSupportForm(request.user)

    return render(request, 'contact_support.html', {'form': form})

def health(request):
    return HttpResponse("")

def stats(request):
    users_count = User.objects.count()
    cvs_complete = len([cv for cv in CurriculumVitae.objects.all() if cv.is_complete])
    cvs_complete_percent = (cvs_complete*1.00/users_count)*100.00
    return render(request, 'stats.html',
                                {'users': users_count,
                                'cvs_complete': cvs_complete,
                                'cvs_complete_percent': cvs_complete_percent,
                                'user_articles': UmmeliOpportunity.objects.count()})

@login_required
@pin_required
def jobs_create(request):
    if request.method == 'POST':
        form = JobEditForm(request.POST)

        title = request.POST.get('title')
        description = request.POST.get('description')
        # check if the user hasn't placed the exact same job article
        # with the exact same information in the last 5 minutes to prevent duplicates
        delta = datetime.now() - timedelta(minutes=5)
        duplicate = Job.objects \
                        .filter(owner=request.user, created__gte=delta, title=title,  description=description) \
                        .exists()
        if form.is_valid():
            if not duplicate:
                user_article = form.save(commit=False)
                user_article.owner = request.user
                user_article.state = 'published'
                user_article.is_community = True
                user_article.publish_on = datetime.now()
                user_article.save()
                user_article.sites.add(site)
                user_article.province.add(form.cleaned_data['province'])
            return redirect(reverse('my_jobs'))
    else:
        form = JobEditForm()

    return render(request, 'opportunities/jobs/jobs_create.html',
                                {'form': form})
