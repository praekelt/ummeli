from django.forms import *
from ummeli.vlive.forms import PMLForm


class IndustrySearchForm(PMLForm):
    industry = IntegerField(required=True)
    province = IntegerField(required=True)


class ConnectionNameSearchForm(PMLForm):
    name = CharField(required=True)
    province = IntegerField(required=True)
