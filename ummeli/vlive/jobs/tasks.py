from ummeli.vlive.jobs.parsers import CategoryParser,  JobsParser
from celery.task import task
from celery.task.sets import TaskSet
from datetime import datetime, timedelta
from ummeli.vlive.models import Article,  Province,  Category
from django.utils.hashcompat import md5_constructor

@task
def process_jobs(cat_id,  link,  jobs_parser):    
    category = Category.objects.get(pk = cat_id)
    
    articles = jobs_parser(url = link[0]).parse()
    
    for date,  source,  text in articles:
        hash = md5_constructor(':'.join([date,  source,  text])).hexdigest()
        date_with_year = ('%s-%s' % (date,  datetime.now().strftime('%Y')))
        article = Article(hash_key = hash,  
                                date = datetime.strptime(date_with_year, '%d-%m-%Y'), 
                                source = source,  
                                text = text)
        article.save()
        if not (category.articles.filter(pk = hash).exists()):
            category.articles.add(article)
    return category

def create_category_id_hash(search_id,  title):
    return md5_constructor('%s:%s' % (title,  search_id)).hexdigest()

@task
def queue_categories(search_id,  category_parser,  jobs_parser):
    parser = category_parser(search_id,  url = 'http://www.wegotads.co.za/Employment/listings/22001%(path)s?umb=1&search_source=%(id)s')
    urls = parser.parse()
    
    province = Province.objects.get(search_id = search_id)
    
    for link, title in urls:
        hash = create_category_id_hash(search_id,  title)
        cat = Category(province = province,  hash_key = hash,  title = title)
        cat.save()
        
    now = datetime.now()
    
    taskset = TaskSet(process_jobs.subtask((create_category_id_hash(search_id,  url[1]),  url, jobs_parser, ),  
                                options = {'eta':now + timedelta(seconds=5 * i)})
                                for i,  url in enumerate(urls))
                                
    result = taskset.apply_async()
    
    return province

@task
def run_jobs_update(category_parser = CategoryParser,  jobs_parser = JobsParser):    # allow mocking of parsers
    Province(search_id = 1,  name = 'All').save()
    Province(search_id = 2,  name = 'Gauteng').save()
    Province(search_id = 5,  name = 'Western Cape').save()
    Province(search_id = 6,  name = 'KZN').save()
    Province(search_id = -1,  name = 'Limpopo').save()
    Province(search_id = -2,  name = 'Mpumalanga').save()
    Province(search_id = -3,  name = 'Free State').save()
    Province(search_id = -4,  name = 'Northern Cape').save()
    Province(search_id = -5,  name = 'Eastern Cape').save()
    Province(search_id = -6,  name = 'North West').save()
    
    now = datetime.now()
    taskset = TaskSet(queue_categories.subtask((province.search_id, category_parser,  jobs_parser, ), 
                                options = {'eta':now + timedelta(seconds=10 * i)}) 
                                for i,  province in enumerate(Province.objects.all()) if province.search_id > 0)
    
    return taskset.apply_async()
