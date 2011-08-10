import base64
from django.test.client import Client

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
