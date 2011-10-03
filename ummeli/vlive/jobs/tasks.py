from ummeli.vlive.jobs_util import CategoryParser,  JobsParser
from celery.task import task
from celery.task.sets import TaskSet
from datetime import datetime, timedelta
from ummeli.vlive.models import Province

@task(ignore_result=True)
def process_jobs(link):
    JobsParser(url = link[0]).parse()

@task(ignore_result=True)
def queue_categories(id):
    urls = CategoryParser(id,  url = 'http://www.wegotads.co.za/Employment/listings/22001%(path)s?umb=1&search_source=%(id)s').parse()
    now = datetime.now()
    taskset = TaskSet(process_jobs.subtask((url, ),  
                                options = {'eta':now + timedelta(seconds=10 * i)})
                                for i,  url in enumerate(urls))
    taskset.apply_async()

@task(ignore_result=True)
def run_jobs_update():
    now = datetime.now()
    taskset = TaskSet(queue_categories.subtask((province.search_id, ), 
                                options = {'eta':now + timedelta(seconds=10 * i)}) 
                                for i,  province in enumerate(Province.objects.all()))
    taskset.apply_async()
    
