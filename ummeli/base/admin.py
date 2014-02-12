from ummeli.base.models import *
from django.contrib import admin
from django.core.urlresolvers import reverse
from jmbocomments.models import UserComment
from jmbocomments.admin import UserCommentAdmin
from jmbo.admin import ModelBaseAdmin


class UmmeliUserCommentAdmin(UserCommentAdmin):
    list_display = ('content_object', 'user', 'comment_alias', 'comment',
                    'submit_date', 'is_public', 'is_removed', 'like_count',
                    'latest_flag')
    list_filter = ('submit_date', 'site', 'is_removed')

    def comment_alias(self, obj):
        comment_alias = obj.user.get_profile().fullname()\
            if not obj.user.get_profile().comment_as_anon\
            else "Anon."

        url = reverse('admin:auth_user_change', args=(obj.user.id,))
        return '<a href="%s?user=%s">%s</a>' % (
            reverse(
                'admin:%s_%s_changelist' % (
                    obj._meta.app_label,
                    obj._meta.module_name
                ),
            ),
            obj.user.id,
            comment_alias,
        ) + ' (<a href="%s">edit</a>)' % url
    comment_alias.allow_tags = True
    comment_alias.short_description = 'Comment Alias'


class BannerAdmin(ModelBaseAdmin):
    list_filter = (
        'state',
        'created',
        'categories',
        'banner_type'
    )
    list_display = (
        'title', 'description', 'thumbnail', 'schedule', '_actions')
    raw_id_fields = ('owner', 'location')

    def thumbnail(self, obj, *args, **kwargs):
        return '<img src="%s" />' % (obj.image.url,)
    thumbnail.allow_tags = True

    def schedule(self, obj, *args, **kwargs):
        if(obj.time_on and obj.time_off):
            return 'Randomly selected by Vlive between %s and %s' % (
                obj.time_on, obj.time_off)
        return 'Randomly selected by Vlive'

class CurriculumVitaeAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'first_name', 'surname']
    list_display = ('user', 'first_name', 'surname', 'province')
    raw_id_fields = ('user', 'certificates', 'languages', 'work_experiences',
                     'references', 'preferred_skill', 'skills',
                     'connection_requests')
    readonly_fields = ('user', 'province', 'certificates', 'languages',
                     'work_experiences', 'references', 'preferred_skill',
                     'skills', 'connection_requests')
    list_filter = ('province', )

admin.site.register(CurriculumVitae, CurriculumVitaeAdmin)
admin.site.register(Certificate)
admin.site.register(Language)
admin.site.register(WorkExperience)
admin.site.register(Reference)
admin.site.register(Banner, BannerAdmin)

if UserComment in admin.site._registry:
    admin.site.unregister(UserComment)
admin.site.register(UserComment, UmmeliUserCommentAdmin)
