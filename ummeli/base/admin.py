from ummeli.base.models import *
from django.contrib import admin
from jmbocomments.models import UserComment
from jmbocomments.admin import UserCommentAdmin
from jmbo.admin import ModelBaseAdmin




class UmmeliUserCommentAdmin(UserCommentAdmin):
    list_display = ('content_object', 'user', 'comment_alias', 'comment',
                    'submit_date', 'is_public', 'is_removed', 'like_count',
                    'latest_flag')
    list_filter = ('submit_date', 'site', 'is_removed')

    def comment_alias(self, instance):
        return instance.user.get_profile().fullname()\
                if not instance.user.get_profile().comment_as_anon\
                else "Anon."

class BannerAdmin(ModelBaseAdmin):

    list_display = (
        'title', 'description', 'thumbnail', 'schedule', 'state')
    raw_id_fields = ('owner', 'location')

    def thumbnail(self, obj, *args, **kwargs):
        return '<img src="%s" />' % (obj.image.url,)
    thumbnail.allow_tags = True

    def schedule(self, obj, *args, **kwargs):
        if(obj.time_on and obj.time_off):
            return 'Randomly selected by Vlive between %s and %s' % (
                obj.time_on, obj.time_off)
        return 'Randomly selected by Vlive'

admin.site.register(CurriculumVitae)
admin.site.register(Certificate)
admin.site.register(Language)
admin.site.register(WorkExperience)
admin.site.register(Reference)
admin.site.register(Banner, BannerAdmin)

if UserComment in admin.site._registry:
    admin.site.unregister(UserComment)
admin.site.register(UserComment, UmmeliUserCommentAdmin)
