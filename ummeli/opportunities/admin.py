from django.contrib import admin
from ummeli.opportunities.models import *
from jmbo.admin import ModelBaseAdmin


class OpportunityAdmin(ModelBaseAdmin):
    pass

admin.site.register(Internship, OpportunityAdmin)
admin.site.register(Volunteer, OpportunityAdmin)
admin.site.register(Bursary, OpportunityAdmin)
admin.site.register(Training, OpportunityAdmin)
admin.site.register(Event, OpportunityAdmin)
admin.site.register(Competition, OpportunityAdmin)
admin.site.register(Salary)
