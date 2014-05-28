from ummeli.vlive.jobs.parsers import CategoryParser,  JobsParser
from celery.task import task
from datetime import datetime
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
        hash_key = md5_constructor(
            ':'.join([date,  source,  text])).hexdigest()
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
    parser = category_parser(
        search_id,  url='http://www.wegotads.co.za/Employment/listings/22001%(path)s?umb=1&search_source=%(id)s')
    urls = parser.parse()

    for url in urls:
        process_jobs(url, jobs_parser, province_name)


@task(ignore_result=True)
# allow mocking of parsers
def run_jobs_update(category_parser=CategoryParser,  jobs_parser=JobsParser):
    provinces = [
        (2, 'Gauteng'),
        (5, 'Western Cape'),
        (6, 'KwaZulu Natal')
    ]

    for i,  province in enumerate(provinces):
        queue_categories(province, category_parser, jobs_parser)
