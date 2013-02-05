from django.contrib import admin
from ummeli.opportunities.models import *
from jmbo.admin import ModelBaseAdmin
from ckeditor.widgets import AdminCKEditor


class OpportunityAdmin(ModelBaseAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminCKEditor},
    }

admin.site.register(Job, OpportunityAdmin)
admin.site.register(Internship, OpportunityAdmin)
admin.site.register(Volunteer, OpportunityAdmin)
admin.site.register(Bursary, OpportunityAdmin)
admin.site.register(Training, OpportunityAdmin)
admin.site.register(Event, OpportunityAdmin)
admin.site.register(Competition, OpportunityAdmin)
admin.site.register(Campaign, OpportunityAdmin)
admin.site.register(TomTomCampaign, OpportunityAdmin)
admin.site.register(MicroTask, OpportunityAdmin)
admin.site.register(TomTomMicroTask, OpportunityAdmin)
admin.site.register(Salary)
admin.site.register(MicroTaskResponse)
admin.site.register(TomTomMicroTaskResponse)
admin.site.register(TaskCheckout)
