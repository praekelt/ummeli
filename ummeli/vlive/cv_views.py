from ummeli.vlive.forms import (PersonalDetailsForm)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

@login_required
def personal_details(request):
    cv = request.user.get_profile()
    if request.method == 'POST':
        cancel = request.POST.get('cancel', None)
        if cancel:
            return HttpResponseRedirect(reverse('vlive:edit'))
        else:
            form = PersonalDetailsForm(request.POST, instance=cv)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('vlive:edit'))
    else:
        form = PersonalDetailsForm(instance=cv)
    return render_to_response('vlive/personal_details.html', {'form': form},
                            context_instance=RequestContext(request))
