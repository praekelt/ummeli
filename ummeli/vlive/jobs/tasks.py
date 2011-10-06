from ummeli.vlive.jobs.parsers import CategoryParser,  JobsParser
from celery.task import task
from celery.task.sets import TaskSet
from datetime import datetime, timedelta
from ummeli.vlive.models import Article,  Province,  Category
from django.utils.hashcompat import md5_constructor

@task(ignore_result=True)
def process_jobs(search_id,  link):    
    province = Province.objects.get(search_id = search_id)
    category = province.job_categories.get(title = link[1])
    
    articles = JobsParser(url = link[0]).parse()
    for date,  source,  text in articles:
        hash = md5_constructor(':'.join([date,  source,  text])).hexdigest()
        article = Article(hash_key = hash,  
                                date = date, 
                                source = source,  
                                text = text)
        article.save()
        category.articles.add(article)

@task(ignore_result=True)
def queue_categories(search_id):
    urls = CategoryParser(search_id,  url = 'http://www.wegotads.co.za/Employment/listings/22001%(path)s?umb=1&search_source=%(id)s').parse()
    
    province = Province.objects.get(search_id = search_id)
    province.job_categories.clear()
    
    for link, title in urls:
        hash = md5_constructor(title).hexdigest()
        cat = Category(hash_key = hash,  title = title)
        cat.save()
        province.job_categories.add(cat) 
    province.save()
    
    now = datetime.now()
    
    taskset = TaskSet(process_jobs.subtask((search_id,  url, ),  
                                options = {'eta':now + timedelta(seconds=5 * i)})
                                for i,  url in enumerate(urls))
    taskset.apply_async()

@task(ignore_result=True)
def run_jobs_update():
    Province(search_id = 1,  name = 'All').save()
    Province(search_id = 2,  name = 'Gauteng').save()
    Province(search_id = 5,  name = 'WC').save()
    Province(search_id = 6,  name = 'KZN').save()
    
    now = datetime.now()
    taskset = TaskSet(queue_categories.subtask((province.search_id, ), 
                                options = {'eta':now + timedelta(seconds=10 * i)}) 
                                for i,  province in enumerate(Province.objects.all()))
    taskset.apply_async()
