import urlparse
import uuid
import string
import random

from datetime import datetime, date, timedelta, time

from django.conf import settings

from ummeli.base.models import (Certificate, Language, WorkExperience,
    Reference, CurriculumVitae, CurriculumVitaeForm,  Article,  Province,  Category,
    UserSubmittedJobArticle)
from ummeli.vlive.forms import EmailCVForm,  FaxCVForm
from ummeli.vlive.jobs import tasks
from ummeli.vlive.tasks import send_password_reset
from ummeli.vlive.utils import pin_required, pml_redirect_timer_view
from ummeli.vlive.forms import EmailCVForm,  FaxCVForm, UserSubmittedJobArticleForm

from ummeli.vlive.forms import EmailCVForm,  FaxCVForm, UserSubmittedJobArticleForm

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response,  render
from django.core.urlresolvers import reverse
from django.utils.hashcompat import md5_constructor

#imports for login
from django.http import HttpResponseRedirect,  HttpRequest, HttpResponse
from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login,
                                 logout as auth_logout,  authenticate)
from django.template import RequestContext
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
    PasswordChangeForm, SetPasswordForm)
from django.contrib.sites.models import get_current_site
from django.views.decorators.csrf import csrf_protect

from django.views.decorators.cache import cache_control

def render_to_login(request,  form,  redirect_to,  template_name,
                                current_app = None,
                                extra_context = None,
                                redirect_field_name=REDIRECT_FIELD_NAME):
    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'msisdn': request.vlive.msisdn,
        'user_exists': User.objects.filter(username=request.vlive.msisdn).exists()
    }
    context.update(extra_context or {})
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request, current_app=current_app))

def login(request, template_name=None,
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
              
    if not template_name:
        template_name = '%s/%s' % (request.template_dir, 'login.html')
    """
Displays the login form and handles the login action.
"""
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST)
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

            return pml_redirect_timer_view(request, redirect_to,
                redirect_time = 0,
                redirect_message = 'You have been logged in.')
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    return render_to_login(request,  form,  redirect_to,  template_name)

def register(request):
    if request.method == 'POST':
        # we need to call this so user.backend is set properly,
        # Django's session / login mechanics require it.
        user = authenticate(remote_user=request.user.username)
        form = SetPasswordForm(user, data=request.POST)
        if form.is_valid():
            form.save()
            # setting the PIN for this session
            request.session[settings.UMMELI_PIN_SESSION_KEY] = True
            # redirect through Django's auth mechanisms
            auth_login(request, user)
            return pml_redirect_timer_view(request, reverse('home'),
                redirect_time = 0,
                redirect_message = 'Thank you. You are now registered.')
    else:
        form = UserCreationForm()

    context = {
        'form': form,
        'msisdn': request.vlive.msisdn,
        'uuid': str(uuid.uuid4()),
    }
    return render_to_response('%s/%s' % (request.template_dir, 'register.html'),
                               context,
                              context_instance=RequestContext(request))

def logout_view(request):
    # remove the pin from the session
    request.session.pop(settings.UMMELI_PIN_SESSION_KEY, None)
    auth_logout(request)
    return pml_redirect_timer_view(request, reverse('home'),
                redirect_time = 0,
                redirect_message = 'You have been logged out.')

def generate_password(length=6, chars=string.letters + string.digits):
    return ''.join([random.choice(chars) for i in range(length)])

def send_password(request,  new_password):
    send_password_reset.delay(request.vlive.msisdn,  new_password)

def forgot_password_view(request):
    if request.method == 'POST':
        new_password = generate_password(chars = string.digits)

        send_password(request,  new_password)
        user = User.objects.get(username = request.vlive.msisdn)
        user.set_password(new_password)
        user.save()

        return pml_redirect_timer_view(request,  reverse('login'),
            redirect_time = 50,
            redirect_message = 'Thank you. Your new pin has been sent to your cellphone.')

    return render_to_response('%s/%s' % (request.template_dir, 'forgot_password.html'),
                                            context_instance=RequestContext(request),
                                            )

@login_required
@pin_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,  data = request.POST)
        if form.is_valid():
            new_user = form.save()
            return pml_redirect_timer_view(request,  reverse('home'),
                redirect_message = 'Thank you. Your pin has been changed.')
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form,
        'msisdn': request.vlive.msisdn,
        'uuid': str(uuid.uuid4()),
    }
    return render_to_response('%s/%s' % (request.template_dir, 'password_change.html'), 
                              context,
                              context_instance=RequestContext(request))

@cache_control(no_cache=True)
def index(request):
    return render_to_response('%s/%s' % (request.template_dir, 'index.html'),
        context_instance= RequestContext(request),
        )

@cache_control(no_cache=True)
def home(request):
    return render_to_response('%s/%s' % (request.template_dir, 'index.html'), {'uuid': str(uuid.uuid4()),
        'user_exists': User.objects.filter(username=request.vlive.msisdn).exists()},
        context_instance= RequestContext(request),
        )

@login_required
@pin_required
@cache_control(no_cache=True)
def edit(request):
    return render_to_response('%s/%s' % (request.template_dir, 'cv.html'),  {'uuid': str(uuid.uuid4())},
                                                context_instance= RequestContext(request),
                                                )

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

            if send_via == 'email':
                user_profile.email_cv(send_to)
                return send_thanks(request)
            else:
                user_profile.fax_cv(send_to)
                return send_thanks(request)

    return render_to_response('%s/%s' % (request.template_dir, 'send_cv.html'),  
                              {'form': form},
                              context_instance= RequestContext(request), )

@login_required
@pin_required
def send_thanks(request):
    return pml_redirect_timer_view(request,  reverse('home'),
                redirect_message = 'Thanks! Your CV is on its way to a prospective employer. Good luck!')

def jobs_province(request):
    provinces = [province for province in Province.objects.all().order_by('name') if province.category_set.exists()]
    return render_to_response('%s/%s' % (request.template_dir, 'jobs_province.html'),
                                                {'provinces': provinces},
                                                context_instance= RequestContext(request),
                                                )

def jobs_list(request,  id):
    categories = [category for category in Province.objects.get(search_id=id).category_set.all().order_by('title') if category.must_show()]
    return render_to_response('%s/%s' % (request.template_dir, 'jobs_list.html'),
                              {'categories': categories,
                              'search_id': id},
                              context_instance= RequestContext(request),
                              )

def jobs(request,  id,  search_id):
    province = Province.objects.get(search_id=search_id)
    category = province.category_set.get(pk=id)

    all_jobs = []
    [all_jobs.append(a) for a in category.articles.all()]
    [all_jobs.append(a.to_view_model()) for a in category.user_submitted_job_articles.all()]

    all_jobs = sorted(all_jobs, key=lambda job: job.date, reverse=True)
    articles = category.articles.all()

    return render_to_response('%s/%s' % (request.template_dir, 'jobs.html'),
                              {'articles': all_jobs,
                              'search_id': search_id,
                              'cat_id': id,
                              'title':  '%s :: %s' % (province.name,  category.title)},
                              context_instance= RequestContext(request),
                              )

def job(request,  id,  cat_id,  search_id):
    form = None
    if request.GET.get('user_submitted'):
        if not UserSubmittedJobArticle.objects.filter(pk = id):
            return pml_redirect_timer_view(request,  
                                reverse('jobs',  args = [search_id,  cat_id]),
                                redirect_message = 'Sorry, this ad has been removed.')
        article = UserSubmittedJobArticle.objects.get(pk = id).to_view_model()
    else:
        article = Article.objects.get(pk = id)

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
                return send_thanks_job_apply(request,  cat_id,  search_id)
            else:
                user_profile.fax_cv(send_to, article.text)
                return send_thanks_job_apply(request,  cat_id,  search_id)

    province = Province.objects.get(search_id=search_id)
    category = Category.objects.get(pk = cat_id)

    return render_to_response('%s/%s' % (request.template_dir, 'job.html'),
                              {'job': article,
                              'search_id': search_id,
                              'cat_id': cat_id,
                              'title':  '%s :: %s' % (province.name,  category.title),
                              'form':  form,},
                              context_instance=RequestContext(request),
                              )

def send_thanks_job_apply(request,  cat_id,  search_id):
    return pml_redirect_timer_view(request, reverse('jobs',  args=[search_id,  cat_id]),
                redirect_message = 'Thanks! Your CV is on its way to a prospective employer. Good luck!')

def jobs_cron(request):
    tasks.run_jobs_update.delay()
    return render_to_response('vlive/cron.html')

def about(request):
    return render_to_response('%s/%s' % (request.template_dir, 'about.html'),
                              context_instance= RequestContext(request))

def terms(request):
    return render_to_response('%s/%s' % (request.template_dir, 'terms.html'),
                              context_instance= RequestContext(request))

def health(request):
    return HttpResponse("")

def stats(request):
    cvs_complete = len([cv for cv in CurriculumVitae.objects.all() if cv.is_complete])
    return render(request, 'stats.html',
                                {'users': User.objects.count(), 
                                'cvs_complete': cvs_complete, 
                                'user_articles': UserSubmittedJobArticle.objects.count()})

@login_required
def jobs_create(request):
    if request.method == 'POST':
        form = UserSubmittedJobArticleForm(request.POST)
        
        title = request.POST.get('title')
        text = request.POST.get('text')
        # check if the user hasn't placed the exact same job article
        # with the exact same information in the last 5 minutes to prevent duplicates
        delta = datetime.now() - timedelta(minutes=5)
        duplicate = UserSubmittedJobArticle.objects \
                        .filter(user=request.user, date__gte=delta, title = title,  text = text) \
                        .exists()
        if form.is_valid():
            if not duplicate:
                user_article = form.save(commit=False)
                user_article.user = request.user
                user_article.save()

                province = Province.objects.get(pk = int(request.POST.get('province')))

                category_title = request.POST.get('category')
                category_hash = md5_constructor('%s:%s' % (category_title, province.search_id)).hexdigest()
                if not Category.objects.filter(hash_key = category_hash).exists():
                    cat  = Category(province = province, hash_key = category_hash,  title = category_title)
                    cat.save()
                else:
                    cat  = Category.objects.get(hash_key = category_hash)

                cat.user_submitted_job_articles.add(user_article)

            return pml_redirect_timer_view(request,  reverse('home'),
                redirect_message = 'Thank you. Your job advert has been submitted.')
    else:
        form = UserSubmittedJobArticleForm()

    provinces = Province.objects.all().order_by('name').exclude(pk=1)
    categories = Category.objects.all().values('title').distinct().order_by('title')

    return render(request, '%s/%s' % (request.template_dir, 'jobs_create.html'),
                                {'form': form,  'provinces': provinces,
                                'categories': categories})
