from celery.task import task
from celery.task.sets import TaskSet
from vumiclient.client import Client

@task(ignore_result=True)
def send_password_reset(msisdn, new_password):    
    message = 'Ummeli on YAL :) Your new password is: %s' % new_password
    client = Client('ummeli', '4mm3l1')
    client.send_sms(to_msisdn = msisdn,  
        from_msisdn = '', 
        message = message)
