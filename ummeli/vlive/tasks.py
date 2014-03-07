import json
import requests
from celery.task import task
from django.conf import settings
from django.core.mail import EmailMessage
from jmboarticles.models import Article


@task(ignore_result=True)
def send_password_reset(msisdn, new_password):
    message = 'Ummeli on YAL :) Your new password is: %s' % new_password
    send_sms(msisdn, message)


@task(ignore_result=True)
def send_email(username, message):
    email = EmailMessage(
        'Blocked User: %s' % username,
        message,
        settings.SEND_FROM_EMAIL_ADDRESS,
        [settings.UMMELI_SUPPORT]
    )
    email.send(fail_silently=False)


def send_sms(to_msisdn, msg):
    base_url = 'https://go.vumi.org/api/v1'
    url = '%s/go/http_api_nostream/%s/messages.json' % (
        base_url,
        settings.VUMI_SMS_CONVERSATION_KEY
    )
    data = {
        "content": msg,
        "to_addr": to_msisdn
    }
    requests.put(
        url,
        json.dumps(data),
        auth=(settings.VUMI_ACCOUNT_KEY, settings.VUMI_ACCESS_TOKEN),
    )


def disable_commenting():
    Article.objects.filter(comments_enabled=True, can_comment=False)\
                   .update(can_comment=True)
    Article.objects.filter(comments_enabled=True, can_comment=True)\
                   .update(comments_enabled=False)


def enable_commenting():
    qs = Article.published_objects.filter(can_comment=True)

    #on homepage
    qs.filter(on_homepage=True).update(comments_enabled=True)

    #latest 3 articles
    featured = qs.filter(on_homepage=False)[:3]

    #disable other articles
    Article.published_objects.filter(comments_enabled=True, can_comment=True,
                                     on_homepage=False)\
                             .exclude(pk__in=[a.pk for a in featured])\
                             .update(comments_enabled=False)

    for a in featured:
        a.comments_enabled = True
        a.save()


@task(ignore_result=True)
def disable_comments_scheduler():
    from datetime import datetime, time
    now = datetime.now().time()
    if now > time(21, 0, 0) or now < time(11, 0, 0):
        disable_commenting()
    else:
        enable_commenting()
