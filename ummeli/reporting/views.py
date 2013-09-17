from django.shortcuts import redirect
from django.http import HttpResponseNotFound
from reporting import helpers
from jmbo.models import ModelBase
from django.shortcuts import get_object_or_404


def report(request, slug, report_key_field):
    if 'HTTP_REFERER' not in request.META:
        return HttpResponseNotFound()

    helpers.vote(request.user,
        get_object_or_404(ModelBase, slug=slug),
        report_key_field
    )

    return redirect(request.META['HTTP_REFERER'])
