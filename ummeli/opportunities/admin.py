from django.contrib import admin
from ummeli.opportunities.models import *
from jmbo.admin import ModelBaseAdmin


class OpportunityAdmin(ModelBaseAdmin):
    pass

admin.site.register(Internship, OpportunityAdmin)
admin.site.register(Salary)
