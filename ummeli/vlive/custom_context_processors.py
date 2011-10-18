import uuid

def unique_id_processor(request):
    return {'uuid': str(uuid.uuid4())}
