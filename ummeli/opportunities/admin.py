from django.contrib import admin
from ummeli.opportunities.models import Opportunity
from jmbo.admin import ModelBaseAdmin


class OpportunityAdmin(ModelBaseAdmin):
    pass

admin.site.register(Opportunity, OpportunityAdmin)
