from ummeli.vlive.jobs.parsers import CategoryParser,  JobsParser
from celery.task import task
from celery.task.sets import TaskSet
from datetime import datetime, timedelta
from ummeli.opportunities.models import Job, Province
from django.utils.hashcompat import md5_constructor
from ummeli.base.utils import category_from_str
from django.contrib.sites.models import Site


@task(ignore_result=True)
def process_jobs(category_tuple,  jobs_parser, province):
    current_site = Site.objects.get_current()
    url, category = category_tuple

    articles = jobs_parser(url=url).parse()

    for date,  source,  text in articles:
        hash_key = md5_constructor(':'.join([date,  source,  text])).hexdigest()
        date_with_year = ('%s-%s' % (date,  datetime.now().strftime('%Y')))

        date = datetime.strptime(date_with_year, '%d-%m-%Y')
        job, created = Job.objects.get_or_create(hash_key=hash_key)

        if created:
            job.title = text[:80]
            job.description = '%s -- %s' % (text, source)
            job.category = category_from_str(category)
            job.state = 'published'
            job.created = date
            job.publish_on = date
            job.province = [Province.from_str(province)]
            job.sites.add(current_site)
            job.save()


@task(ignore_result=True)
def queue_categories(province, category_parser, jobs_parser):
    search_id, province_name = province
    parser = category_parser(search_id,  url = 'http://www.wegotads.co.za/Employment/listings/22001%(path)s?umb=1&search_source=%(id)s')
    urls = parser.parse()
    now = datetime.now()

    taskset = TaskSet(process_jobs.subtask((url, jobs_parser, province_name),
                                options = {'eta':now + timedelta(seconds=5 * i)})
                                for i,  url in enumerate(urls))

    return taskset.apply_async()


@task(ignore_result=True)
def run_jobs_update(category_parser = CategoryParser,  jobs_parser = JobsParser):    # allow mocking of parsers
    provinces = [
        (2, 'Gauteng'),
        (5, 'Western Cape'),
        (6, 'KwaZulu Natal')
    ]

    now = datetime.now()
    taskset = TaskSet(queue_categories.subtask((province, category_parser, jobs_parser),
                                options = {'eta':now + timedelta(seconds=10 * i)})
                                for i,  province in enumerate(provinces))
    return taskset.apply_async()
