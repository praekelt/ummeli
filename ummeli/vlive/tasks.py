from celery.task import task
from celery.task.sets import TaskSet
from vumiclient.client import Client
from django.conf import settings
from django.core.mail import send_mail,  EmailMessage

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