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
from django.views.decorators.cache import cache_control

from ummeli.vlive.utils import render_to_pdf
from ummeli.api.models import (Certificate,  WorkExperience,  Language,  
                                                    Reference)

from django.core import mail

from django.views.generic import list_detail, create_update
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView,  DeleteView,  CreateView

from ummeli.vlive.views import edit as edit_view

@csrf_protect
@cache_control(no_cache=True)
def process_edit_request(request, model_form, page_title):
    cv = request.user.get_profile()
    if request.method == 'POST':
        cancel = request.POST.get('cancel', None)
        if cancel:
            return edit_view(request)
        else:
            form = model_form(request.POST, instance=cv)
            if form.is_valid():
                form.save()
                return edit_view(request)
    else:
        form = model_form(instance=cv)
        
    return render_to_response('pml/edit_details.xml',
                            {'form': form, 'page_title': page_title},
                            context_instance=RequestContext(request), 
                            mimetype = 'text/xml')
    
@login_required
@cache_control(no_cache=True)
@csrf_protect
def personal_details(request):
    return process_edit_request(request, PersonalDetailsForm, 
                                                'personal details')

@login_required
@cache_control(no_cache=True)
@csrf_protect
def contact_details(request):
    return process_edit_request(request, ContactDetailsForm, 
                                                'contact details')

@login_required
@cache_control(no_cache=True)
@csrf_protect
def education_details(request):
    return process_edit_request(request, EducationDetailsForm, 
                                                'education details')

class CertificateListView(ListView):
    template_name = 'pml/list_objects.xml'
    
    def get_context_data(self, **kwargs):
        context = super(CertificateListView, self).get_context_data(**kwargs)
        context['list_name'] = 'certificates'
        context['page_title'] = 'certificates'
        return context
        
    def get_queryset(self):
        return self.request.user.get_profile().certificates.all()
        
    def render_to_response(self, context, **kwargs):
        return super(CertificateListView, self).render_to_response(context,
                        content_type='text/xml', **kwargs)
        
class CertificateEditView(UpdateView):
    model = Certificate
    template_name = 'pml/edit_object.xml'
    form_class = CertificateForm
    
    def get_success_url(self):
        return reverse("certificate_list")
        
    def get_context_data(self, **kwargs):
        context = super(CertificateEditView, self).get_context_data(**kwargs)
        context['list_name'] = 'certificates'
        context['page_title'] = 'certificate'
        context['cancel_url'] = reverse("certificate_list")
        return context
        
    def render_to_response(self, context, **kwargs):
        return super(CertificateEditView, self).render_to_response(context,
                        content_type='text/xml', **kwargs)
    
class CertificateCreateView(CreateView):
    model = Certificate
    template_name = 'pml/edit_object.xml'
    form_class = CertificateForm
    
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
        
    def render_to_response(self, context, **kwargs):
        return super(CertificateCreateView, self).render_to_response(context,
                        content_type='text/xml', **kwargs)

class CertificateDeleteView(DeleteView):
    model = Certificate
    template_name = 'pml/delete.xml'
    
    def get_success_url(self):
        return reverse("certificate_list")
        
    def get_context_data(self, **kwargs):
        context = super(CertificateDeleteView, self).get_context_data(**kwargs)
        context['list_name'] = 'certificates'
        context['cancel_url'] = reverse("certificate_list")
        return context
    
    def render_to_response(self, context, **kwargs):
        return super(CertificateDeleteView, self).render_to_response(context,
                        content_type='text/xml', **kwargs)
        
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
