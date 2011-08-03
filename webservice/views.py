from django.shortcuts import *
from webservice.models import *
from django.core import serializers

def home(request):
    return HttpResponse("Welcome to ummeli.")

def getuserdata(request, _username):
	auser = User.objects.get(username = _username)
	cv = Curriculumvitae.objects.get(user = auser)
	certs = Certificate.objects.filter(cv=cv)
	refs = Reference.objects.filter(cv=cv)
	works = Workexperience.objects.filter(cv=cv)
	langs = Language.objects.filter(cv=cv)	

	data = serializers.serialize('json', [cv, certs, refs, works, langs])

	return HttpResponse(data)
