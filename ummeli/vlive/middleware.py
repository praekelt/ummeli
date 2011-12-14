from django.contrib import messages

class AddMessageToResponseMiddleware(object):
    def process_response(self, request,  response):
        if (request.method == 'POST' and 
            (response.status_code == 301 or response.status_code == 302)):
                messages.add_message(request, messages.SUCCESS, 'Submitted successfully.')
        return response
