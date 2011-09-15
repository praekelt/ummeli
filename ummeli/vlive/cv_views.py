from ummeli.vlive.forms import (PersonalDetailsForm, ContactDetailsForm,
                                EducationDetailsForm, CertificateForm, 
                                WorkExperienceForm, LanguageForm, ReferenceForm)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

from ummeli.vlive.utils import render_to_pdf
from ummeli.api.models import (Certificate,  WorkExperience,  Language,  
                                                    Reference)

from django.core import mail

from django.views.generic import list_detail, create_update
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView,  DeleteView,  CreateView

from ummeli.vlive.views import edit as edit_view

@csrf_protect
def process_edit_request(request, model_form, page_title,  cancel_url):
    cv = request.user.get_profile()
    form = model_form(instance=cv)
    
    form_name = ''
    if(model_form == PersonalDetailsForm):
        form_name = 'personal_details'
    elif (model_form == ContactDetailsForm):
        form_name = 'contact_details'
    else:
        form_name = 'education_details'
        
    return render_to_response('pml/edit_details.xml', 
                            {'form': form, 'page_title': page_title,
                            'method': 'post',  'cancel_url': cancel_url, 
                            'form_name': form_name},
                            context_instance = RequestContext(request), 
                            mimetype = 'text/xml')

@csrf_protect
def process_edit_request_post(request):
    cv = request.user.get_profile()
    
    form_name = request.GET.get('form_name', None)
    cancel_url = request.GET.get('cancel_url',  None)
    
    model_form = None
    page_title = None
    
    if(form_name == 'personal_details'):
        model_form = PersonalDetailsForm
        page_title = 'personal details'
    elif(form_name == 'contact_details'):
        model_form = ContactDetailsForm
        page_title = 'contact details'
    else:
        model_form = EducationDetailsForm
        page_title = 'education details'
        
    form = model_form(request.GET, instance=cv)
    
    if form.is_valid():
        form.save()
        return edit_view(request)
        
    return render_to_response('pml/edit_details.xml', 
                            {'form': form, 'page_title': page_title, 
                            'cancel_url': cancel_url},
                            context_instance = RequestContext(request), 
                            mimetype = 'text/xml')
    
@login_required
def personal_details(request):
    return process_edit_request(request, PersonalDetailsForm, 
                                                'personal details', 
                                                reverse('edit_personal'))

@login_required
def contact_details(request):
    return process_edit_request(request, ContactDetailsForm, 
                                                'contact details', 
                                                reverse('edit_contact'))

@login_required
def education_details(request):
    return process_edit_request(request, EducationDetailsForm, 
                                                'education details',  
                                                reverse('edit_education'))

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
    model = Certificate
    template_name = 'vlive/edit_object.html'
    
    def get_success_url(self):
        return reverse("certificate_list")
        
    def get_context_data(self, **kwargs):
        context = super(CertificateEditView, self).get_context_data(**kwargs)
        context['list_name'] = 'certificates'
        context['page_title'] = 'certificate'
        context['cancel_url'] = reverse("certificate_list")
        return context
    
class CertificateCreateView(CreateView):
    model = Certificate
    template_name = 'vlive/edit_object.html'
    
    def get_success_url(self):
        return reverse("certificate_list")
        
    def get_context_data(self, **kwargs):
        context = super(CertificateCreateView, self).get_context_data(**kwargs)
        context['list_name'] = 'certificates'
        context['page_title'] = 'certificate'
        context['cancel_url'] = reverse("certificate_list")
        return context
    
    def form_valid(self, form):
        new_cert = form.save()
        self.request.user.get_profile().certificates.add(new_cert)
        return HttpResponseRedirect(self.get_success_url())

class CertificateDeleteView(DeleteView):
    model = Certificate
    template_name = 'vlive/delete.html'
    
    def get_success_url(self):
        return reverse("certificate_list")
        
    def get_context_data(self, **kwargs):
        context = super(CertificateDeleteView, self).get_context_data(**kwargs)
        context['list_name'] = 'certificates'
        context['cancel_url'] = reverse("certificate_list")
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
    model = WorkExperience
    template_name = 'vlive/edit_object.html'
    
    def get_success_url(self):
        return reverse("workExperience_list")
        
    def get_context_data(self, **kwargs):
        context = super(WorkExperienceEditView, self).get_context_data(**kwargs)
        context['list_name'] = 'workExperiences'
        context['page_title'] = 'work experience'
        context['cancel_url'] = reverse("workExperience_list")
        return context
    
    
class WorkExperienceCreateView(CreateView):
    model = WorkExperience
    template_name = 'vlive/edit_object.html'
    
    def get_success_url(self):
        return reverse("workExperience_list")
        
    def get_context_data(self, **kwargs):
        context = super(WorkExperienceCreateView, self).get_context_data(**kwargs)
        context['list_name'] = 'workExperiences'
        context['page_title'] = 'work experience'
        context['cancel_url'] = reverse("workExperience_list")
        return context
    
    def form_valid(self, form):
        new_workExperience = form.save()
        self.request.user.get_profile().workExperiences.add(new_workExperience)
        return HttpResponseRedirect(self.get_success_url())


class WorkExperienceDeleteView(DeleteView):
    model = WorkExperience
    template_name = 'vlive/delete.html'
    
    def get_success_url(self):
        return reverse("workExperience_list")
        
    def get_context_data(self, **kwargs):
        context = super(WorkExperienceDeleteView, self).get_context_data(**kwargs)
        context['list_name'] = 'workExperiences'
        context['cancel_url'] = reverse("workExperience_list")
        return context
        
        
class LanguageListView(ListView):
    template_name = 'vlive/list_objects.html'
    
    def get_context_data(self, **kwargs):
        context = super(LanguageListView, self).get_context_data(**kwargs)
        context['list_name'] = 'languages'
        context['page_title'] = 'languages'
        return context
        
    def get_queryset(self):
        return self.request.user.get_profile().languages.all()
        
        
class LanguageEditView(UpdateView):
    model = Language
    template_name = 'vlive/edit_object.html'
    
    def get_success_url(self):
        return reverse("language_list")
        
    def get_context_data(self, **kwargs):
        context = super(LanguageEditView, self).get_context_data(**kwargs)
        context['list_name'] = 'languages'
        context['page_title'] = 'language'
        context['cancel_url'] = reverse("language_list")
        return context
    
    
class LanguageCreateView(CreateView):
    model = Language
    template_name = 'vlive/edit_object.html'
    
    def get_success_url(self):
        return reverse("language_list")
        
    def get_context_data(self, **kwargs):
        context = super(LanguageCreateView, self).get_context_data(**kwargs)
        context['list_name'] = 'languages'
        context['page_title'] = 'language'
        context['cancel_url'] = reverse("language_list")
        return context
    
    def form_valid(self, form):
        new_language = form.save()
        self.request.user.get_profile().languages.add(new_language)
        return HttpResponseRedirect(self.get_success_url())


class LanguageDeleteView(DeleteView):
    model = Language
    template_name = 'vlive/delete.html'
    
    def get_success_url(self):
        return reverse("language_list")
        
    def get_context_data(self, **kwargs):
        context = super(LanguageDeleteView, self).get_context_data(**kwargs)
        context['list_name'] = 'languages'
        context['cancel_url'] = reverse("language_list")
        return context
        
        
class ReferenceListView(ListView):
    template_name = 'vlive/list_objects.html'
    
    def get_context_data(self, **kwargs):
        context = super(ReferenceListView, self).get_context_data(**kwargs)
        context['list_name'] = 'references'
        context['page_title'] = 'references'
        return context
        
    def get_queryset(self):
        return self.request.user.get_profile().references.all()
        
        
class ReferenceEditView(UpdateView):
    model = Reference
    template_name = 'vlive/edit_object.html'
    
    def get_success_url(self):
        return reverse("reference_list")
        
    def get_context_data(self, **kwargs):
        context = super(ReferenceEditView, self).get_context_data(**kwargs)
        context['list_name'] = 'references'
        context['page_title'] = 'reference'
        context['cancel_url'] = reverse("reference_list")
        return context
    
    
class ReferenceCreateView(CreateView):
    model = Reference
    template_name = 'vlive/edit_object.html'
    
    def get_success_url(self):
        return reverse("reference_list")
        
    def get_context_data(self, **kwargs):
        context = super(ReferenceCreateView, self).get_context_data(**kwargs)
        context['list_name'] = 'references'
        context['page_title'] = 'reference'
        context['cancel_url'] = reverse("reference_list")
        return context
    
    def form_valid(self, form):
        new_reference = form.save()
        self.request.user.get_profile().references.add(new_reference)
        return HttpResponseRedirect(self.get_success_url())


class ReferenceDeleteView(DeleteView):
    model = Reference
    template_name = 'vlive/delete.html'
    
    def get_success_url(self):
        return reverse("reference_list")
        
    def get_context_data(self, **kwargs):
        context = super(ReferenceDeleteView, self).get_context_data(**kwargs)
        context['list_name'] = 'references'
        context['cancel_url'] = reverse("reference_list")
        return context
