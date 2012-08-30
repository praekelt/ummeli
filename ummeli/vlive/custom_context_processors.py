import uuid
from ummeli.base.models import PROVINCE_CHOICES


def unique_id_processor(request):
    return {'uuid': str(uuid.uuid4())}


def user_profile_processor(request):
    if hasattr(request, 'user') and request.user.is_authenticated():
        return {'user_profile': request.user.get_profile()}
    return {}


def province_session_processor(request):
    province = request.session.get('province', None)

    if province:
        return {'province_id': province,
                'province': dict(PROVINCE_CHOICES)[province]}

    if hasattr(request, 'user')\
        and request.user.is_authenticated():
        province = request.user.get_profile().province
        province = province if province else 0
        request.session['province'] = province
        return {'province_id': province,
                'province': dict(PROVINCE_CHOICES)[province]}

    return {'province_id': 0,
            'province': dict(PROVINCE_CHOICES)[0]}
