from django.contrib.sites.models import Site
from ummeli.opportunities.models import Campaign, TomTomMicroTask, Province
import csv
from django.contrib.gis.geos import fromstr
from atlas.models import Location
from atlas.utils import get_city
from celery import task
import logging
logger = logging.getLogger('django.request')


@task(ignore_result=True)
def process_upload(csv_file, campaign_slug):
    #csv_file = open(file, 'rU')
    rows = read_data_from_csv_file(csv_file)
    campaign = Campaign.objects.get(slug=campaign_slug)

    for r in rows:
        try:
            TomTomMicroTask.objects.get(poi_id=r['POI_ID'])
        except TomTomMicroTask.DoesNotExist:
            create_task(campaign, r)


def create_task(campaign, r):
    t = TomTomMicroTask(poi_id=r['POI_ID'])
    loc = Location()
    # srid is the ID for the coordinate system, 4326
    # specifies longitude/latitude coordinates
    loc.coordinates = fromstr("POINT (%s %s)" % (r['X'], r['Y']), srid=4326)
    city = get_city(position=loc.coordinates)

    if not city:
        logger.error('Unable to create task: %s - %s. Could not obtain city from coordinates. (%s, %s)',
            r['NAME'], r['POI_ID'], r['Y'], r['X'])
        return

    loc.city = city
    loc.country = city.country
    loc.save()

    t.title = r['NAME']
    t.description = '%s %s' % (r['NAME_ALT'], r['ADDRESS'])
    t.category = r['CAT_NAME']
    t.location = loc
    t.tel_1 = r['TEL_NR']
    t.tel_2 = r['TEL_NR2']
    t.fax = r['FAX_NR']
    t.email = r['E_MAIL']
    t.website = r['WEBSITE']

    t.city = r['CITY']
    t.suburb = r['SUBURB']
    t.owner = campaign.owner
    t.campaign = campaign
    t.save()

    t.province.add(Province.from_str(r['PROVINCE']))
    t.sites.add(Site.objects.get_current())

    t.publish()


def read_data_from_csv_file(csvfile_name):
    with open(csvfile_name, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Only process rows that actually have data
            if any([column for column in row]):
                yield row
