from celery.task import task
from celery.task.sets import TaskSet
from vumiclient.client import Client
from django.conf import settings
from django.core.mail import send_mail,  EmailMessage
from jmboarticles.models import Article
from django.db.models import Q


@task(ignore_result=True)
def send_password_reset(msisdn, new_password):
    message = 'Ummeli on YAL :) Your new password is: %s' % new_password
    client = Client(settings.VUMI_USERNAME, settings.VUMI_PASSWORD)
    resp = client.send_sms(to_msisdn = msisdn,
        from_msisdn = '1',
        message = message)


@task(ignore_result=True)
def send_email(username, message):
    email = EmailMessage('Blocked User: %s' % username, message,
                                            settings.SEND_FROM_EMAIL_ADDRESS,
                                            [settings.UMMELI_SUPPORT])
    email.send(fail_silently=False)


def send_sms(msisdn, message):
    client = Client(settings.VUMI_USERNAME, settings.VUMI_PASSWORD)
    client.send_sms(to_msisdn = msisdn, from_msisdn = '1', message = message)


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
    if now > time(22, 0, 0) or now < time(6, 0, 0):
        disable_commenting()
    else:
        enable_commenting()
