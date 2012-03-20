from random import randint

from django import http
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse

from ummeli.vlive.utils import pin_required
from django.contrib.auth.decorators import login_required

@login_required
@pin_required
def profile_detail(request, pk=None):

    if request.method == 'POST':
        request.user.first_name = request.POST.get('nickname', '')
        request.user.save()

    # is the user viewing their own profile, and therefore editing it?
    if not pk:
        profile_user = request.user
        editable = True
    else:
        profile_user = get_object_or_404(User, pk=pk)
        editable = False
        if profile_user == request.user:
            editable = True

    nickname = profile_user.get_full_name() or 'Anon.'

    return direct_to_template(request, 'accounts/profile_detail.html', {
        'profile_user': profile_user,
        'nickname': nickname,
        'editable': editable
    })
