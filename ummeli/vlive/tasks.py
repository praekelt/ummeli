from celery.task import task
from celery.task.sets import TaskSet

@task(ignore_result=True)
def send_password_reset(msisdn, new_password):    
    #TODO: send password using Vumi
    return True
