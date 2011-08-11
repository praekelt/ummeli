import base64
from django.test.client import Client
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate

class APIClient(Client):
    
    username = None
    password = None
    
    def request(self, **request):
        if ('HTTP_AUTHORIZATION' not in request) \
            and (self.username and self.password):
            b64 = base64.encodestring('%s:%s' % (
                self.username,
                self.password
            )).strip()
            request.update({'HTTP_AUTHORIZATION': 'Basic %s' % b64})
        return super(APIClient, self).request(**request)
    
    def login(self, username, password):
        """Overridge the cookie based login of Client,
we're using HTTP Basic Auth instead."""
        self.username = username
        self.password = password

class UserHelper:
    @staticmethod
    def get_user_or_403(username, password):
        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                return user
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied