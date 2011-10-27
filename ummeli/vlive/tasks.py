from celery.task import task
from celery.task.sets import TaskSet
from vumiclient.client import Client
from django.conf import settings

@task(ignore_result=True)
def send_password_reset(msisdn, new_password):
    message = 'Ummeli on YAL :) Your new password is: %s' % new_password
    client = Client(settings.VUMI_USERNAME, settings.VUMI_PASSWORD)
    resp = client.send_sms(to_msisdn = msisdn,
        from_msisdn = '1',
        message = message)
