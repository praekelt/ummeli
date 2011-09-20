class FormActionMiddleware(object):
    """
    Friendlier access to device / request info that Vodafone Live makes 
    available to us via HTTP Headers
    """
    def process_request(self, request):
        if (request.GET.get('_action',  None) == 'POST'):
            request.method = "POST"
            request.POST = request.GET
            print request.POST
