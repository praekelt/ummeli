from django.contrib.auth.models import User
from ummeli.vlive.forms import (PersonalDetailsForm, ContactDetailsForm,
                                EducationDetailsForm, CertificateForm,
                                WorkExperienceForm, LanguageForm,
                                ReferenceForm, SkillForm,
                                PersonalStatementForm,
                                UserSubmittedJobArticleForm,
                                UserSubmittedJobArticleEditForm)
from ummeli.vlive.profile.forms import IndustrySearchForm,\
                                        ConnectionNameSearchForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,  render
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView,  DeleteView,  CreateView
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ummeli.base.models import (Certificate,  WorkExperience,  Language,
                                Reference,  CurriculumVitae, Skill,
                                UserSubmittedJobArticle,
                                Province,  Category, PROVINCE_CHOICES)
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
                'other_user_jobs': other_user.user_submitted_job_article_user.count(),
                 'other_user_pk':other_user.pk,
                 'num_connections': num_connections,
                 'connected_to_user': user_node.is_connected_to(other_user_node),
                 'is_self': int(user_id) == request.user.pk,
                 'already_requested':already_requested,
                 'connection_requested':connection_requested,
                 })

@login_required
@pin_required
def my_connections(request):
    return render(request, 'profile/my_connections.html')

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
        form = model_form(request.POST, instance=cv)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile'))
    else:
        form = model_form(instance=cv)

    return render(request, 'profile/edit_details.html',
                            {'form': form, 'page_title': page_title})

@login_required
@pin_required
def education_details(request):
    if request.method == 'POST':
        cv = request.user.get_profile()
        form = EducationDetailsForm(request.POST, instance=cv)
        if form.is_valid():
            form.save()
    return redirect(reverse('certificate_list'))

class PersonalDetailsEditView(UpdateView):
    model = CurriculumVitae
    form_class = PersonalDetailsForm
    template_name = 'profile/personal_details.html'

    def get_success_url(self):
        return reverse("profile")

    def get_object(self,  queryset=None):
        return self.request.user.get_profile()

class ContactDetailsEditView(UpdateView):
    model = CurriculumVitae
    form_class = ContactDetailsForm
    template_name = 'profile/contact_details.html'

    def get_success_url(self):
        return reverse("profile")

    def get_object(self,  queryset=None):
        return self.request.user.get_profile()

    def get_context_data(self, **kwargs):
        context = super(ContactDetailsEditView, self).get_context_data(**kwargs)
        context['provinces'] = PROVINCE_CHOICES
        return context

class PersonalStatementEditView(UpdateView):
    model = CurriculumVitae
    form_class = PersonalStatementForm
    template_name = 'profile/personal_statement.html'

    def get_success_url(self):
        return reverse("profile")

    def get_object(self,  queryset=None):
        return self.request.user.get_profile()

class CertificateListView(ListView):

    def get_context_data(self, **kwargs):
        context = super(CertificateListView, self).get_context_data(**kwargs)
        context['list_name'] = 'certificates'
        context['page_title'] = 'Eductaion'
        return context

    def get_queryset(self):
        return self.request.user.get_profile().certificates.all()

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/list_education.html'

        return super(CertificateListView, self).render_to_response(context, **kwargs)

class CertificateEditView(UpdateView):
    model = Certificate
    form_class = CertificateForm

    def get_success_url(self):
        return reverse("certificate_list")

    def get_context_data(self, **kwargs):
        context = super(CertificateEditView, self).get_context_data(**kwargs)
        context['list_name'] = 'certificates'
        context['page_title'] = 'Eductaion'
        context['cancel_url'] = reverse("certificate_list")
        return context

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/edit_education.html'
        return super(CertificateEditView, self).render_to_response(context, **kwargs)

class CertificateCreateView(CreateView):
    model = Certificate
    form_class = CertificateForm

    def get_success_url(self):
        return reverse("certificate_list")

    def get_context_data(self, **kwargs):
        context = super(CertificateCreateView, self).get_context_data(**kwargs)
        context['list_name'] = 'certificates'
        context['page_title'] = 'Eductaion'
        context['cancel_url'] = reverse("certificate_list")
        return context

    def form_valid(self, form):
        new_cert = form.save()
        self.request.user.get_profile().certificates.add(new_cert)
        return redirect(self.get_success_url())

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/edit_education.html'
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
        context['page_title'] = 'Work Experiences'
        context['cancel_url'] = reverse("work_experience_list")
        return context

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/edit_work_experience.html'
        return super(WorkExperienceEditView, self).render_to_response(context, **kwargs)

class WorkExperienceCreateView(CreateView):
    model = WorkExperience
    form_class = WorkExperienceForm

    def get_success_url(self):
        return reverse("work_experience_list")

    def get_context_data(self, **kwargs):
        context = super(WorkExperienceCreateView, self).get_context_data(**kwargs)
        context['list_name'] = 'work_experiences'
        context['page_title'] = 'Work Experiences'
        context['cancel_url'] = reverse("work_experience_list")
        return context

    def form_valid(self, form):
        new_workExperience = form.save()
        self.request.user.get_profile().work_experiences.add(new_workExperience)
        return redirect(self.get_success_url())

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/edit_work_experience.html'
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
        context['page_title'] = 'Languages'
        context['cancel_url'] = reverse("language_list")
        return context

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/edit_language.html'
        return super(LanguageEditView, self).render_to_response(context, **kwargs)


class LanguageCreateView(CreateView):
    model = Language
    form_class = LanguageForm

    def get_success_url(self):
        return reverse("language_list")

    def get_context_data(self, **kwargs):
        context = super(LanguageCreateView, self).get_context_data(**kwargs)
        context['list_name'] = 'languages'
        context['page_title'] = 'Languages'
        context['cancel_url'] = reverse("language_list")
        return context

    def form_valid(self, form):
        new_language = form.save()
        self.request.user.get_profile().languages.add(new_language)
        return redirect(self.get_success_url())

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/edit_language.html'
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
        context['page_title'] = 'References'
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
        context['page_title'] = 'References'
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

class MyJobsListView(ListView):
    paginate_by = 5
    template_name = 'my_jobs_list.html'

    def get_queryset(self):
        return self.request.user.user_submitted_job_article_user.all().order_by('-date')

class ConnectionJobsListView(ListView):
    paginate_by = 5
    template_name = 'connection_jobs_list.html'

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['user_id'])
        return user.user_submitted_job_article_user.all().order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(ConnectionJobsListView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs['user_id'])
        context['user_id'] = self.kwargs['user_id']
        context['other_user_profile'] = user.get_profile()
        return context


class ConnectionJobsDetailView(DetailView):
    model = UserSubmittedJobArticle
    template_name = 'connection_jobs_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ConnectionJobsDetailView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs['user_id'])
        context['user_id'] = self.kwargs['user_id']
        context['other_user_profile'] = user.get_profile()
        return context


class MyJobsEditView(UpdateView):
    model = UserSubmittedJobArticle
    form_class = UserSubmittedJobArticleEditForm
    template_name = 'my_jobs_create.html'

    def get_success_url(self):
        return reverse("my_jobs")

    def get_context_data(self, **kwargs):
        context = super(MyJobsEditView, self).get_context_data(**kwargs)

        context['provinces'] = Province.objects.all().order_by('name').exclude(pk=1)
        context['categories'] = Category.objects.all().values('title').distinct().order_by('title')
        return context


class MyJobsDeleteView(DeleteView):
    model = UserSubmittedJobArticle
    template_name = 'my_jobs_delete.html'

    def get_success_url(self):
        return reverse("my_jobs")


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


class SkillsEditView(UpdateView):
    model = Skill
    form_class = SkillForm

    def get_success_url(self):
        return reverse("skills")

    def get_context_data(self, **kwargs):
        context = super(SkillsEditView, self).get_context_data(**kwargs)
        context['list_name'] = 'skills'
        context['page_title'] = 'Job Roles'
        context['cancel_url'] = reverse("skills")
        return context

    def render_to_response(self, context, **kwargs):
        self.template_name = 'profile/edit_skill.html'
        return super(SkillsEditView, self).render_to_response(context, **kwargs)


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
            .words.exclude(word__in = [skill.skill for skill in existing_skills])\
            .order_by('word')
    return render(request, 'profile/skills_0.html',
                            {'skills': skills})


@login_required
def add_connection_by_industry_result(request, industry, province, page=1):
    profiles_qs = CurriculumVitae.objects.exclude(first_name='')
    industry_pk = int(industry)
    province_pk = int(province)

    if industry_pk > 0:
        profiles_qs = profiles_qs.filter(skills__pk = industry_pk)
        selected_industry = AcceptedWord.objects.get(pk=industry_pk).word
    else:
        selected_industry = 'All'

    if province_pk > 0:
        profiles_qs = profiles_qs.filter(province = province_pk)
        selected_province = dict(PROVINCE_CHOICES)[province_pk]
    else:
        selected_province = 'All'

    paginator = Paginator(profiles_qs, 10) # Show 25 contacts per page

    try:
        paged_profiles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paged_profiles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paged_profiles = paginator.page(paginator.num_pages)

    return render(request, 'profile/add_connection_by_industry_result.html',
                                  {'user_profiles': paged_profiles,
                                   'provinces': PROVINCE_CHOICES,
                                   'industry': selected_industry,
                                   'province': selected_province,
                                   'industry_pk': industry_pk,
                                   'province_pk': province_pk,
                                   })

@login_required
def add_connection_by_industry(request):
    form = IndustrySearchForm()
    if request.method == 'POST':
        form = IndustrySearchForm(request.POST)
        if form.is_valid():
            industry = int(form.cleaned_data['industry'])
            province = int(form.cleaned_data['province'])

            return redirect(reverse('add_connection_by_industry_result', \
                            args=[industry,province]))

    skills = AcceptedWordCategory.objects.get(name='skills')\
            .words.order_by('word')
    return render(request, 'profile/add_connection_by_industry.html',
                            {'skills': skills,
                             'provinces': PROVINCE_CHOICES,
                             'form': form})

@login_required
def add_connection_by_first_name_result(request, province, page=1):
    name = request.GET.get('name', 'None')
    profiles_qs = CurriculumVitae.objects.filter(first_name__icontains=name)
    return render_connection_by_name_result(request, province, profiles_qs,\
            'profile/add_connection_by_first_name_result.html', name, page)

@login_required
def add_connection_by_surname_result(request, province, page=1):
    name = request.GET.get('name', 'None')
    profiles_qs = CurriculumVitae.objects.filter(surname__icontains=name)
    return render_connection_by_name_result(request, province, profiles_qs,\
            'profile/add_connection_by_surname_result.html', name, page)

def render_connection_by_name_result(request, province, profiles_qs,\
                                    template_name, name, page=1):
    province_pk = int(province)

    if province_pk > 0:
        profiles_qs = profiles_qs.filter(province = province_pk)
        selected_province = dict(PROVINCE_CHOICES)[province_pk]
    else:
        selected_province = 'All'

    paginator = Paginator(profiles_qs, 10) # Show 25 contacts per page

    try:
        paged_profiles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paged_profiles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paged_profiles = paginator.page(paginator.num_pages)

    return render(request, template_name,
                                  {'user_profiles': paged_profiles,
                                   'provinces': PROVINCE_CHOICES,
                                   'province': selected_province,
                                   'province_pk': province_pk,
                                   'name': name
                                   })

@login_required
def add_connection_by_first_name(request):
    form = ConnectionNameSearchForm()
    if request.method == 'POST':
        form = ConnectionNameSearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            province = int(form.cleaned_data['province'])

            return redirect("%s?first_name=%s" %\
                    (reverse('add_connection_by_first_name_result', args=[province]),
                    name))

    return render(request, 'profile/add_connection_by_first_name.html',
                            {'provinces': PROVINCE_CHOICES,
                             'form': form})

@login_required
def add_connection_by_surname(request):
    form = ConnectionNameSearchForm()
    if request.method == 'POST':
        form = ConnectionNameSearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            province = int(form.cleaned_data['province'])

            return redirect("%s?surname=%s" %\
                    (reverse('add_connection_by_surname_result', args=[province]),
                    name))

    return render(request, 'profile/add_connection_by_surname.html',
                            {'provinces': PROVINCE_CHOICES,
                             'form': form})

@login_required
@pin_required
def add_skill_from_list(request, skill_id):
    word = get_object_or_404(AcceptedWord, pk = skill_id) #Get word from list of skills
    profile = request.user.get_profile()
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            if not profile.skills.filter(skill=word.word).exists():
                skill = form.save()
                profile.skills.add(skill)
                return redirect(reverse('skills'))
            else:
                return render(request, 'profile/skill_duplicate.html',
                            {'skill': word.word})

    return render(request, 'profile/skill_from_list_confirm.html',
                            {'skill': word.word,
                             'form': form})

@login_required
@pin_required
def mark_skill_as_primary(request, skill_id):
    user_skills = request.user.get_profile().skills
    if user_skills.filter(pk = skill_id).exists():
        skill = user_skills.get(pk = skill_id) #Get word from list of skills

        skill.primary = True;
        skill.save()

        user_skills.exclude(pk=skill_id).update(primary=False)

    return redirect(reverse('skills'))
