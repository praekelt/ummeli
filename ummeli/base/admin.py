from ummeli.base.models import (Certificate, Language, WorkExperience,
    Reference, CurriculumVitae, CurriculumVitaeForm,  Article,  Province,  Category,
    UserSubmittedJobArticle)
from django.contrib import admin
from jmbocomments.models import UserComment
from jmbocomments.admin import UserCommentAdmin


class UserSubmittedJobArticleAdmin(admin.ModelAdmin):
    search_fields = ('title', 'text', 'user__username')
    list_display = ('date', 'title', 'text', 'province', 'job_category')
    list_filter = ('province', 'job_category')
    ordering = ('-date',)
    date_hierarchy = 'date'
    raw_id_fields = ('user', )


class UmmeliUserCommentAdmin(UserCommentAdmin):
    list_display = ('content_object', 'user', 'comment_alias', 'comment',
                    'submit_date', 'is_public', 'is_removed', 'like_count',
                    'latest_flag')
    list_filter = ('submit_date', 'site', 'is_public', 'is_removed')

    def comment_alias(self, instance):
        return instance.user.get_profile().fullname()\
                if not instance.user.get_profile().comment_as_anon\
                else "Anon."

class ArticleAdmin(admin.ModelAdmin):
    search_fields = ('text',)
    list_display = ('date', 'text', 'source')
    list_filter = ('source',)
    ordering = ('-date',)
    date_hierarchy = 'date'

class JobCategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'province')
    list_filter = ('is_allowed','province')
    ordering = ('title',)

admin.site.register(CurriculumVitae)
admin.site.register(Certificate)
admin.site.register(Language)
admin.site.register(WorkExperience)
admin.site.register(Reference)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Province)
admin.site.register(Category, JobCategoryAdmin)
admin.site.register(UserSubmittedJobArticle, UserSubmittedJobArticleAdmin)

if UserComment in admin.site._registry:
    admin.site.unregister(UserComment)
admin.site.register(UserComment, UmmeliUserCommentAdmin)
