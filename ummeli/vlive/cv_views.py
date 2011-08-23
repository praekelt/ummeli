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
def certificate_details(request, pk_id = None):
    page_title = 'certificate'
    redirect_url = ('%s/%s' % (reverse('vlive:edit'),'certificates'))
    list_items = request.user.get_profile().certificates
    return process_edit_list_items(request, CertificateForm, list_items,
                                    page_title, redirect_url, pk_id,
                                    'vlive/edit_list_item.html')
    
def process_edit_list_items(request, model_form, list_items, page_title,
                            redirect_url, pk_id, template_name):
    if request.method == 'POST':
        cancel = request.POST.get('cancel', None)
        if cancel:
            return HttpResponseRedirect(redirect_url)
        
        delete = request.POST.get('delete', None)
        if delete:
            if pk_id:
                list_items.get(pk = pk_id).delete()
            return HttpResponseRedirect(redirect_url)
        
        post_action = request.POST.get('action', None)
        if post_action == 'edit':
            print pk_id
            form = model_form(request.POST, 
                                instance = list_items.get(pk = pk_id))
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(redirect_url)
        else:
            form = model_form(request.POST)
            action = 'add'
            if form.is_valid():
                new_form = form.save()
                list_items.add(new_form)
                return HttpResponseRedirect(redirect_url)        
    elif pk_id:
        form = model_form(instance = list_items.get(pk = pk_id))
        action = 'edit'
    else:
        form = model_form()
        action = 'create'
    
    return render_to_response(template_name, 
                            {'form': form, 'page_title': page_title,
                            'action': action},
                            context_instance=RequestContext(request))
