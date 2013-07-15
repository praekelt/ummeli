from django.contrib import admin
from ummeli.opportunities.models import *
from jmbo.admin import ModelBaseAdmin
from ckeditor.widgets import AdminCKEditor


class OpportunityAdmin(ModelBaseAdmin):
    raw_id_fields = ('owner', 'location')
    formfield_overrides = {
        models.TextField: {'widget': AdminCKEditor},
    }


class CampaignAdmin(OpportunityAdmin):
    raw_id_fields = ('qualifiers', )


class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'state')
    raw_id_fields = ('user', 'task')

admin.site.register(Job, OpportunityAdmin)
admin.site.register(Internship, OpportunityAdmin)
admin.site.register(Volunteer, OpportunityAdmin)
admin.site.register(Bursary, OpportunityAdmin)
admin.site.register(Training, OpportunityAdmin)
admin.site.register(Event, OpportunityAdmin)
admin.site.register(Competition, OpportunityAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(TomTomCampaign, OpportunityAdmin)
admin.site.register(MicroTask, OpportunityAdmin)
admin.site.register(TomTomMicroTask, OpportunityAdmin)
admin.site.register(Province)
admin.site.register(Salary)
admin.site.register(MicroTaskResponse, TaskAdmin)
admin.site.register(TomTomMicroTaskResponse, TaskAdmin)
admin.site.register(TaskCheckout, TaskAdmin)
