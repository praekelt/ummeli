import urlparse
import uuid
import string
import random

from datetime import datetime, date, timedelta, time

from django.conf import settings

from ummeli.base.models import (Certificate, Language, WorkExperience,
    Reference, CurriculumVitae, CurriculumVitaeForm,  Article,  Province,  Category,
    UserSubmittedJobArticle)
from ummeli.vlive.jobs import tasks
from ummeli.vlive.tasks import send_password_reset, send_email
from ummeli.vlive.utils import pin_required, process_post_data_username
from ummeli.vlive.forms import (EmailCVForm, FaxCVForm, MobiUserCreationForm,
                                UserSubmittedJobArticleForm, ForgotPasswordForm,
                                ConcactSupportForm, MyContactPrivacyForm,
                                MyCommentSettingsForm)

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,  redirect
from django.core.urlresolvers import reverse
from django.utils.hashcompat import md5_constructor
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import UpdateView

#imports for login
from django.http import  HttpResponse
from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login,
                                 logout as auth_logout,  authenticate)
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
    PasswordChangeForm, SetPasswordForm)

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
        form = ForgotPasswordForm(request.POST)
        
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
    community_list = UserSubmittedJobArticle.objects.all().order_by('-date')[:3]
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

def jobs_province(request):
    provinces = [province for province in Province.objects.all().order_by('name').annotate(articles_count=Count('category__articles', distinct=True), userarticles_count=Count('category__user_submitted_job_articles', distinct=True)) if province.category_set.exists()]
    return render(request, 'jobs_province.html', {'provinces': provinces})

def jobs_list(request,  id):
    categories = [category for category in Province.objects.get(search_id=id).category_set.all().order_by('title') if category.must_show()]
    return render(request, 'jobs_list.html',
                              {'categories': categories,
                              'search_id': id, 
                              'province_name': Province.objects.get(search_id=id).name})

def jobs(request,  id,  search_id):
    province = Province.objects.get(search_id=search_id)
    category = province.category_set.get(pk=id)

    all_jobs = []
    [all_jobs.append(a) for a in category.articles.all()]
    [all_jobs.append(a.to_view_model()) for a in category.user_submitted_job_articles.all()]

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

    return render(request, 'jobs.html',
                              {'articles': paged_jobs,
                              'search_id': search_id,
                              'cat_id': id,
                              'province_name': province.name, 
                              'category_title': category.title})

def job(request,  id,  cat_id,  search_id, user_submitted=0):
    form = None
    if int(user_submitted) == 1:
        if not UserSubmittedJobArticle.objects.filter(pk = id):
            return redirect(reverse('jobs',  args = [search_id,  cat_id])) # Sorry, this ad has been removed.
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

    return render(request, 'job.html',
                              {'job': article,
                              'search_id': search_id,
                              'cat_id': cat_id,
                              'province_name':  province.name,
                              'category_title':  category.title,
                              'form':  form,})

def community_jobs(request):
    articles = UserSubmittedJobArticle.objects.all().order_by('-date')
    
    paginator = Paginator(articles, 15) # Show 15 contacts per page
    page = request.GET.get('page', 'none')
    
    try:
        paged_jobs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paged_jobs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paged_jobs = paginator.page(paginator.num_pages)
    return render(request, 'community_jobs.html', {'articles': paged_jobs})
                             
def community_job(request, id):
    form = None
    if not UserSubmittedJobArticle.objects.filter(pk = id):
        return redirect(reverse('community_jobs')) # Sorry, this ad has been removed.
    article = UserSubmittedJobArticle.objects.get(pk = id)

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
                return redirect(reverse('community_jobs'))
            else:
                user_profile.fax_cv(send_to, article.text)
                return redirect(reverse('community_jobs'))

    return render(request, 'community_job.html',
                              {'job': article,
                              'form':  form,})

def send_thanks_job_apply(request,  cat_id,  search_id):
    return redirect(reverse('jobs',  args=[search_id,  cat_id]))

def jobs_cron(request):
    tasks.run_jobs_update.delay()
    return render(request, 'cron.html')

def about(request):
    return render(request, 'about.html')

def terms(request):
    return render(request, 'terms.html')

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
                                'user_articles': UserSubmittedJobArticle.objects.count()})

@login_required
@pin_required
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
                province = Province.objects.get(pk = int(request.POST.get('province')))

                category_title = request.POST.get('category')
                category_hash = md5_constructor('%s:%s' % (category_title, province.search_id)).hexdigest()
                if not Category.objects.filter(hash_key = category_hash).exists():
                    cat  = Category(province = province, hash_key = category_hash,  title = category_title)
                    cat.save()
                else:
                    cat  = Category.objects.get(hash_key = category_hash)

                user_article = form.save(commit=False)
                user_article.user = request.user
                user_article.province = province.name
                user_article.job_category = cat.title
                user_article.save()
                
                cat.user_submitted_job_articles.add(user_article)

            return redirect(reverse('my_jobs'))
    else:
        form = UserSubmittedJobArticleForm()

    provinces = Province.objects.all().order_by('name').exclude(pk=1)
    categories = Category.objects.all().values('title').distinct().order_by('title')

    return render(request, 'jobs_create.html',
                                {'form': form,  'provinces': provinces,
                                'categories': categories})
