from django.contrib.sites.models import Site
from ummeli.opportunities.models import Campaign, TomTomMicroTask, Province
import csv
from django.contrib.gis.geos import fromstr
from atlas.models import Location
from atlas.utils import get_city
from celery import task


@task(ignore_result=True)
def process_upload(csv_file, campaign_slug):
    #csv_file = open(file, 'rU')
    rows = read_data_from_csv_file(csv_file)
    campaign = Campaign.objects.get(slug=campaign_slug)

    for r in rows:
        try:
            t = TomTomMicroTask.objects.get(poi_id=r['POI_ID'])
        except TomTomMicroTask.DoesNotExist:
            t = TomTomMicroTask(poi_id=r['POI_ID'])
            loc = Location()
            # srid is the ID for the coordinate system, 4326
            # specifies longitude/latitude coordinates
            loc.coordinates = fromstr("POINT (%s %s)" % (r['X'], r['Y']),
                                        srid=4326)
            loc.city = get_city(position=loc.coordinates)
            loc.country = loc.city.country
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

            t.website = r['CITY']
            t.website = r['SUBURB']
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
