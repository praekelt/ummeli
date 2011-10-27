from functools import wraps
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render
from django.conf import settings


def pin_required(function):
    """
    Decorator to ask people to verify their pin before being able to access a view.
    """
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        auth_backend = ModelBackend()
        if request.session.get(settings.UMMELI_PIN_SESSION_KEY):
            return function(request, *args, **kwargs)
        return pml_redirect_timer_view(request, settings.LOGIN_URL,
                redirect_time = 0,
                redirect_message = 'Redirecting to the login page')
    return wrapper

def pml_redirect_timer_view(request,  redirect_url,  redirect_time = 20,  redirect_message = 'Thank you.'):
    return render(request, 'pml/redirect.xml',
                                {'redirect_url': redirect_url,
                                'redirect_time': redirect_time,
                                'redirect_message': redirect_message},
                                content_type='text/xml')

