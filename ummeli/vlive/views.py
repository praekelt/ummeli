import urlparse
import uuid
import string
import random

from django.conf import settings

from ummeli.base.models import (Certificate, Language, WorkExperience,
    Reference, CurriculumVitae, CurriculumVitaeForm)
from ummeli.vlive.forms import EmailCVForm,  FaxCVForm
from ummeli.vlive.jobs import tasks
from ummeli.vlive.tasks import send_password_reset

from ummeli.vlive.models import Article,  Province,  Category
from ummeli.vlive.forms import EmailCVForm,  FaxCVForm, UserSubmittedJobArticleForm
    
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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
    PasswordChangeForm)
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
                              mimetype='text/xml', 
                              context_instance=RequestContext(request, current_app=current_app))

def login(request, template_name='pml/login.xml',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
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
        form = UserCreationForm(data = request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            auth_login(request, new_user)

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
    return render_to_response('pml/register.xml', context,
                              mimetype='text/xml', 
                              context_instance=RequestContext(request))
                             
def logout_view(request):
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
            redirect_message = 'Thank you. Your new pin has been sent to you cellphone.')
        
    return render_to_response('pml/forgot_password.xml', 
                                            context_instance=RequestContext(request),  
                                            mimetype='text/xml')
    
@login_required
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
    return render_to_response('pml/password_change.xml', context,
                              mimetype='text/xml', 
                              context_instance=RequestContext(request))
                              
@cache_control(no_cache=True)
def index(request):    
    return render_to_response('pml/index.xml', {'uuid': str(uuid.uuid4()), 
        'user_exists': User.objects.filter(username=request.vlive.msisdn).exists()}, 
        context_instance= RequestContext(request), 
        mimetype='text/xml')
    
@cache_control(no_cache=True)
def home(request):    
    return render_to_response('pml/index.xml', {'uuid': str(uuid.uuid4()), 
        'user_exists': User.objects.filter(username=request.vlive.msisdn).exists()}, 
        context_instance= RequestContext(request), 
        mimetype='text/xml')

@login_required
@cache_control(no_cache=True)
def edit(request):    
    return render_to_response('pml/cv.xml',  {'uuid': str(uuid.uuid4())}, 
                                                context_instance= RequestContext(request), 
                                                mimetype='text/xml')

@login_required
def send(request):
    form = None
    
    if request.method == 'POST': 
        if(request.POST.get('send_via') == 'email'):
            form = EmailCVForm(data = request.POST)
        else:
            form = FaxCVForm(data = request.POST)
        if form.is_valid():
            send_via = form.cleaned_data['send_via']
            send_to = form.cleaned_data['send_to']
            
            user_profile = request.user.get_profile()
            
            if send_via == 'email':
                user_profile.email_cv(send_to)
                return send_thanks(request)
            else:
                user_profile.fax_cv(send_to)
                return send_thanks(request)
             
    return render_to_response('pml/send_cv.xml',  {'form': form},
                              mimetype='text/xml', 
                              context_instance= RequestContext(request), )

@login_required
def send_thanks(request):    
    return pml_redirect_timer_view(request,  reverse('home'),
                redirect_message = 'Thank you. Your CV will be sent shortly.')

def pml_redirect_timer_view(request,  redirect_url,  redirect_time = 20,  redirect_message = 'Thank you.'):
    return render(request, 'pml/redirect.xml',  
                                {'redirect_url': redirect_url, 
                                'redirect_time': redirect_time, 
                                'redirect_message': redirect_message}, 
                                content_type='text/xml')

def jobs_province(request):
    return render_to_response('pml/jobs_province.xml', 
                                                {'provinces': Province.objects.all().order_by('name')}, 
                                                context_instance= RequestContext(request), 
                                                mimetype='text/xml')

def jobs_list(request,  id):
    return render_to_response('pml/jobs_list.xml',  
                              {'categories': Province.objects.get(search_id=id).category_set.all().order_by('title'), 
                              'search_id': id}, 
                              context_instance= RequestContext(request), 
                              mimetype='text/xml')
                             
def jobs(request,  id,  search_id):
    province = Province.objects.get(search_id=search_id)
    category = province.category_set.get(pk=id)
    articles = category.articles.all()
    return render_to_response('pml/jobs.xml',  
                              {'articles': articles, 
                              'search_id': search_id, 
                              'cat_id': id, 
                              'title':  '%s :: %s' % (province.name,  category.title)}, 
                              context_instance= RequestContext(request), 
                              mimetype='text/xml')

def job(request,  id,  cat_id,  search_id):
    form = None
    
    if request.method == 'POST': 
        if(request.POST.get('send_via') == 'email'):
            form = EmailCVForm(data = request.POST)
        else:
            form = FaxCVForm(data = request.POST)
        
        if form.is_valid():
            send_via = form.cleaned_data['send_via']
            send_to = form.cleaned_data['send_to']
            
            article = Article.objects.get(pk = id)
            user_profile = request.user.get_profile()
            
            if send_via == 'email':
                user_profile.email_cv(send_to,  article.text)
                return send_thanks_job_apply(request,  cat_id,  search_id)
            else:
                user_profile.fax_cv(send_to, article.text)
                return send_thanks_job_apply(request,  cat_id,  search_id)
                
    province = Province.objects.get(search_id=search_id)
    category = Category.objects.get(pk = cat_id)
    article = Article.objects.get(pk = id)
    return render_to_response('pml/job.xml',  
                              {'job': article, 
                              'search_id': search_id, 
                              'cat_id': cat_id, 
                              'title':  '%s :: %s' % (province.name,  category.title), 
                              'form':  form,},
                              context_instance=RequestContext(request), 
                              mimetype='text/xml')

def send_thanks_job_apply(request,  cat_id,  search_id):
    return pml_redirect_timer_view(request, reverse('jobs',  args=[search_id,  cat_id]),
                redirect_message = 'Thank you. Your CV will be sent shortly.')

def jobs_cron(request):   
    tasks.run_jobs_update.delay()
    return render_to_response('vlive/cron.html')

def about(request):
    return render_to_response('pml/about.xml',  mimetype='text/xml', 
                              context_instance= RequestContext(request))

def terms(request):
    return render_to_response('pml/terms.xml',  mimetype='text/xml', 
                              context_instance= RequestContext(request))

def health(request):
    return HttpResponse("")

def jobs_create(request):    
    if request.method == 'POST': 
        form = UserSubmittedJobArticleForm(request.POST)
        if form.is_valid():
            user_article = form.save(commit=False)
            user_article.user = request.user
            user_article.save()
            
            province = Province.objects.get(pk = int(form.cleaned_data['province']))
            
            category_title = form.cleaned_data['category']
            category_hash = md5_constructor('%s:%s' % (category_title, province.search_id)).hexdigest()
            cat  = Category(province = province, hash_key = category_hash,  title = category_title)
            cat.save()
            
            cat.user_submitted_job_articles.add(user_article)
            
            return pml_redirect_timer_view(request,  reverse('home'),
                redirect_message = 'Thank you. Your job advert has been submitted.')
    else:
        form = UserSubmittedJobArticleForm() 
        
    provinces = Province.objects.all().exclude(pk=1)
    categories = Category.objects.all().values('title').distinct().order_by('title')
    
    return render(request, 'pml/jobs_create.xml',  
                                {'form': form,  'provinces': provinces,  
                                'categories': categories}, 
                                content_type='text/xml')
