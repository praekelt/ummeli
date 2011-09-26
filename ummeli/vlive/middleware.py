class FormActionMiddleware(object):
    """
    Friendlier access to device / request info that Vodafone Live makes 
    available to us via HTTP Headers
    """
    def process_request(self, request):
        msisdn = request.META.get('HTTP_X_UP_CALLING_LINE_ID', None)

        if (request.GET.get('_action',  None) == 'POST' and msisdn != None):
            request.method = "POST"
            request.POST = request.GET
            print 'here'
