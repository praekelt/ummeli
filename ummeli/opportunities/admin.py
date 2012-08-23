from django.contrib import admin
from ummeli.opportunities.models import *
from jmbo.admin import ModelBaseAdmin


class InternshipAdmin(ModelBaseAdmin):
    pass

admin.site.register(Internship, InternshipAdmin)
admin.site.register(Salary)
