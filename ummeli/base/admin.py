from datetime import datetime, timedelta
from ummeli.base.models import *
from django.contrib import admin
from django.core.urlresolvers import reverse
from django import forms
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
        ban_url = reverse('admin:base_userban_add') + '?user=%s' % obj.user.id
        return '<a href="%s?user=%s">%s</a>' % (
            reverse(
                'admin:%s_%s_changelist' % (
                    obj._meta.app_label,
                    obj._meta.module_name
                ),
            ),
            obj.user.id,
            comment_alias,
        ) + ' (<a href="%s">edit</a>) (<a href="%s">ban</a>)' % (
            url, ban_url)

    comment_alias.allow_tags = True
    comment_alias.short_description = 'Comment Alias'

    def queryset(self, request):
        """
        Due to the volume of comments, moderation of comments is becoming
        unwieldy. We're limiting the number of comments displayed in the CMS

        Only show comments in the last month
        """
        qs = super(UmmeliUserCommentAdmin, self).queryset(request)

        #only apply date filter if no date filter in query string
        query_string = request.GET.copy()
        if ('submit_date' in query_string or
            'submit_date__gte' in query_string or
            'submit_date__lte' in query_string or
            'submit_date__lt' in query_string or
                'submit_date__gt' in query_string):
            return qs

        recent_qs = qs.filter(
            submit_date__gte=datetime.now()-timedelta(days=30))
        if recent_qs.exists():
            return recent_qs

        return qs


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
        url = obj.image.url if obj.image else None
        return '<img src="%s" />' % (url, )
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


class UserBanAdminForm(forms.ModelForm):
    bans = forms.IntegerField(required=False)
    last_ban = forms.DateTimeField(required=False)
    last_ban_duration = forms.IntegerField(required=False)

    def get_last_ban(self, user):
        for ban in user.userban_set.all():
            last_ban = ban.ban_on
            last_ban_duration = ban.get_ban_duration()
            return (last_ban, last_ban_duration)
        return (None, None)

    def __init__(self, *args, **kwargs):
        super(UserBanAdminForm, self).__init__(*args, **kwargs)
        initial = kwargs.get('initial')
        instance = kwargs.get('instance')
        bans_count = last_ban = last_ban_duration = None
        if instance:
            bans_count = instance.user.userban_set.all().count()
            last_ban, last_ban_duration = self.get_last_ban(instance.user)
        if initial:
            user_pk = initial.get('user')
            if User.objects.filter(pk=user_pk).exists():
                user = User.objects.get(pk=user_pk)
                bans = user.userban_set.all().order_by('-ban_on')
                bans_count = bans.count()
                last_ban, last_ban_duration = self.get_last_ban(user)

        self.fields['bans'].initial = bans_count
        self.fields['last_ban'].initial = last_ban
        self.fields['last_ban_duration'].initial = last_ban_duration

        self.fields['bans'].widget.attrs['disabled'] = 'disabled'
        self.fields['last_ban'].widget.attrs['disabled'] = 'disabled'
        self.fields['last_ban_duration'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = UserBan


class UserBanAdmin(admin.ModelAdmin):
    list_display = ('user', 'ban_on', 'unban_on', '_bans', '_duration',
                    '_active')
    list_filter = ('ban_on', 'unban_on', 'user__is_active')
    raw_id_fields = ('user', )
    ordering = ('-ban_on', )
    exclude = ('is_unbanned', )
    form = UserBanAdminForm

    def _active(self, obj, *args, **kwargs):
        return obj.user.is_active
    _active.allow_tags = True
    _active.boolean = True
    _active.short_description = "active"

    def _bans(self, obj, *args, **kwargs):
        return obj.user.userban_set.all().count()
    _bans.allow_tags = True
    _bans.short_description = "bans"

    def _duration(self, obj, *args, **kwargs):
        return obj.get_ban_duration()
    _duration.short_description = "duration"

admin.site.register(CurriculumVitae, CurriculumVitaeAdmin)
admin.site.register(Certificate)
admin.site.register(Language)
admin.site.register(WorkExperience)
admin.site.register(Reference)
admin.site.register(Banner, BannerAdmin)
admin.site.register(UserBan, UserBanAdmin)

if UserComment in admin.site._registry:
    admin.site.unregister(UserComment)
admin.site.register(UserComment, UmmeliUserCommentAdmin)
