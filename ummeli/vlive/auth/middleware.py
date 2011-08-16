from django.contrib.auth.middleware import RemoteUserMiddleware

class VodafoneLiveUserMiddleware(RemoteUserMiddleware):
    header = 'HTTP_X_UP_CALLING_LINE_ID'


class VodafoneLiveInfo(object): pass

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
