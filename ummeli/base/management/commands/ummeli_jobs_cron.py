from django.core.management.base import BaseCommand
from ummeli.vlive.jobs import tasks

class Command(BaseCommand):
    help = 'update jobs from wegotads'

    def handle(self, **options):    
        tasks.run_jobs_update.delay()
