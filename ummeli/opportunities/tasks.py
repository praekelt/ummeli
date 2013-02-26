from celery.task import task
from ummeli.opportunities.models import MicroTask


@task(ignore_result=True)
def microtask_expire_tasks():
    MicroTask.expire_tasks()
