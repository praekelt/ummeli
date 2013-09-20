from redis import StrictRedis
from django.conf import settings

redis_server = StrictRedis(**settings.REDIS_SETTINGS)

def get_object_vote_key(obj, report_key_field):
    return '-'.join([obj.content_type.app_label,
        obj.content_type.model,
        obj.slug,
        report_key_field
    ])

def get_user_vote_key(user, obj, report_key_field):
    return '-'.join([user.username,
        get_object_vote_key(obj, report_key_field)
    ])

def get_object_votes(obj, report_key_field):
    key = get_object_vote_key(obj, report_key_field)
    votes = redis_server.get(key) or 0
    return int(votes)

def has_voted(user, obj, report_key_field):
    key = get_user_vote_key(user, obj, report_key_field)
    return redis_server.exists(key)

def vote(user, obj, report_key_field):
    if not has_voted(user, obj, report_key_field):
        redis_server.incr(get_object_vote_key(obj, report_key_field))
        redis_server.incr(get_user_vote_key(user, obj, report_key_field))
