from django.core.management.base import BaseCommand
from ummeli.opportunities.models import MicroTask


class Command(BaseCommand):
    help = 'Expire micro tasks that have been checked out for longer than limit'

    def handle(self, **options):
        MicroTask.expire_tasks()
