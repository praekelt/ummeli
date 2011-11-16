from ummeli.vlive.forms import (PersonalDetailsForm, ContactDetailsForm,
                                EducationDetailsForm, CertificateForm,
                                WorkExperienceForm, LanguageForm, ReferenceForm)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_control

from ummeli.base.models import (Certificate,  WorkExperience,  Language,
                                                    Reference)

import uuid
from django.core import mail

from django.views.generic import list_detail, create_update
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView,  DeleteView,  CreateView

from ummeli.vlive.views import edit as edit_view
from ummeli.vlive.utils import pin_required

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

    return render_to_response('edit_details.html',
                            {'form': form, 'page_title': page_title},
                            context_instance=RequestContext(request))

def redirect_pml(request,  redirect_url):
    return render_to_response('redirect.html',
                              {'redirect_url': redirect_url + '?' + str(uuid.uuid4()),
                              'redirect_time': 10,
                              'redirect_message': 'Thanks! Your information has been updated.'},
                            context_instance=RequestContext(request))

def delete_and_redirect_pml(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect_pml(self.request,  self.get_success_url())

@login_required
@pin_required
@cache_control(no_cache=True)
def personal_details(request):
    return process_edit_request(request, PersonalDetailsForm,
                                                'personal details')

@login_required
@pin_required
@cache_control(no_cache=True)
def contact_details(request):
    return process_edit_request(request, ContactDetailsForm,
                                                'contact details')

@login_required
@pin_required
@cache_control(no_cache=True)
def education_details(request):
    return process_edit_request(request, EducationDetailsForm,
                                                'education details')

class CertificateListView(ListView):

    def get_context_data(self, **kwargs):
        context = super(CertificateListView, self).get_context_data(**kwargs)
        context['list_name'] = 'certificates'
        context['page_title'] = 'Qualifications'
        return context

    def get_queryset(self):
        return self.request.user.get_profile().certificates.all()

    def render_to_response(self, context, **kwargs):
        self.template_name = 'list_objects.html'
        
        return super(CertificateListView, self).render_to_response(context, **kwargs)

class CertificateEditView(UpdateView):
    model = Certificate
    form_class = CertificateForm

    def get_success_url(self):
        return reverse("certificate_list")

    def get_context_data(self, **kwargs):
        context = super(CertificateEditView, self).get_context_data(**kwargs)
        context['list_name'] = 'certificates'
        context['page_title'] = 'Qualification'
        context['cancel_url'] = reverse("certificate_list")
        return context

    def render_to_response(self, context, **kwargs):
        self.template_name = 'edit_object.html'
        return super(CertificateEditView, self).render_to_response(context, **kwargs)

    def form_valid(self, form):
        form.save()
        return redirect_pml(self.request,  self.get_success_url())

class CertificateCreateView(CreateView):
    model = Certificate
    form_class = CertificateForm

    def get_success_url(self):
        return reverse("certificate_list")

    def get_context_data(self, **kwargs):
        context = super(CertificateCreateView, self).get_context_data(**kwargs)
        context['list_name'] = 'certificates'
        context['page_title'] = 'Qualifications'
        context['cancel_url'] = reverse("certificate_list")
        return context

    def form_valid(self, form):
        new_cert = form.save()
        self.request.user.get_profile().certificates.add(new_cert)
        return redirect_pml(self.request,  self.get_success_url())

    def render_to_response(self, context, **kwargs):
        self.template_name = 'edit_object.html'
        return super(CertificateCreateView, self).render_to_response(context, **kwargs)

class CertificateDeleteView(DeleteView):
    model = Certificate

    def get_success_url(self):
        return reverse("certificate_list")

    def get_context_data(self, **kwargs):
        context = super(CertificateDeleteView, self).get_context_data(**kwargs)
        context['list_name'] = 'certificates'
        context['cancel_url'] = reverse("certificate_list")
        return context

    def render_to_response(self, context, **kwargs):
        self.template_name = 'delete.html'
        
        return super(CertificateDeleteView, self).render_to_response(context, **kwargs)

    def delete(self, request, *args, **kwargs):
        return delete_and_redirect_pml(self, request, args, kwargs)

class WorkExperienceListView(ListView):

    def get_context_data(self, **kwargs):
        context = super(WorkExperienceListView, self).get_context_data(**kwargs)
        context['list_name'] = 'work_experiences'
        context['page_title'] = 'Work Experiences'
        return context

    def get_queryset(self):
        return self.request.user.get_profile().work_experiences.all()

    def render_to_response(self, context, **kwargs):
        self.template_name = 'list_objects.html'
        return super(WorkExperienceListView, self).render_to_response(context, **kwargs)

class WorkExperienceEditView(UpdateView):
    model = WorkExperience
    form_class = WorkExperienceForm

    def get_success_url(self):
        return reverse("work_experience_list")

    def get_context_data(self, **kwargs):
        context = super(WorkExperienceEditView, self).get_context_data(**kwargs)
        context['list_name'] = 'work_experiences'
        context['page_title'] = 'Work Experience'
        context['cancel_url'] = reverse("work_experience_list")
        return context

    def form_valid(self, form):
        form.save()
        return redirect_pml(self.request,  self.get_success_url())

    def render_to_response(self, context, **kwargs):
        self.template_name = 'edit_object.html'
        return super(WorkExperienceEditView, self).render_to_response(context, **kwargs)

class WorkExperienceCreateView(CreateView):
    model = WorkExperience
    form_class = WorkExperienceForm

    def get_success_url(self):
        return reverse("work_experience_list")

    def get_context_data(self, **kwargs):
        context = super(WorkExperienceCreateView, self).get_context_data(**kwargs)
        context['list_name'] = 'work_experiences'
        context['page_title'] = 'Work Experience'
        context['cancel_url'] = reverse("work_experience_list")
        return context

    def form_valid(self, form):
        new_workExperience = form.save()
        self.request.user.get_profile().work_experiences.add(new_workExperience)
        return redirect_pml(self.request,  self.get_success_url())

    def render_to_response(self, context, **kwargs):
        self.template_name = 'edit_object.html'
        return super(WorkExperienceCreateView, self).render_to_response(context, **kwargs)

class WorkExperienceDeleteView(DeleteView):
    model = WorkExperience

    def get_success_url(self):
        return reverse("work_experience_list")

    def get_context_data(self, **kwargs):
        context = super(WorkExperienceDeleteView, self).get_context_data(**kwargs)
        context['list_name'] = 'work_experiences'
        context['cancel_url'] = reverse("work_experience_list")
        return context

    def delete(self, request, *args, **kwargs):
        return delete_and_redirect_pml(self, request, args, kwargs)

    def render_to_response(self, context, **kwargs):
        self.template_name = 'delete.html'
        return super(WorkExperienceDeleteView, self).render_to_response(context, **kwargs)

class LanguageListView(ListView):

    def get_context_data(self, **kwargs):
        context = super(LanguageListView, self).get_context_data(**kwargs)
        context['list_name'] = 'languages'
        context['page_title'] = 'Languages'
        return context

    def get_queryset(self):
        return self.request.user.get_profile().languages.all()

    def render_to_response(self, context, **kwargs):
        self.template_name = 'list_objects.html'
        return super(LanguageListView, self).render_to_response(context, **kwargs)


class LanguageEditView(UpdateView):
    model = Language
    form_class = LanguageForm

    def get_success_url(self):
        return reverse("language_list")

    def get_context_data(self, **kwargs):
        context = super(LanguageEditView, self).get_context_data(**kwargs)
        context['list_name'] = 'languages'
        context['page_title'] = 'Language'
        context['cancel_url'] = reverse("language_list")
        return context

    def form_valid(self, form):
        form.save()
        return redirect_pml(self.request,  self.get_success_url())

    def render_to_response(self, context, **kwargs):
        self.template_name = 'edit_object.html'
        return super(LanguageEditView, self).render_to_response(context, **kwargs)


class LanguageCreateView(CreateView):
    model = Language
    form_class = LanguageForm

    def get_success_url(self):
        return reverse("language_list")

    def get_context_data(self, **kwargs):
        context = super(LanguageCreateView, self).get_context_data(**kwargs)
        context['list_name'] = 'languages'
        context['page_title'] = 'Language'
        context['cancel_url'] = reverse("language_list")
        return context

    def form_valid(self, form):
        new_language = form.save()
        self.request.user.get_profile().languages.add(new_language)
        return redirect_pml(self.request,  self.get_success_url())

    def render_to_response(self, context, **kwargs):
        self.template_name = 'edit_object.html'
        return super(LanguageCreateView, self).render_to_response(context, **kwargs)


class LanguageDeleteView(DeleteView):
    model = Language

    def get_success_url(self):
        return reverse("language_list")

    def get_context_data(self, **kwargs):
        context = super(LanguageDeleteView, self).get_context_data(**kwargs)
        context['list_name'] = 'languages'
        context['cancel_url'] = reverse("language_list")
        return context

    def delete(self, request, *args, **kwargs):
        return delete_and_redirect_pml(self, request, args, kwargs)

    def render_to_response(self, context, **kwargs):
        self.template_name = 'delete.html'
        return super(LanguageDeleteView, self).render_to_response(context, **kwargs)

class ReferenceListView(ListView):

    def get_context_data(self, **kwargs):
        context = super(ReferenceListView, self).get_context_data(**kwargs)
        context['list_name'] = 'references'
        context['page_title'] = 'References'
        return context

    def get_queryset(self):
        return self.request.user.get_profile().references.all()

    def render_to_response(self, context, **kwargs):
        self.template_name = 'list_objects.html'
        return super(ReferenceListView, self).render_to_response(context, **kwargs)


class ReferenceEditView(UpdateView):
    model = Reference
    form_class = ReferenceForm

    def get_success_url(self):
        return reverse("reference_list")

    def get_context_data(self, **kwargs):
        context = super(ReferenceEditView, self).get_context_data(**kwargs)
        context['list_name'] = 'references'
        context['page_title'] = 'Reference'
        context['cancel_url'] = reverse("reference_list")
        return context

    def form_valid(self, form):
        form.save()
        return redirect_pml(self.request,  self.get_success_url())

    def render_to_response(self, context, **kwargs):
        self.template_name = 'edit_object.html'
        return super(ReferenceEditView, self).render_to_response(context, **kwargs)


class ReferenceCreateView(CreateView):
    model = Reference
    form_class = ReferenceForm

    def get_success_url(self):
        return reverse("reference_list")

    def get_context_data(self, **kwargs):
        context = super(ReferenceCreateView, self).get_context_data(**kwargs)
        context['list_name'] = 'references'
        context['page_title'] = 'Reference'
        context['cancel_url'] = reverse("reference_list")
        return context

    def form_valid(self, form):
        new_reference = form.save()
        self.request.user.get_profile().references.add(new_reference)
        return redirect_pml(self.request,  self.get_success_url())

    def render_to_response(self, context, **kwargs):
        self.template_name = 'edit_object.html'
        return super(ReferenceCreateView, self).render_to_response(context, **kwargs)


class ReferenceDeleteView(DeleteView):
    model = Reference

    def get_success_url(self):
        return reverse("reference_list")

    def get_context_data(self, **kwargs):
        context = super(ReferenceDeleteView, self).get_context_data(**kwargs)
        context['list_name'] = 'references'
        context['cancel_url'] = reverse("reference_list")
        return context

    def delete(self, request, *args, **kwargs):
        return delete_and_redirect_pml(self, request, args, kwargs)

    def render_to_response(self, context, **kwargs):
        self.template_name = 'delete.html'
        return super(ReferenceDeleteView, self).render_to_response(context, **kwargs)
