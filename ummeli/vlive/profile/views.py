from django.contrib.auth.models import User
from ummeli.vlive.forms import (PersonalDetailsForm, ContactDetailsForm,
                                EducationDetailsForm, CertificateForm,
                                WorkExperienceForm, LanguageForm, 
                                ReferenceForm, SkillForm)
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,  render
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView,  DeleteView,  CreateView
from django.http import Http404

from ummeli.base.models import (Certificate,  WorkExperience,  Language,
                                Reference,  CurriculumVitae, Skill)
from ummeli.graphing.models import Person
from ummeli.vlive.utils import pin_required
from ummeli.graphing.utils import add_connection_for_user

from jmbowordsuggest.models import AcceptedWord, AcceptedWordCategory
from jmbowordsuggest.utils import suggest_words

@login_required
@pin_required
def profile(request):
    user_node = Person.get_and_update(request.user)
    num_connections = len(user_node.connections())
    return render(request, 'profile/profile.html', {'num_connections': num_connections})

@login_required
@pin_required
def profile_view(request, user_id):
    user_node = Person.get_and_update(request.user)
    other_user = get_object_or_404(User, pk=user_id)
    other_user_node = Person.get_and_update(other_user)
    num_connections = len(other_user_node.connections())
    
    already_requested = other_user.get_profile().is_connection_requested(request.user.pk)
    connection_requested = request.user.get_profile().is_connection_requested(user_id)
    return render(request, 'profile/profile_view.html', 
                {'other_user_profile': other_user.get_profile(),
                 'other_user_pk':other_user.pk,
                 'num_connections': num_connections,
                 'connected_to_user': user_node.is_connected_to(other_user_node),
                 'is_self': int(user_id) == request.user.pk,
                 'already_requested':already_requested,
                 'connection_requested':connection_requested,
                 })

@login_required
@pin_required
def connections(request, user_id):
    other_user = get_object_or_404(User, pk = user_id)
    other_user_node = Person.get_and_update(other_user)
    
    user_node = Person.get_and_update(request.user)
    connections = [(node, user_node.is_connected_to(node), \
                    request.user.connection_requests.filter(user__pk=node.user_id).exists(), \
                    request.user.get_profile().is_connection_requested(node.user_id)) \
                   for node in other_user_node.connections()]
                   
    already_requested = other_user.get_profile().connection_requests.filter(pk=request.user.pk).exists()
    return render(request, 'profile/connections.html', 
                {'user_node': user_node,
                 'other_user_node': other_user_node,
                 'connections': connections,
                 'is_self': int(user_id) == request.user.pk,
                 'already_requested':already_requested,
                 })

@login_required
@pin_required
def add_connection(request, user_id):
    if request.user.pk == user_id: #don't allow user to add themself as a connection
        redirect(reverse('profile'))
    
    user = get_object_or_404(User, pk = user_id)
    profile = user.get_profile()
    
    if request.method == 'POST':        
        profile.connection_requests.add(request.user)
        
        redirect_to = request.POST.get('next', reverse('profile'))
        return redirect(redirect_to)
    
    next = request.GET.get('next', reverse('profile'))
    return render(request, 'profile/add_connection.html',
                            {'other_user_profile': profile,
                             'other_user_pk':user.pk,
                             'next':next})

@login_required
@pin_required
def confirm_request(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    profile = user.get_profile()
    
    if not request.user.get_profile().connection_requests.filter(pk=user_id).exists():
        raise Http404
        
    if request.method == 'POST':        
        add_connection_for_user(user, request.user)
        request.user.get_profile().connection_requests.remove(user)
        redirect_to = request.POST.get('next', reverse('profile'))
        return redirect(redirect_to)
    
    next = request.GET.get('next', reverse('profile'))
    return render(request, 'profile/confirm_request.html',
                            {'other_user_profile': profile,
                             'other_user_pk':user.pk,
                             'next':next})

@login_required
@pin_required
def reject_request(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    profile = user.get_profile()
    profile.connection_requests.remove(request.user)
    
    if not request.user.get_profile().connection_requests.filter(pk=user_id).exists():
        raise Http404
        
    if request.method == 'POST':
        request.user.get_profile().connection_requests.remove(user)
        redirect_to = request.POST.get('next', reverse('profile'))
        return redirect(redirect_to)
    
    next = request.GET.get('next', reverse('profile'))
    return render(request, 'profile/reject_request.html',
                            {'other_user_profile': profile,
                             'other_user_pk':user.pk,
                             'next':next})
                             
                             
@login_required
@pin_required
def connection_requests(request):
    return render(request, 'profile/connection_requests.html',
                            {'requests': request.user.get_profile().connection_requests.all()})

@login_required
@pin_required
def edit_basic(request):
    return render(request, 'profile/profile_personal_details.html')

@login_required
@pin_required
def edit_personal(request):
    return render(request, 'profile/profile_personal_details.html')

def process_edit_request(request, model_form, page_title):
    cv = request.user.get_profile()
    if request.method == 'POST':
        cancel = request.POST.get('cancel', None)
        if cancel:
            return edit_basic(request)
        else:
            form = model_form(request.POST, instance=cv)
            if form.is_valid():
                form.save()
                return redirect(reverse('edit_basic'))
    else:
        form = model_form(instance=cv)

    return render(request, 'profile/edit_details.html',
                            {'form': form, 'page_title': page_title})

@login_required
@pin_required
def personal_details(request):
    return process_edit_request(request, PersonalDetailsForm,
                                                'Personal details')

@login_required
@pin_required
def contact_details(request):
    return process_edit_request(request, ContactDetailsForm,
                                                'Contact details')

@login_required
@pin_required
def education_details(request):
    return process_edit_request(request, EducationDetailsForm,
                                                'Education details')

class PersonalDetailsEditView(UpdateView):
    model = CurriculumVitae
    form_class = PersonalDetailsForm
    template_name = 'profile/personal_details.html'

    def get_success_url(self):
        return reverse("edit_basic")
        
    def get_object(self,  queryset=None):
        return self.request.user.get_profile()

class CertificateListView(ListView):

    def get_context_data(self, **kwargs):
        context = super(CertificateListView, self).get_context_data(**kwargs)
        context['list_name'] = 'certificates'
        context['page_title'] = 'Qualifications'
        return context

    def get_queryset(self):
        return self.request.user.get_profile().certificates.all()

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/list_objects.html'
        
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
        self.template_name = 'profile/edit_object.html'
        return super(CertificateEditView, self).render_to_response(context, **kwargs)

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
        return redirect(self.get_success_url())

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/edit_object.html'
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
        self.template_name = 'profile/delete.html'
        
        return super(CertificateDeleteView, self).render_to_response(context, **kwargs)

class WorkExperienceListView(ListView):

    def get_context_data(self, **kwargs):
        context = super(WorkExperienceListView, self).get_context_data(**kwargs)
        context['list_name'] = 'work_experiences'
        context['page_title'] = 'Work Experiences'
        return context

    def get_queryset(self):
        return self.request.user.get_profile().work_experiences.all()

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/list_objects.html'
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

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/edit_object.html'
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
        return redirect(self.get_success_url())

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/edit_object.html'
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

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/delete.html'
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
        self.template_name = 'profile/list_objects.html'
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

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/edit_object.html'
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
        return redirect(self.get_success_url())

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/edit_object.html'
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

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/delete.html'
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
        self.template_name = 'profile/list_objects.html'
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

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/edit_object.html'
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
        return redirect(self.get_success_url())

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/edit_object.html'
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

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/delete.html'
        return super(ReferenceDeleteView, self).render_to_response(context, **kwargs)

class SkillListView(ListView):

    def get_context_data(self, **kwargs):
        context = super(SkillListView, self).get_context_data(**kwargs)
        context['list_name'] = 'skills'
        context['page_title'] = 'Skills'
        return context

    def get_queryset(self):
        return self.request.user.get_profile().skills.all()

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/list_skills.html'
        return super(SkillListView, self).render_to_response(context, **kwargs)


class SkillDeleteView(DeleteView):
    model = Skill

    def get_success_url(self):
        return reverse("skills")

    def get_context_data(self, **kwargs):
        context = super(SkillDeleteView, self).get_context_data(**kwargs)
        context['list_name'] = 'skills'
        context['cancel_url'] = reverse("skills")
        return context

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/delete.html'
        return super(SkillDeleteView, self).render_to_response(context, **kwargs)


@login_required
@pin_required
def add_skill(request):
    existing_skills = request.user.get_profile().skills.all()
    skills = AcceptedWordCategory.objects.get(name='skills')\
            .words.exclude(word__in = [skill.skill for skill in existing_skills])
    return render(request, 'profile/skills_0.html',
                            {'skills': skills})

@login_required
@pin_required
def add_skill_from_list(request, skill_id):
    word = get_object_or_404(AcceptedWord, pk = skill_id) #Get word from list of skills
    profile = request.user.get_profile()
        
    if request.method == 'POST':
        if not profile.skills.filter(skill=word.word).exists():
            skill = Skill(skill=word.word)
            skill.save()
            
            profile.skills.add(skill)
            return redirect(reverse('skills'))
        else:
            return render(request, 'profile/skill_duplicate.html',
                            {'skill': word.word})
    
    return render(request, 'profile/skill_from_list_confirm.html',
                            {'skill': word.word})
