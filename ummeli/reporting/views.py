from django.shortcuts import redirect
from django.http import HttpResponseNotFound
from reporting import helpers
from jmbo.models import ModelBase
from django.shortcuts import get_object_or_404
from django.contrib import messages


def report(request, slug, report_key_field):
    if 'HTTP_REFERER' not in request.META:
        return HttpResponseNotFound()

    helpers.vote(request.user,
        get_object_or_404(ModelBase, slug=slug),
        report_key_field
    )

    msg = 'Thank you for your report. A notification will appear if 3 separate users report this.'
    messages.success(request, msg)
    return redirect(request.META['HTTP_REFERER'])
