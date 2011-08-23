from ummeli.vlive.forms import (PersonalDetailsForm, ContactDetailsForm,
                                EducationDetailsForm, CertificatesDetailsForm,
                                CertificateForm)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def process_edit_request(request, model_form, page_title):
    cv = request.user.get_profile()
    if request.method == 'POST':
        cancel = request.POST.get('cancel', None)
        if cancel:
            return HttpResponseRedirect(reverse('vlive:edit'))
        else:
            form = model_form(request.POST, instance=cv)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('vlive:edit'))
    else:
        form = model_form(instance=cv)
        
    return render_to_response('vlive/edit_details.html', 
                            {'form': form, 'page_title': page_title,
                            'method': 'post'},
                            context_instance=RequestContext(request))
                            
@login_required
def personal_details(request):
    return process_edit_request(request, PersonalDetailsForm, 'personal details')

@login_required
def contact_details(request):
    return process_edit_request(request, ContactDetailsForm, 'contact details')

@login_required
def education_details(request):
    return process_edit_request(request, EducationDetailsForm, 'education details')

def render_item_list(request, items, page_title, list_name):
    return render_to_response('vlive/item_list.html', 
                            {'items': items, 'page_title': page_title, 
                            'list_name': list_name},
                            context_instance=RequestContext(request))

@login_required
def certificates_details(request):
    cv = request.user.get_profile()
    return render_item_list(request, cv.certificates, 'certificates', 
                            'certificates')

@login_required
def certificate_details(request, cert_pk = None):
    page_title = 'certificate'
    cv = request.user.get_profile()
    certificates_url = ('%s/%s' % (reverse('vlive:edit'),'certificates'))
    
    if request.method == 'POST':
        cancel = request.POST.get('cancel', None)
        if cancel:
            return HttpResponseRedirect(certificates_url)
        
        delete = request.POST.get('delete', None)
        if delete:
            if cert_pk:
                cv.certificates.get(pk = cert_pk).delete()
            return HttpResponseRedirect(certificates_url)
        
        post_action = request.POST.get('action', None)
        if post_action == 'edit':
            print cert_pk
            form = CertificateForm(request.POST, 
                                instance = cv.certificates.get(pk = cert_pk))
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(certificates_url)
        else:
            form = CertificateForm(request.POST)
            action = 'add'
            if form.is_valid():
                new_form = form.save()
                cv.certificates.add(new_form)
                return HttpResponseRedirect(certificates_url)        
    elif cert_pk:
        form = CertificateForm(instance = cv.certificates.get(pk = cert_pk))
        action = 'edit'
    else:
        form = CertificateForm()
        action = 'create'
    
    return render_to_response('vlive/edit_list_item.html', 
                            {'form': form, 'page_title': page_title,
                            'action': action},
                            context_instance=RequestContext(request))
