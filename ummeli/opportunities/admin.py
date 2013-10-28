from django.contrib import admin
from ummeli.opportunities.models import *
from jmbo.admin import ModelBaseAdmin
from ckeditor.widgets import CKEditorWidget
from reporting import helpers


class OpportunityAdmin(ModelBaseAdmin):
    raw_id_fields = ('owner', 'location')
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }

class UmmeliOpportunityAdmin(OpportunityAdmin):
    list_filter = ('state', 'created', 'is_community',)
    list_display = ('title', 'publish_on', 'retract_on',
                    '_get_absolute_url', 'owner', 'created',
                    '_community_moderation', '_actions')

    def _community_moderation(self, obj):
        # Poll redis for whether this opportunity was removed
        scam_votes = helpers.get_object_votes(obj, UmmeliOpportunity.SCAM_REPORT_KEY_FIELD)
        postion_filled_votes = helpers.get_object_votes(obj, UmmeliOpportunity.POSITION_FILLED_REPORT_KEY_FIELD)
        inappropriate_votes = helpers.get_object_votes(obj, UmmeliOpportunity.INAPPROPRIATE_REPORT_KEY_FIELD)

        is_scam = scam_votes >= settings.REPORT_FLAG_LIMIT
        is_position_filled = postion_filled_votes >= settings.REPORT_FLAG_LIMIT
        is_removed_by_community = inappropriate_votes >= settings.REPORT_FLAG_LIMIT

        if is_removed_by_community:
            return 'Removed by community'
        if is_position_filled:
            return 'Position filled'
        if is_scam:
            return 'Scam'
        return ''

    _community_moderation.short_description = 'Moderation'
    _community_moderation.allow_tags = True


class CampaignAdmin(OpportunityAdmin):
    raw_id_fields = ('qualifiers', )


class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'state')
    raw_id_fields = ('user', 'task')

admin.site.register(Job, UmmeliOpportunityAdmin)
admin.site.register(Internship, UmmeliOpportunityAdmin)
admin.site.register(Volunteer, UmmeliOpportunityAdmin)
admin.site.register(Bursary, UmmeliOpportunityAdmin)
admin.site.register(Training, UmmeliOpportunityAdmin)
admin.site.register(Event, OpportunityAdmin)
admin.site.register(Competition, OpportunityAdmin)
admin.site.register(StatusUpdate, UmmeliOpportunityAdmin)
admin.site.register(SkillsUpdate, UmmeliOpportunityAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(TomTomCampaign, OpportunityAdmin)
admin.site.register(MicroTask, OpportunityAdmin)
admin.site.register(TomTomMicroTask, OpportunityAdmin)
admin.site.register(Province)
admin.site.register(Salary)
admin.site.register(MicroTaskResponse, TaskAdmin)
admin.site.register(TomTomMicroTaskResponse, TaskAdmin)
admin.site.register(TaskCheckout, TaskAdmin)
