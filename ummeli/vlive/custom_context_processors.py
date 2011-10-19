import uuid

def unique_id_processor(request):
    return {'uuid': str(uuid.uuid4())}
    
def user_profile_processor(request):
    return {'user_profile': request.user.get_profile()}
