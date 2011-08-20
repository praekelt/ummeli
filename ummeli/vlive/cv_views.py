from ummeli.vlive.forms import (PersonalDetailsForm, ContactDetailsForm,
                                EducationDetailsForm)
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
                            {'form': form, 'page_title': page_title},
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