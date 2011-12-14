from functools import wraps
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render
from django.conf import settings
from django.core.urlresolvers import reverse
from jmbovlive.utils import pml_redirect_timer_view

def pin_required(function):
    """
    Decorator to ask people to verify their pin before being able to access a view.
    """
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        auth_backend = ModelBackend()
        if request.session.get(settings.UMMELI_PIN_SESSION_KEY):
            return function(request, *args, **kwargs)
            
        if request.user.password:
            return pml_redirect_timer_view(request, settings.LOGIN_URL,
                    redirect_time = 0,
                    redirect_message = 'You need to login first.')
        else:
            return pml_redirect_timer_view(request, reverse('register'),
                    redirect_time = 0,
                    redirect_message = 'You need to create a pin first.')
                    
    return wrapper
                                
def phone_number_to_international(phone_number):
    if phone_number.startswith('27') and len(phone_number) == 11:
        return phone_number
    elif phone_number.startswith('0') and len(phone_number) == 10:
        return '27' + phone_number[1:]
    else:
        return 'invalid no'

def process_post_data_username(post):
    """
    converts username(phone number) to valid international phone number (27821234567)
    """
    if not post.get('username', None):
        return post
    
    post_data = post.copy()
    post_data['username'] = phone_number_to_international(post_data['username'])
    return post_data
