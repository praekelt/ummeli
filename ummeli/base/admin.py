from ummeli.base.models import (Certificate, Language, WorkExperience,
    Reference, CurriculumVitae, CurriculumVitaeForm,  Article,  Province,  Category,
    UserSubmittedJobArticle)
from django.contrib import admin

class UserSubmittedJobArticleAdmin(admin.ModelAdmin):
    search_fields = ('title', 'text',)
    list_display = ('date','title', 'text', 'province', 'job_category')
    list_filter = ('province', 'job_category')
    ordering = ('-date',)
    date_hierarchy = 'date'

admin.site.register(CurriculumVitae)
admin.site.register(Certificate)
admin.site.register(Language)
admin.site.register(WorkExperience)
admin.site.register(Reference)
admin.site.register(Article)
admin.site.register(Province)
admin.site.register(Category)
admin.site.register(UserSubmittedJobArticle, UserSubmittedJobArticleAdmin)
