import urlparse
from django.conf import settings

from ummeli.api.models import (Certificate, Language, WorkExperience,
    Reference, CurriculumVitae, CurriculumVitaeForm)
from ummeli.vlive.utils import render_to_pdf
from ummeli.vlive.forms import SendEmailForm,  SendFaxForm

    
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.mail import send_mail,  EmailMessage

#imports for login
from django.http import HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.template import RequestContext
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.sites.models import get_current_site
from django.views.decorators.csrf import csrf_protect

def render_to_login(request,  form,  redirect_to,  template_name,  
                                current_app = None, 
                                extra_context = None, 
                                redirect_field_name=REDIRECT_FIELD_NAME):
    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        'msisdn': request.vlive.msisdn,
        'user_exists': User.objects.filter(username=request.vlive.msisdn).exists()
    }
    context.update(extra_context or {})
    return render_to_response(template_name, context
                              , mimetype='text/xml'
                              , context_instance=RequestContext(request, current_app=current_app))

@csrf_protect
def login(request, template_name='pml/login.xml',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    #redirect_to = request.REQUEST.get(redirect_field_name, '')
    redirect_to = reverse('home')
    
    form = authentication_form(request)

    request.session.set_test_cookie()

    return render_to_login(request,  form,  redirect_to,  template_name)

def login_post(request,  template_name,  
                        authentication_form=AuthenticationForm):
    #redirect_to = request.REQUEST.get(redirect_field_name, '')
    redirect_to = reverse('home')
    
    form = authentication_form(data=request.GET)
    print form
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

        return render_to_response('pml/index.xml',  mimetype='text/xml')
    
    return render_to_login(request,  form,  redirect_to,  template_name)

def register(request,  template_name = 'pml/register.xml'):
    if request.method == 'POST':
        form = UserCreationForm(data = request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserCreationForm()
    
    current_site = get_current_site(request)
    
    context = {
        'form': form,
        'msisdn': request.vlive.msisdn,
    }
    return render_to_response(template_name, context,
                              mimetype='text/xml', 
                              context_instance=RequestContext(request))
    
def logout_view(request):
    auth_logout(request)
    return login(request)
    
@login_required
def index(request):    
    return render_to_response('pml/index.xml',  mimetype='text/xml')
    
@login_required
def home(request):    
    return render_to_response('pml/index.xml',  mimetype='text/xml')

@login_required
def edit(request):    
    return render_to_response('vlive/cv.html')

@login_required
def send(request):    
    return render_to_response('vlive/send_cv.html')
    
def send_email(request, email_address):
    cv = request.user.get_profile()
    fullname = '%s %s' % (cv.firstName,  cv.surname)
    email = EmailMessage('CV for %s' % fullname, 
                                        '''
Hi,
%s has chosen to send you their CV.
See attachment for details.

Brought to you by,
Ummeli
www.praekeltfoundation.org/ummeli
 ''' % fullname, 
                                        'no-reply@ummeli.org',
                                        [email_address])
    pdf = render_to_pdf('vlive/pdf_template.html', {'model': cv})
    email.attach('curriculum_vitae_for_%s_%s' % (cv.firstName,  
                                                                                cv.surname), 
                        pdf,  'application/pdf')
    return email.send(fail_silently=False)
    
@login_required
def send_via_email(request):    
    redirect_url = ('%s/%s' % (reverse('send'),'thanks'))
    if request.method == 'POST': 
        cancel = request.POST.get('cancel', None)
        if cancel:
            return HttpResponseRedirect(reverse('send'))
            
        form = SendEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            send_email(request,  email)
            return HttpResponseRedirect(redirect_url) 
    else:
        form = SendEmailForm() 

    return render_to_response('vlive/send_via.html', 
                                            {'form': form,'via': 'Email'}, 
                                            context_instance=RequestContext(request))

@login_required
def send_via_fax(request):    
    redirect_url = ('%s/%s' % (reverse('send'),'thanks'))
    if request.method == 'POST': 
        cancel = request.POST.get('cancel', None)
        if cancel:
            return HttpResponseRedirect(reverse('send'))
            
        form = SendFaxForm(request.POST)
        if form.is_valid():
            fax = form.cleaned_data['fax']
            send_email(request,  '%s@faxfx.net' % fax.replace(' ', ''))
            return HttpResponseRedirect(redirect_url) 
    else:
        form = SendFaxForm() 

    return render_to_response('vlive/send_via.html', 
                                            {'form': form, 'via':  'Fax'}, 
                                            context_instance=RequestContext(request))
                                            

@login_required
def send_thanks(request):    
    return render_to_response('vlive/send_thanks.html')
    
@login_required
def jobs(request):    
    return render_to_response('vlive/blank.html')
