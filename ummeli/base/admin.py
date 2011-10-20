from ummeli.base.models import (CurriculumVitae, Certificate,
                                Language, WorkExperience, Reference)
from django.contrib import admin

admin.site.register(CurriculumVitae)
admin.site.register(Certificate)
admin.site.register(Language)
admin.site.register(WorkExperience)
admin.site.register(Reference)
