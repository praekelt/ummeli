from django.contrib import admin
from ummeli.opportunities.models import *
from jmbo.admin import ModelBaseAdmin
from ckeditor.widgets import CKEditorWidget


class OpportunityAdmin(ModelBaseAdmin):
    raw_id_fields = ('owner', 'location')
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }

class UmmeliOpportunityAdmin(OpportunityAdmin):
    list_filter = ('state', 'created', 'is_community',)


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
