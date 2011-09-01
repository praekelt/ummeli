from ummeli.vlive.forms import (PersonalDetailsForm, ContactDetailsForm,
                                EducationDetailsForm, CertificateForm, 
                                WorkExperienceForm, LanguageForm, ReferenceForm)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from ummeli.vlive.utils import render_to_pdf
from ummeli.api.models import Certificate,  WorkExperience

from django.core import mail

from django.views.generic import list_detail, create_update
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView,  DeleteView,  CreateView

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
            action = 'edit'
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

def render_item_list(request, items, page_title, list_name):
    return render_to_response('vlive/item_list.html', 
                            {'items': items, 'page_title': page_title, 
                            'list_name': list_name},
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

class CertificateListView(ListView):
    template_name = 'vlive/list_objects.html'
    
    def get_context_data(self, **kwargs):
        context = super(CertificateListView, self).get_context_data(**kwargs)
        context['list_name'] = 'certificates'
        context['page_title'] = 'certificates'
        return context
        
    def get_queryset(self):
        return self.request.user.get_profile().certificates.all()
        
class CertificateEditView(UpdateView):
    model=Certificate
    template_name = 'vlive/edit_object.html'
    
    def get_success_url(self):
        return reverse("vlive:certificate_list")
        
    def get_context_data(self, **kwargs):
        context = super(CertificateEditView, self).get_context_data(**kwargs)
        context['list_name'] = 'certificates'
        context['page_title'] = 'certificate'
        context['cancel_url'] = reverse("vlive:certificate_list")
        return context
    
class CertificateCreateView(CreateView):
    model=Certificate
    template_name = 'vlive/edit_object.html'
    
    def get_success_url(self):
        return reverse("vlive:certificate_list")
        
    def get_context_data(self, **kwargs):
        context = super(CertificateCreateView, self).get_context_data(**kwargs)
        context['list_name'] = 'certificates'
        context['page_title'] = 'certificate'
        context['cancel_url'] = reverse("vlive:certificate_list")
        return context
    
    def form_valid(self, form):
        new_cert = form.save()
        self.request.user.get_profile().certificates.add(new_cert)
        return HttpResponseRedirect(self.get_success_url())

class CertificateDeleteView(DeleteView):
    model=Certificate
    template_name = 'vlive/delete.html'
    
    def get_success_url(self):
        return reverse("vlive:certificate_list")
        
    def get_context_data(self, **kwargs):
        context = super(CertificateDeleteView, self).get_context_data(**kwargs)
        context['list_name'] = 'certificates'
        context['cancel_url'] = reverse("vlive:certificate_list")
        return context
        
        
class WorkExperienceListView(ListView):
    template_name = 'vlive/list_objects.html'
    
    def get_context_data(self, **kwargs):
        context = super(WorkExperienceListView, self).get_context_data(**kwargs)
        context['list_name'] = 'workExperiences'
        context['page_title'] = 'work experiences'
        return context
        
    def get_queryset(self):
        return self.request.user.get_profile().workExperiences.all()
        
        
class WorkExperienceEditView(UpdateView):
    model=WorkExperience
    template_name = 'vlive/edit_object.html'
    
    def get_success_url(self):
        return reverse("vlive:workExperience_list")
        
    def get_context_data(self, **kwargs):
        context = super(WorkExperienceEditView, self).get_context_data(**kwargs)
        context['list_name'] = 'workExperiences'
        context['page_title'] = 'work experience'
        context['cancel_url'] = reverse("vlive:workExperience_list")
        return context
    
    
class WorkExperienceCreateView(CreateView):
    model=WorkExperience
    template_name = 'vlive/edit_object.html'
    
    def get_success_url(self):
        return reverse("vlive:workExperience_list")
        
    def get_context_data(self, **kwargs):
        context = super(WorkExperienceCreateView, self).get_context_data(**kwargs)
        context['list_name'] = 'workExperiences'
        context['page_title'] = 'work experience'
        context['cancel_url'] = reverse("vlive:workExperience_list")
        return context
    
    def form_valid(self, form):
        new_workExperience = form.save()
        self.request.user.get_profile().workExperiences.add(new_workExperience)
        return HttpResponseRedirect(self.get_success_url())


class WorkExperienceDeleteView(DeleteView):
    model=WorkExperience
    template_name = 'vlive/delete.html'
    
    def get_success_url(self):
        return reverse("vlive:workExperience_list")
        
    def get_context_data(self, **kwargs):
        context = super(WorkExperienceDeleteView, self).get_context_data(**kwargs)
        context['list_name'] = 'workExperiences'
        context['cancel_url'] = reverse("vlive:workExperience_list")
        return context
        
@login_required
def languages_details(request):
    cv = request.user.get_profile()
    return render_item_list(request, cv.languages, 'languages', 
                            'languages')

@login_required
def language_details(request, pk_id = None):
    page_title = 'languages'
    redirect_url = ('%s/%s' % (reverse('vlive:edit'),'languages'))
    list_items = request.user.get_profile().languages
    return process_edit_list_items(request, LanguageForm, list_items,
                                    page_title, redirect_url, pk_id,
                                    'vlive/edit_list_item.html')
                                    
@login_required
def references_details(request):
    cv = request.user.get_profile()
    return render_item_list(request, cv.references, 'references', 
                            'references')

@login_required
def reference_details(request, pk_id = None):
    page_title = 'references'
    redirect_url = ('%s/%s' % (reverse('vlive:edit'),'references'))
    list_items = request.user.get_profile().references
    return process_edit_list_items(request, ReferenceForm, list_items,
                                    page_title, redirect_url, pk_id,
                                    'vlive/edit_list_item.html')
                                    
                                    
