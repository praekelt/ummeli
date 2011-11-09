from django.contrib.auth.middleware import RemoteUserMiddleware
from django.conf import settings

class VodafoneLiveUserMiddleware(RemoteUserMiddleware):
    header = 'HTTP_X_UP_CALLING_LINE_ID'

class VodafoneLiveInfo(object): 
    pass

class VodafoneLiveInfoMiddleware(object):
    """
    Friendlier access to device / request info that Vodafone Live makes 
    available to us via HTTP Headers
    """
    def process_request(self, request):
        vlive = VodafoneLiveInfo()
        vlive.msisdn = request.META.get('HTTP_X_UP_CALLING_LINE_ID', 'unknown')
        vlive.area = request.META.get('HTTP_X_VODAFONE_AREA', 'unknown')
        request.vlive = vlive
        
        if request.session.get(settings.UMMELI_PIN_SESSION_KEY):
            request.is_authorized = True
        else:
            request.is_authorized = False
