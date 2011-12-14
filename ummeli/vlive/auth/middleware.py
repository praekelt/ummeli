from jmbovlive.utils import pml_redirect_timer_view
from django.contrib.auth.middleware import RemoteUserMiddleware
from django.conf import settings

class UserAuthorizationMiddleware(object):
    
    def process_request(self, request):
        if request.session.get(settings.UMMELI_PIN_SESSION_KEY):
            request.is_authorized = True
        else:
            request.is_authorized = False
